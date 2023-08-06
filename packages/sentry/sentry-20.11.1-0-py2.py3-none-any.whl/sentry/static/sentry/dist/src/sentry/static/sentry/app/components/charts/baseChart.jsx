import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import { withTheme } from 'emotion-theming';
import React from 'react';
import 'zrender/lib/svg/svg';
import ReactEchartsCore from 'echarts-for-react/lib/core';
import echarts from 'echarts/lib/echarts';
import styled from '@emotion/styled';
import { IS_ACCEPTANCE_TEST } from 'app/constants';
import space from 'app/styles/space';
import Grid from './components/grid';
import Legend from './components/legend';
import LineSeries from './series/lineSeries';
import Tooltip from './components/tooltip';
import XAxis from './components/xAxis';
import YAxis from './components/yAxis';
// If dimension is a number convert it to pixels, otherwise use dimension without transform
var getDimensionValue = function (dimension) {
    if (typeof dimension === 'number') {
        return dimension + "px";
    }
    if (dimension === null) {
        return undefined;
    }
    return dimension;
};
var BaseChart = /** @class */ (function (_super) {
    __extends(BaseChart, _super);
    function BaseChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getEventsMap = {
            click: function (props, instance) {
                var _a, _b;
                _this.handleClick(props, instance);
                (_b = (_a = _this.props).onClick) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance);
            },
            highlight: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onHighlight) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            mouseover: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onMouseOver) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            datazoom: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onDataZoom) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            restore: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onRestore) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            finished: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onFinished) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            rendered: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onRendered) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
            legendselectchanged: function (props, instance) { var _a, _b; return (_b = (_a = _this.props).onLegendSelectChanged) === null || _b === void 0 ? void 0 : _b.call(_a, props, instance); },
        };
        // TODO(ts): What is the series type? EChartOption.Series's data cannot have
        // `onClick` since it's typically an array.
        /**
         * Handle series item clicks (e.g. Releases mark line or a single series item)
         * This is different than when you hover over an "axis" line on a chart (e.g.
         * if there are 2 series for an axis and you're not directly hovered over an item)
         *
         * Calls "onClick" inside of series data
         */
        _this.handleClick = function (series, instance) {
            var _a, _b;
            if (series.data) {
                (_b = (_a = series.data).onClick) === null || _b === void 0 ? void 0 : _b.call(_a, series, instance);
            }
        };
        return _this;
    }
    BaseChart.prototype.getColorPalette = function () {
        var _a = this.props, theme = _a.theme, series = _a.series;
        var palette = (series === null || series === void 0 ? void 0 : series.length) ? theme.charts.getColorPalette(series.length)
            : theme.charts.colors;
        return palette;
    };
    BaseChart.prototype.getSeries = function () {
        var _a, _b, _c, _d;
        var _e = this.props, previousPeriod = _e.previousPeriod, series = _e.series, theme = _e.theme, transformSinglePointToBar = _e.transformSinglePointToBar;
        var hasSinglePoints = (_a = series) === null || _a === void 0 ? void 0 : _a.every(function (s) { return Array.isArray(s.data) && s.data.length === 1; });
        var transformedSeries = (_c = (hasSinglePoints && transformSinglePointToBar
            ? (_b = series) === null || _b === void 0 ? void 0 : _b.map(function (s) { return (__assign(__assign({}, s), { type: 'bar', barWidth: 40, barGap: 0 })); }) : series)) !== null && _c !== void 0 ? _c : [];
        var transformedPreviousPeriod = (_d = previousPeriod === null || previousPeriod === void 0 ? void 0 : previousPeriod.map(function (previous) {
            return LineSeries({
                name: previous.seriesName,
                data: previous.data.map(function (_a) {
                    var name = _a.name, value = _a.value;
                    return [name, value];
                }),
                lineStyle: {
                    color: theme.gray200,
                    type: 'dotted',
                },
                itemStyle: {
                    color: theme.gray200,
                },
            });
        })) !== null && _d !== void 0 ? _d : [];
        if (!previousPeriod) {
            return transformedSeries;
        }
        return __spread(transformedSeries, transformedPreviousPeriod);
    };
    BaseChart.prototype.render = function () {
        var _a;
        var _b = this.props, theme = _b.theme, options = _b.options, colors = _b.colors, grid = _b.grid, tooltip = _b.tooltip, legend = _b.legend, series = _b.series, yAxis = _b.yAxis, xAxis = _b.xAxis, dataZoom = _b.dataZoom, toolBox = _b.toolBox, graphic = _b.graphic, axisPointer = _b.axisPointer, isGroupedByDate = _b.isGroupedByDate, showTimeInTooltip = _b.showTimeInTooltip, useShortDate = _b.useShortDate, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc, yAxes = _b.yAxes, xAxes = _b.xAxes, devicePixelRatio = _b.devicePixelRatio, height = _b.height, width = _b.width, renderer = _b.renderer, notMerge = _b.notMerge, lazyUpdate = _b.lazyUpdate, style = _b.style, forwardedRef = _b.forwardedRef, onChartReady = _b.onChartReady;
        var defaultAxesProps = { theme: theme };
        var yAxisOrCustom = !yAxes
            ? yAxis !== null
                ? YAxis(__assign({ theme: theme }, yAxis))
                : undefined
            : Array.isArray(yAxes)
                ? yAxes.map(function (axis) { return YAxis(__assign(__assign({}, axis), { theme: theme })); })
                : [YAxis(defaultAxesProps), YAxis(defaultAxesProps)];
        var xAxisOrCustom = !xAxes
            ? xAxis !== null
                ? XAxis(__assign(__assign({}, xAxis), { theme: theme,
                    useShortDate: useShortDate,
                    start: start,
                    end: end,
                    period: period,
                    isGroupedByDate: isGroupedByDate,
                    utc: utc }))
                : undefined
            : Array.isArray(xAxes)
                ? xAxes.map(function (axis) {
                    return XAxis(__assign(__assign({}, axis), { theme: theme, useShortDate: useShortDate, start: start, end: end, period: period, isGroupedByDate: isGroupedByDate, utc: utc }));
                })
                : [XAxis(defaultAxesProps), XAxis(defaultAxesProps)];
        // Maybe changing the series type to types/echarts Series[] would be a better solution
        // and can't use ignore for multiline blocks
        // @ts-expect-error
        var seriesValid = series && ((_a = series[0]) === null || _a === void 0 ? void 0 : _a.data) && series[0].data.length > 1;
        // @ts-expect-error
        var seriesData = seriesValid ? series[0].data : undefined;
        var bucketSize = seriesData ? seriesData[1][0] - seriesData[0][0] : undefined;
        return (<ChartContainer>
        <ReactEchartsCore ref={forwardedRef} echarts={echarts} notMerge={notMerge} lazyUpdate={lazyUpdate} theme={this.props.echartsTheme} onChartReady={onChartReady} onEvents={this.getEventsMap} opts={{
            height: height,
            width: width,
            renderer: renderer,
            devicePixelRatio: devicePixelRatio,
        }} style={__assign({ height: getDimensionValue(height), width: getDimensionValue(width) }, style)} option={__assign(__assign({ animation: IS_ACCEPTANCE_TEST ? false : true }, options), { useUTC: utc, color: colors || this.getColorPalette(), grid: Array.isArray(grid) ? grid.map(Grid) : Grid(grid), tooltip: tooltip !== null
                ? Tooltip(__assign({ showTimeInTooltip: showTimeInTooltip,
                    isGroupedByDate: isGroupedByDate,
                    utc: utc,
                    bucketSize: bucketSize }, tooltip))
                : undefined, legend: legend ? Legend(__assign({}, legend)) : undefined, yAxis: yAxisOrCustom, xAxis: xAxisOrCustom, series: this.getSeries(), axisPointer: axisPointer,
            dataZoom: dataZoom, toolbox: toolBox, graphic: graphic })}/>
      </ChartContainer>);
    };
    BaseChart.defaultProps = {
        height: 200,
        width: 'auto',
        renderer: 'svg',
        notMerge: true,
        lazyUpdate: false,
        onChartReady: function () { },
        options: {},
        series: [],
        xAxis: {},
        yAxis: {},
        isGroupedByDate: false,
        transformSinglePointToBar: false,
    };
    return BaseChart;
}(React.Component));
// Contains styling for chart elements as we can't easily style those
// elements directly
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Tooltip styling */\n  .tooltip-series,\n  .tooltip-date {\n    color: ", ";\n    font-family: ", ";\n    background: ", ";\n    padding: ", " ", ";\n    border-radius: ", " ", " 0 0;\n  }\n  .tooltip-series-solo {\n    border-radius: ", ";\n  }\n  .tooltip-label {\n    margin-right: ", ";\n  }\n  .tooltip-label strong {\n    font-weight: normal;\n    color: ", ";\n  }\n  .tooltip-series > div {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n  }\n  .tooltip-date {\n    border-top: 1px solid ", ";\n    text-align: center;\n    position: relative;\n    width: auto;\n    border-radius: ", ";\n  }\n  .tooltip-arrow {\n    top: 100%;\n    left: 50%;\n    border: 0px solid transparent;\n    content: ' ';\n    height: 0;\n    width: 0;\n    position: absolute;\n    pointer-events: none;\n    border-top-color: ", ";\n    border-width: 8px;\n    margin-left: -8px;\n  }\n\n  .echarts-for-react div:first-of-type {\n    width: 100% !important;\n  }\n"], ["\n  /* Tooltip styling */\n  .tooltip-series,\n  .tooltip-date {\n    color: ", ";\n    font-family: ", ";\n    background: ", ";\n    padding: ", " ", ";\n    border-radius: ", " ", " 0 0;\n  }\n  .tooltip-series-solo {\n    border-radius: ", ";\n  }\n  .tooltip-label {\n    margin-right: ", ";\n  }\n  .tooltip-label strong {\n    font-weight: normal;\n    color: ", ";\n  }\n  .tooltip-series > div {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n  }\n  .tooltip-date {\n    border-top: 1px solid ", ";\n    text-align: center;\n    position: relative;\n    width: auto;\n    border-radius: ", ";\n  }\n  .tooltip-arrow {\n    top: 100%;\n    left: 50%;\n    border: 0px solid transparent;\n    content: ' ';\n    height: 0;\n    width: 0;\n    position: absolute;\n    pointer-events: none;\n    border-top-color: ", ";\n    border-width: 8px;\n    margin-left: -8px;\n  }\n\n  .echarts-for-react div:first-of-type {\n    width: 100% !important;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.gray500; }, space(1), space(2), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, space(1), function (p) { return p.theme.white; }, function (p) { return p.theme.gray400; }, function (p) { return p.theme.borderRadiusBottom; }, function (p) { return p.theme.gray500; });
var BaseChartWithTheme = withTheme(BaseChart);
var BaseChartRef = React.forwardRef(function (props, ref) { return <BaseChartWithTheme forwardedRef={ref} {...props}/>; });
BaseChartRef.displayName = 'forwardRef(BaseChart)';
export default BaseChartRef;
var templateObject_1;
//# sourceMappingURL=baseChart.jsx.map