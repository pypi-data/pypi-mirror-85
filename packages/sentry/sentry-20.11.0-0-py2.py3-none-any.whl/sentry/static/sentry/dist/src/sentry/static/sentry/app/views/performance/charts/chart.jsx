import { __assign, __extends } from "tslib";
import React from 'react';
import max from 'lodash/max';
import min from 'lodash/min';
import AreaChart from 'app/components/charts/areaChart';
import ChartZoom from 'app/components/charts/chartZoom';
import { aggregateOutputType } from 'app/utils/discover/fields';
import { tooltipFormatter, axisLabelFormatter } from 'app/utils/discover/charts';
import theme from 'app/utils/theme';
// adapted from https://stackoverflow.com/questions/11397239/rounding-up-for-a-graph-maximum
function computeAxisMax(data) {
    // assumes min is 0
    var valuesDict = data.map(function (value) { return value.data.map(function (point) { return point.value; }); });
    var maxValue = max(valuesDict.map(max));
    if (maxValue <= 1) {
        return 1;
    }
    var power = Math.log10(maxValue);
    var magnitude = min([max([Math.pow(10, (power - Math.floor(power))), 0]), 10]);
    var scale;
    if (magnitude <= 2.5) {
        scale = 0.2;
    }
    else if (magnitude <= 5) {
        scale = 0.5;
    }
    else if (magnitude <= 7.5) {
        scale = 1.0;
    }
    else {
        scale = 2.0;
    }
    var step = Math.pow(10, Math.floor(power)) * scale;
    return Math.round(Math.ceil(maxValue / step) * step);
}
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Chart.prototype.render = function () {
        var _a = this.props, data = _a.data, router = _a.router, statsPeriod = _a.statsPeriod, utc = _a.utc, projects = _a.projects, environments = _a.environments, loading = _a.loading;
        if (!data || data.length <= 0) {
            return null;
        }
        var colors = theme.charts.getColorPalette(4);
        var durationOnly = data.every(function (value) { return aggregateOutputType(value.seriesName) === 'duration'; });
        var dataMax = durationOnly ? computeAxisMax(data) : undefined;
        var areaChartProps = {
            seriesOptions: {
                showSymbol: false,
            },
            grid: [
                {
                    top: '8px',
                    left: '24px',
                    right: '52%',
                    bottom: '16px',
                },
                {
                    top: '8px',
                    left: '52%',
                    right: '24px',
                    bottom: '16px',
                },
            ],
            axisPointer: {
                // Link the two series x-axis together.
                link: [{ xAxisIndex: [0, 1] }],
            },
            xAxes: [
                {
                    gridIndex: 0,
                    type: 'time',
                },
                {
                    gridIndex: 1,
                    type: 'time',
                },
            ],
            yAxes: [
                {
                    gridIndex: 0,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return axisLabelFormatter(value, data[0].seriesName);
                        },
                    },
                },
                {
                    gridIndex: 1,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return axisLabelFormatter(value, data[1].seriesName);
                        },
                    },
                },
            ],
            utc: utc,
            isGroupedByDate: true,
            showTimeInTooltip: true,
            colors: [colors[0], colors[1]],
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return tooltipFormatter(value, seriesName);
                },
                nameFormatter: function (value) {
                    return value === 'epm()' ? 'tpm()' : value;
                },
            },
        };
        if (loading) {
            return <AreaChart series={[]} {...areaChartProps}/>;
        }
        var series = data.map(function (values, i) { return (__assign(__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); });
        return (<ChartZoom router={router} period={statsPeriod} utc={utc} projects={projects} environments={environments} xAxisIndex={[0, 1]}>
        {function (zoomRenderProps) { return (<AreaChart {...zoomRenderProps} series={series} {...areaChartProps}/>); }}
      </ChartZoom>);
    };
    return Chart;
}(React.Component));
export default Chart;
//# sourceMappingURL=chart.jsx.map