import { __read, __spread } from "tslib";
import React from 'react';
import moment from 'moment';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import LineChart from 'app/components/charts/lineChart';
import MarkPoint from 'app/components/charts/components/markPoint';
import MarkLine from 'app/components/charts/components/markLine';
import closedSymbol from './closedSymbol';
import startedSymbol from './startedSymbol';
/**
 * So we'll have to see how this looks with real data, but echarts requires
 * an explicit (x,y) value to draw a symbol (incident started/closed bubble).
 *
 * This uses the closest date *without* going over.
 *
 * AFAICT we can't give it an x-axis value and have it draw on the line,
 * so we probably need to calculate the y-axis value ourselves if we want it placed
 * at the exact time.
 *
 * @param data Data array
 * @param needle the target timestamp
 */
function getNearbyIndex(data, needle) {
    // `data` is sorted, return the first index whose value (timestamp) is > `needle`
    var index = data.findIndex(function (_a) {
        var _b = __read(_a, 1), ts = _b[0];
        return ts > needle;
    });
    // this shouldn't happen, as we try to buffer dates before start/end dates
    if (index === 0) {
        return 0;
    }
    return index !== -1 ? index - 1 : data.length - 1;
}
var Chart = function (props) {
    var aggregate = props.aggregate, data = props.data, started = props.started, closed = props.closed, triggers = props.triggers, resolveThreshold = props.resolveThreshold;
    var startedTs = started && moment.utc(started).unix();
    var closedTs = closed && moment.utc(closed).unix();
    var chartData = data.map(function (_a) {
        var _b = __read(_a, 2), ts = _b[0], val = _b[1];
        return [
            ts * 1000,
            val.length ? val.reduce(function (acc, _a) {
                var count = (_a === void 0 ? { count: 0 } : _a).count;
                return acc + count;
            }, 0) : 0,
        ];
    });
    var startedCoordinate = startedTs
        ? chartData[getNearbyIndex(data, startedTs)]
        : undefined;
    var showClosedMarker = data && closedTs && data[data.length - 1] && data[data.length - 1][0] >= closedTs
        ? true
        : false;
    var closedCoordinate = closedTs && showClosedMarker ? chartData[getNearbyIndex(data, closedTs)] : undefined;
    var seriesName = aggregate;
    var warningTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'warning'; });
    var criticalTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'critical'; });
    var warningTriggerAlertThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
        ? warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold : undefined;
    var criticalTriggerAlertThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
        ? criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold : undefined;
    var alertResolveThreshold = typeof resolveThreshold === 'number' ? resolveThreshold : undefined;
    var marklinePrecision = Math.max.apply(Math, __spread([
        warningTriggerAlertThreshold,
        criticalTriggerAlertThreshold,
        alertResolveThreshold,
    ].map(function (decimal) {
        if (!decimal || !isFinite(decimal))
            return 0;
        var e = 1;
        var p = 0;
        while (Math.round(decimal * e) / e !== decimal) {
            e *= 10;
            p += 1;
        }
        return p;
    })));
    return (<LineChart isGroupedByDate showTimeInTooltip grid={{
        left: 0,
        right: 0,
        top: space(2),
        bottom: 0,
    }} series={[
        {
            // e.g. Events or Users
            seriesName: seriesName,
            dataArray: chartData,
            markPoint: MarkPoint({
                data: __spread([
                    {
                        labelForValue: seriesName,
                        seriesName: seriesName,
                        symbol: "image://" + startedSymbol,
                        name: t('Alert Triggered'),
                        coord: startedCoordinate,
                    }
                ], (closedTs
                    ? [
                        {
                            labelForValue: seriesName,
                            seriesName: seriesName,
                            symbol: "image://" + closedSymbol,
                            symbolSize: 24,
                            name: t('Alert Resolved'),
                            coord: closedCoordinate,
                        },
                    ]
                    : [])),
            }),
        },
        warningTrigger &&
            warningTriggerAlertThreshold && {
            name: 'Warning Alert',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.yellow300 },
                data: [
                    {
                        yAxis: warningTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'WARNING',
                    color: theme.yellow300,
                    fontSize: 10,
                },
            }),
            data: [],
        },
        criticalTrigger &&
            criticalTriggerAlertThreshold && {
            name: 'Critical Alert',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.red200 },
                data: [
                    {
                        yAxis: criticalTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'CRITICAL',
                    color: theme.red300,
                    fontSize: 10,
                },
            }),
            data: [],
        },
        criticalTrigger &&
            alertResolveThreshold && {
            name: 'Critical Resolve',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.gray200 },
                data: [
                    {
                        yAxis: alertResolveThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: 'CRITICAL RESOLUTION',
                    color: theme.gray200,
                    fontSize: 10,
                },
            }),
            data: [],
        },
    ].filter(Boolean)}/>);
};
export default Chart;
//# sourceMappingURL=chart.jsx.map