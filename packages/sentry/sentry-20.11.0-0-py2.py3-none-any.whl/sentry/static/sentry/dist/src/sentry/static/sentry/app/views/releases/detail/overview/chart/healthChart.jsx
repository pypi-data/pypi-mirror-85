import { __assign, __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { browserHistory } from 'react-router';
import LineChart from 'app/components/charts/lineChart';
import AreaChart from 'app/components/charts/areaChart';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import { getSeriesSelection } from 'app/components/charts/utils';
import { parseStatsPeriod } from 'app/components/organizations/timeRangeSelector/utils';
import theme from 'app/utils/theme';
import { defined } from 'app/utils';
import { getExactDuration } from 'app/utils/formatters';
import { axisDuration } from 'app/utils/discover/charts';
import { decodeList } from 'app/utils/queryString';
import { YAxis } from './releaseChartControls';
var HealthChart = /** @class */ (function (_super) {
    __extends(HealthChart, _super);
    function HealthChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { unselectedSeries: Object.keys(selected).filter(function (key) { return !selected[key]; }) }) });
            browserHistory.replace(to);
        };
        _this.formatTooltipValue = function (value) {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case YAxis.SESSION_DURATION:
                    return typeof value === 'number' ? getExactDuration(value, true) : '\u2015';
                case YAxis.CRASH_FREE:
                    return defined(value) ? value + "%" : '\u2015';
                case YAxis.SESSIONS:
                case YAxis.USERS:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        return _this;
    }
    HealthChart.prototype.componentDidMount = function () {
        if (this.shouldUnselectHealthySeries()) {
            this.props.onVisibleSeriesRecalculated();
            this.handleLegendSelectChanged({ selected: { Healthy: false } });
        }
    };
    HealthChart.prototype.shouldComponentUpdate = function (nextProps) {
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (this.props.location.query.unselectedSeries !==
            nextProps.location.query.unselectedSeries) {
            return true;
        }
        if (isEqual(this.props.timeseriesData, nextProps.timeseriesData)) {
            return false;
        }
        return true;
    };
    HealthChart.prototype.shouldUnselectHealthySeries = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, location = _a.location, shouldRecalculateVisibleSeries = _a.shouldRecalculateVisibleSeries;
        var otherAreasThanHealthyArePositive = timeseriesData
            .filter(function (s) { return s.seriesName !== 'Healthy'; })
            .some(function (s) { return s.data.some(function (d) { return d.value > 0; }); });
        var alreadySomethingUnselected = !!decodeList(location.query.unselectedSeries);
        return (shouldRecalculateVisibleSeries &&
            otherAreasThanHealthyArePositive &&
            !alreadySomethingUnselected);
    };
    HealthChart.prototype.configureYAxis = function () {
        var yAxis = this.props.yAxis;
        switch (yAxis) {
            case YAxis.CRASH_FREE:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: '{value}%',
                        color: theme.chartLabel,
                    },
                };
            case YAxis.SESSION_DURATION:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return axisDuration(value * 1000); },
                        color: theme.chartLabel,
                    },
                };
            case YAxis.SESSIONS:
            case YAxis.USERS:
            default:
                return undefined;
        }
    };
    HealthChart.prototype.configureXAxis = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps;
        if (timeseriesData.every(function (s) { return s.data.length === 1; })) {
            if (zoomRenderProps.period) {
                var _b = parseStatsPeriod(zoomRenderProps.period, null), start = _b.start, end = _b.end;
                return { min: start, max: end };
            }
            return {
                min: zoomRenderProps.start,
                max: zoomRenderProps.end,
            };
        }
        return undefined;
    };
    HealthChart.prototype.getChart = function () {
        var yAxis = this.props.yAxis;
        switch (yAxis) {
            case YAxis.SESSION_DURATION:
                return AreaChart;
            case YAxis.SESSIONS:
            case YAxis.USERS:
                return StackedAreaChart;
            case YAxis.CRASH_FREE:
            default:
                return LineChart;
        }
    };
    HealthChart.prototype.render = function () {
        var _a = this.props, utc = _a.utc, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps, location = _a.location;
        var Chart = this.getChart();
        var legend = {
            right: 22,
            top: 10,
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
            data: timeseriesData.map(function (d) { return d.seriesName; }).reverse(),
            selected: getSeriesSelection(location),
        };
        return (<Chart legend={legend} utc={utc} {...zoomRenderProps} series={timeseriesData} isGroupedByDate seriesOptions={{
            showSymbol: false,
        }} grid={{
            left: '24px',
            right: '24px',
            top: '32px',
            bottom: '12px',
        }} yAxis={this.configureYAxis()} xAxis={this.configureXAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>);
    };
    return HealthChart;
}(React.Component));
export default HealthChart;
//# sourceMappingURL=healthChart.jsx.map