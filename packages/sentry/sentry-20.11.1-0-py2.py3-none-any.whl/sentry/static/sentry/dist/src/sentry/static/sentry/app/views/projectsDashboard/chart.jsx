import { __read } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import BaseChart from 'app/components/charts/baseChart';
import theme from 'app/utils/theme';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import NoEvents from './noEvents';
var Chart = function (_a) {
    var firstEvent = _a.firstEvent, stats = _a.stats, transactionStats = _a.transactionStats;
    var series = [];
    var hasTransactions = transactionStats !== undefined;
    if (transactionStats) {
        var transactionSeries = transactionStats.map(function (_a) {
            var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
            return [
                timestamp * 1000,
                value,
            ];
        });
        series.push({
            cursor: 'normal',
            name: t('Transactions'),
            type: 'bar',
            data: transactionSeries,
            barMinHeight: 1,
            xAxisIndex: 1,
            yAxisIndex: 1,
            itemStyle: {
                color: theme.gray200,
                opacity: 0.8,
                emphasis: {
                    color: theme.gray200,
                    opacity: 1.0,
                },
            },
        });
    }
    if (stats) {
        series.push({
            cursor: 'normal',
            name: t('Errors'),
            type: 'bar',
            data: stats.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
                return [timestamp * 1000, value];
            }),
            barMinHeight: 1,
            xAxisIndex: 0,
            yAxisIndex: 0,
            itemStyle: {
                color: theme.purple300,
                opacity: 0.6,
                emphasis: {
                    color: theme.purple300,
                    opacity: 0.8,
                },
            },
        });
    }
    var grid = hasTransactions
        ? [
            {
                top: 10,
                bottom: 60,
                left: 2,
                right: 2,
            },
            {
                top: 105,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ]
        : [
            {
                top: 10,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ];
    var chartOptions = {
        series: series,
        colors: [],
        height: 150,
        isGroupedByDate: true,
        showTimeInTooltip: true,
        grid: grid,
        tooltip: {
            trigger: 'axis',
        },
        xAxes: Array.from(new Array(series.length)).map(function (_i, index) { return ({
            gridIndex: index,
            boundaryGap: true,
            axisLine: {
                show: false,
            },
            axisTick: {
                show: false,
            },
            axisLabel: {
                show: false,
            },
            axisPointer: {
                type: 'line',
                label: {
                    show: false,
                },
                lineStyle: {
                    width: 0,
                },
            },
        }); }),
        yAxes: Array.from(new Array(series.length)).map(function (_i, index) { return ({
            gridIndex: index,
            interval: Infinity,
            max: function (value) {
                // This keeps small datasets from looking 'scary'
                // by having full bars for < 10 values.
                return Math.max(10, value.max);
            },
            axisLabel: {
                margin: 2,
                showMaxLabel: true,
                showMinLabel: false,
                color: theme.chartLabel,
                fontFamily: theme.text.family,
                inside: true,
                lineHeight: 12,
                formatter: function (value) { return axisLabelFormatter(value, 'count()', true); },
                textBorderColor: theme.backgroundSecondary,
                textBorderWidth: 1,
            },
            splitLine: {
                show: false,
            },
            zlevel: theme.zIndex.header,
        }); }),
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        },
        options: {
            animation: false,
        },
    };
    return (<React.Fragment>
      <BaseChart {...chartOptions}/>
      {!firstEvent && <NoEvents seriesCount={series.length}/>}
    </React.Fragment>);
};
export default Chart;
//# sourceMappingURL=chart.jsx.map