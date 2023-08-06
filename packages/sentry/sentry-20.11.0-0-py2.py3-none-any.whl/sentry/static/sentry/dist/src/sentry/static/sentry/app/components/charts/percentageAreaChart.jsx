import { __assign, __extends, __read, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import moment from 'moment';
import AreaSeries from './series/areaSeries';
import BaseChart from './baseChart';
var FILLER_NAME = '__filler';
/**
 * A stacked 100% column chart over time
 *
 * See https://exceljet.net/chart-type/100-stacked-bar-chart
 */
var PercentageAreaChart = /** @class */ (function (_super) {
    __extends(PercentageAreaChart, _super);
    function PercentageAreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PercentageAreaChart.prototype.getSeries = function () {
        var _a = this.props, series = _a.series, getDataItemName = _a.getDataItemName, getValue = _a.getValue;
        var totalsArray = series.length
            ? series[0].data.map(function (_a, i) {
                var name = _a.name;
                return [
                    name,
                    series.reduce(function (sum, _a) {
                        var data = _a.data;
                        return sum + data[i].value;
                    }, 0),
                ];
            })
            : [];
        var totals = new Map(totalsArray);
        return __spread(series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data;
            return AreaSeries({
                name: seriesName,
                lineStyle: { width: 1 },
                areaStyle: { opacity: 1 },
                smooth: true,
                stack: 'percentageAreaChartStack',
                data: data.map(function (dataObj) { return [
                    getDataItemName(dataObj),
                    getValue(dataObj, totals.get(dataObj.name)),
                ]; }),
            });
        }));
    };
    PercentageAreaChart.prototype.render = function () {
        return (<BaseChart {...this.props} tooltip={{
            formatter: function (seriesParams) {
                // `seriesParams` can be an array or an object :/
                var series = Array.isArray(seriesParams) ? seriesParams : [seriesParams];
                // Filter series that have 0 counts
                var date = (series.length && moment(series[0].axisValue).format('MMM D, YYYY')) + "<br />" || '';
                return [
                    '<div class="tooltip-series">',
                    series
                        .filter(function (_a) {
                        var seriesName = _a.seriesName, data = _a.data;
                        return data[1] > 0.001 && seriesName !== FILLER_NAME;
                    })
                        .map(function (_a) {
                        var marker = _a.marker, seriesName = _a.seriesName, data = _a.data;
                        return "<div><span class=\"tooltip-label\">" + marker + " <strong>" + seriesName + "</strong></span> " + data[1] + "%</div>";
                    })
                        .join(''),
                    '</div>',
                    "<div class=\"tooltip-date\">" + date + "</div>",
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        }} xAxis={{ boundaryGap: true }} yAxis={{
            min: 0,
            max: 100,
            type: 'value',
            interval: 25,
            splitNumber: 4,
            data: [0, 25, 50, 100],
            axisLabel: {
                formatter: '{value}%',
            },
        }} series={this.getSeries()}/>);
    };
    PercentageAreaChart.propTypes = __assign(__assign({}, BaseChart.propTypes), { getDataItemName: PropTypes.func, getValue: PropTypes.func });
    PercentageAreaChart.defaultProps = {
        // TODO(billyvg): Move these into BaseChart? or get rid completely
        getDataItemName: function (_a) {
            var name = _a.name;
            return name;
        },
        getValue: function (_a, total) {
            var value = _a.value;
            return (!total ? 0 : Math.round((value / total) * 1000) / 10);
        },
    };
    return PercentageAreaChart;
}(React.Component));
export default PercentageAreaChart;
//# sourceMappingURL=percentageAreaChart.jsx.map