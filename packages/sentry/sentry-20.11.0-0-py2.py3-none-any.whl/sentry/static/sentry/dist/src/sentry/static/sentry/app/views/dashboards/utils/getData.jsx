import { __assign, __read, __rest, __spread } from "tslib";
import { t } from 'app/locale';
import { WIDGET_DISPLAY } from '../constants';
import { getChartDataFunc } from './getChartDataFunc';
import { isTimeSeries } from './isTimeSeries';
// TODO(billy): Currently only supports discover queries
export function getData(results, widget) {
    var _a;
    var type = widget.type, queries = widget.queries, yAxisMapping = widget.yAxisMapping;
    var isTable = type === WIDGET_DISPLAY.TABLE;
    var _b = __read(getChartDataFunc(widget), 2), chartDataFunc = _b[0], chartDataFuncArgs = _b[1];
    var hasYAxes = yAxisMapping && yAxisMapping.length === 2;
    if (isTable) {
        var _c = __read(chartDataFunc.apply(void 0, __spread([results[0].data,
            queries.discover[0]], chartDataFuncArgs)), 1), series_1 = _c[0];
        return {
            title: t('Name'),
            countTitle: t('Events'),
            data: series_1.data,
        };
    }
    var series = results
        .map(function (result, i) {
        return chartDataFunc(result.data, queries.discover[i], __assign(__assign({}, chartDataFuncArgs), { formatVersion: true }));
    })
        .reduce(function (acc, s) { return __spread(acc, s); }, []);
    // Has 2 y axes
    if (hasYAxes) {
        yAxisMapping === null || yAxisMapping === void 0 ? void 0 : yAxisMapping.forEach(function (mappings, yAxisIndex) {
            mappings.forEach(function (seriesIndex) {
                if (typeof series[seriesIndex] === 'undefined') {
                    return;
                }
                series[seriesIndex].yAxisIndex = yAxisIndex;
            });
        });
    }
    var previousPeriod = null;
    // XXX(billy): Probably will need to be more generic in future
    // Instead of simply doubling period for previous period
    // we'll want to a second query with a specific period. that way
    // we can compare to "this time last month" (or anything else besides the very last period)
    if (widget.includePreviousPeriod) {
        // `series` is an array of series objects
        // need to map through each one and split up data into 2 series objects
        // (one for previous period and one for the current period)
        _a = __read(series
            .map(function (_a) {
            var data = _a.data, seriesName = _a.seriesName, rest = __rest(_a, ["data", "seriesName"]);
            // Split data into halves
            var previousPeriodData = data.slice(0, Math.ceil(data.length / 2));
            var currentPeriodData = data.slice(Math.floor(data.length / 2));
            return [
                __assign({ seriesName: seriesName + " (Previous Period)", data: previousPeriodData.map(function (_a, index) {
                        var name = _a.name, value = _a.value;
                        return ({
                            value: value,
                            originalTimestamp: name,
                            name: currentPeriodData[index].name,
                        });
                    }) }, rest),
                __assign({ seriesName: seriesName, data: currentPeriodData }, rest),
            ];
        })
            .reduce(
        // reduce down to a tuple of [PreviousPeriodSeriesObj[], CurrentPeriodSeriesObj[]]
        function (_a, _b) {
            var _c = __read(_a, 2), accPrev = _c[0], accSeries = _c[1];
            var _d = __read(_b, 2), prev = _d[0], currentSeries = _d[1];
            return [
                __spread(accPrev, [prev]),
                __spread(accSeries, [currentSeries]),
            ];
        }, [[], []]), 2), previousPeriod = _a[0], series = _a[1];
    }
    var isTime = queries.discover.some(isTimeSeries);
    return {
        isGroupedByDate: isTime,
        xAxis: __assign({}, (!isTime && { truncate: 80 })),
        grid: {
            left: '16px',
            right: '16px',
        },
        series: series,
        previousPeriod: previousPeriod,
        yAxes: hasYAxes,
    };
}
//# sourceMappingURL=getData.jsx.map