import { __assign, __extends, __read, __rest, __spread } from "tslib";
import React from 'react';
import color from 'color';
import debounce from 'lodash/debounce';
import flatten from 'lodash/flatten';
import Graphic from 'app/components/charts/components/graphic';
import LineChart from 'app/components/charts/lineChart';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { AlertRuleThresholdType } from '../../types';
var CHART_GRID = {
    left: space(2),
    right: space(2),
    top: space(4),
    bottom: space(2),
};
// Colors to use for trigger thresholds
var COLOR = {
    RESOLUTION_FILL: color(theme.green200).alpha(0.1).rgb().string(),
    CRITICAL_FILL: color(theme.red300).alpha(0.25).rgb().string(),
    WARNING_FILL: color(theme.yellow200).alpha(0.1).rgb().string(),
};
/**
 * This chart displays shaded regions that represent different Trigger thresholds in a
 * Metric Alert rule.
 */
var ThresholdsChart = /** @class */ (function (_super) {
    __extends(ThresholdsChart, _super);
    function ThresholdsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
            yAxisMax: null,
        };
        _this.chartRef = null;
        // If we have ref to chart and data, try to update chart axis so that
        // alertThreshold or resolveThreshold is visible in chart
        _this.handleUpdateChartAxis = function () {
            var _a = _this.props, triggers = _a.triggers, resolveThreshold = _a.resolveThreshold;
            if (_this.chartRef) {
                _this.updateChartAxis(Math.max.apply(Math, __spread(flatten(triggers.map(function (trigger) { return [trigger.alertThreshold || 0, resolveThreshold || 0]; })))));
            }
        };
        /**
         * Updates the chart so that yAxis is within bounds of our max value
         */
        _this.updateChartAxis = debounce(function (threshold) {
            var maxValue = _this.props.maxValue;
            if (typeof maxValue !== 'undefined' && threshold > maxValue) {
                // We need to force update after we set a new yAxis max because `convertToPixel`
                // can return a negitive position (probably because yAxisMax is not synced with chart yet)
                _this.setState({ yAxisMax: Math.round(threshold * 1.1) }, _this.forceUpdate);
            }
            else {
                _this.setState({ yAxisMax: null }, _this.forceUpdate);
            }
        }, 150);
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function (chartRef) {
            if (chartRef === void 0) { chartRef = _this.chartRef; }
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            // When chart initially renders, we want to update state with its width, as well as initialize starting
            // locations (on y axis) for the draggable lines
            if (ref && typeof ref.getEchartsInstance === 'function' && !_this.chartRef) {
                _this.chartRef = ref.getEchartsInstance();
                _this.updateDimensions(_this.chartRef);
                _this.handleUpdateChartAxis();
            }
            if (!ref) {
                _this.chartRef = null;
            }
        };
        /**
         * Draws the boundary lines and shaded areas for the chart.
         *
         * May need to refactor so that they are aware of other trigger thresholds.
         *
         * e.g. draw warning from threshold -> critical threshold instead of the entire height of chart
         */
        _this.getThresholdLine = function (trigger, type, isResolution) {
            var _a;
            var _b = _this.props, thresholdType = _b.thresholdType, resolveThreshold = _b.resolveThreshold, maxValue = _b.maxValue;
            var position = type === 'alertThreshold'
                ? _this.getChartPixelForThreshold(trigger[type])
                : _this.getChartPixelForThreshold(resolveThreshold);
            var isInverted = thresholdType === AlertRuleThresholdType.BELOW;
            if (typeof position !== 'number' ||
                isNaN(position) ||
                !_this.state.height ||
                !_this.chartRef) {
                return [];
            }
            var yAxisPixelPosition = _this.chartRef.convertToPixel({ yAxisIndex: 0 }, '0');
            var yAxisPosition = typeof yAxisPixelPosition === 'number' ? yAxisPixelPosition : 0;
            // As the yAxis gets larger we want to start our line/area further to the right
            // Handle case where the graph max is 1 and includes decimals
            var yAxisMax = Math.max(maxValue !== null && maxValue !== void 0 ? maxValue : 1, (_a = _this.state.yAxisMax) !== null && _a !== void 0 ? _a : 1);
            var yAxisSize = 15 + (yAxisMax <= 1 ? 15 : ("" + (yAxisMax !== null && yAxisMax !== void 0 ? yAxisMax : '')).length * 8);
            // Distance from the top of the chart to save for the legend
            var legendPadding = 20;
            var isCritical = trigger.label === 'critical';
            var LINE_STYLE = {
                stroke: isResolution ? theme.green300 : isCritical ? theme.red300 : theme.yellow300,
                lineDash: [2],
            };
            return __spread([
                // This line is used as a "border" for the shaded region
                // and represents the threshold value.
                {
                    type: 'line',
                    // Resolution is considered "off" if it is -1
                    invisible: position === null,
                    draggable: false,
                    position: [yAxisSize, position],
                    shape: { y1: 1, y2: 1, x1: 0, x2: _this.state.width },
                    style: LINE_STYLE,
                }
            ], (position !== null && [
                {
                    type: 'rect',
                    draggable: false,
                    position: isResolution !== isInverted
                        ? [yAxisSize, position + 1]
                        : [yAxisSize, legendPadding],
                    shape: {
                        width: _this.state.width,
                        height: isResolution !== isInverted
                            ? yAxisPosition - position
                            : position - legendPadding,
                    },
                    style: {
                        fill: isResolution
                            ? COLOR.RESOLUTION_FILL
                            : isCritical
                                ? COLOR.CRITICAL_FILL
                                : COLOR.WARNING_FILL,
                    },
                    // This needs to be below the draggable line
                    z: 100,
                },
            ]));
        };
        _this.getChartPixelForThreshold = function (threshold) {
            return threshold !== '' &&
                _this.chartRef &&
                _this.chartRef.convertToPixel({ yAxisIndex: 0 }, "" + threshold);
        };
        return _this;
    }
    ThresholdsChart.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.triggers !== prevProps.triggers ||
            this.props.data !== prevProps.data) {
            this.handleUpdateChartAxis();
        }
    };
    ThresholdsChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, triggers = _a.triggers, period = _a.period;
        var dataWithoutRecentBucket = data === null || data === void 0 ? void 0 : data.map(function (_a) {
            var eventData = _a.data, restOfData = __rest(_a, ["data"]);
            return (__assign(__assign({}, restOfData), { data: eventData.slice(0, -1) }));
        });
        // Disable all lines by default but the 1st one
        var selected = dataWithoutRecentBucket.reduce(function (acc, _a, index) {
            var seriesName = _a.seriesName;
            acc[seriesName] = index === 0;
            return acc;
        }, {});
        var legend = {
            right: 10,
            top: 0,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
            selected: selected,
        };
        return (<LineChart isGroupedByDate showTimeInTooltip period={period} forwardedRef={this.handleRef} grid={CHART_GRID} yAxis={{
            max: this.state.yAxisMax,
        }} legend={legend} graphic={Graphic({
            elements: flatten(triggers.map(function (trigger) { return __spread(_this.getThresholdLine(trigger, 'alertThreshold', false), _this.getThresholdLine(trigger, 'resolveThreshold', true)); })),
        })} series={dataWithoutRecentBucket} onFinished={function () {
            // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
            // any graphics related to the triggers (e.g. the threshold areas + boundaries)
            if (!_this.chartRef) {
                return;
            }
            _this.updateDimensions(_this.chartRef);
        }}/>);
    };
    ThresholdsChart.defaultProps = {
        data: [],
    };
    return ThresholdsChart;
}(React.PureComponent));
export default ThresholdsChart;
//# sourceMappingURL=thresholdsChart.jsx.map