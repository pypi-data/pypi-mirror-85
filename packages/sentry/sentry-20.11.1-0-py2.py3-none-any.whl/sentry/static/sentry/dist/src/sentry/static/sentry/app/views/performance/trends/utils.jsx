var _a, _b, _c, _d;
import { __assign, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import { ASAP } from 'downsample/methods/ASAP';
import theme from 'app/utils/theme';
import { getInterval } from 'app/components/charts/utils';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import Duration from 'app/components/duration';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { IconArrow } from 'app/icons';
import { TrendChangeType, TrendFunctionField, } from './types';
export var DEFAULT_TRENDS_STATS_PERIOD = '14d';
export var DEFAULT_MAX_DURATION = '15min';
export var TRENDS_FUNCTIONS = [
    {
        label: 'Duration (p50)',
        field: TrendFunctionField.P50,
        alias: 'percentile_range',
        chartLabel: 'p50()',
        legendLabel: 'p50',
    },
    {
        label: 'Duration (p75)',
        field: TrendFunctionField.P75,
        alias: 'percentile_range',
        chartLabel: 'p75()',
        legendLabel: 'p75',
    },
    {
        label: 'Duration (p95)',
        field: TrendFunctionField.P95,
        alias: 'percentile_range',
        chartLabel: 'p95()',
        legendLabel: 'p95',
    },
    {
        label: 'Duration (p99)',
        field: TrendFunctionField.P99,
        alias: 'percentile_range',
        chartLabel: 'p99()',
        legendLabel: 'p99',
    },
    {
        label: 'Duration (average)',
        field: TrendFunctionField.AVG,
        alias: 'avg_range',
        chartLabel: 'avg(transaction.duration)',
        legendLabel: 'average',
    },
];
export var CONFIDENCE_LEVELS = [
    {
        label: 'High',
        min: 6,
    },
    {
        label: 'Low',
        min: 0,
        max: 6,
    },
    {
        label: 'Any',
    },
];
export var trendToColor = (_a = {},
    _a[TrendChangeType.IMPROVED] = {
        lighter: theme.green200,
        default: theme.green300,
    },
    _a[TrendChangeType.REGRESSION] = {
        lighter: theme.red200,
        default: theme.red300,
    },
    _a);
export var trendSelectedQueryKeys = (_b = {},
    _b[TrendChangeType.IMPROVED] = 'improvedSelected',
    _b[TrendChangeType.REGRESSION] = 'regressionSelected',
    _b);
export var trendUnselectedSeries = (_c = {},
    _c[TrendChangeType.IMPROVED] = 'improvedUnselectedSeries',
    _c[TrendChangeType.REGRESSION] = 'regressionUnselectedSeries',
    _c);
export var trendCursorNames = (_d = {},
    _d[TrendChangeType.IMPROVED] = 'improvedCursor',
    _d[TrendChangeType.REGRESSION] = 'regressionCursor',
    _d);
export function resetCursors() {
    var cursors = {};
    Object.values(trendCursorNames).forEach(function (cursor) { return (cursors[cursor] = undefined); }); // Resets both cursors
    return cursors;
}
export function getCurrentTrendFunction(location) {
    var _a;
    var trendFunctionField = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.trendFunction);
    var trendFunction = TRENDS_FUNCTIONS.find(function (_a) {
        var field = _a.field;
        return field === trendFunctionField;
    });
    return trendFunction || TRENDS_FUNCTIONS[0];
}
export function getCurrentConfidenceLevel(location) {
    var _a;
    var confidenceLevelLabel = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.confidenceLevel);
    var confidenceLevel = CONFIDENCE_LEVELS.find(function (_a) {
        var label = _a.label;
        return label === confidenceLevelLabel;
    });
    return confidenceLevel || CONFIDENCE_LEVELS[0];
}
export function getIntervalRatio(location) {
    var _a;
    var intervalFromLocation = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.intervalRatio);
    return intervalFromLocation ? parseFloat(intervalFromLocation) : 0.5;
}
export function transformDeltaSpread(from, to) {
    var fromSeconds = from / 1000;
    var toSeconds = to / 1000;
    var showDigits = from > 1000 || to > 1000 || from < 10 || to < 10; // Show digits consistently if either has them
    return (<span>
      <Duration seconds={fromSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
      <StyledIconArrow direction="right" size="xs"/>
      <Duration seconds={toSeconds} fixedDigits={showDigits ? 1 : 0} abbreviation/>
    </span>);
}
export function getTrendProjectId(trend, projects) {
    if (!trend.project || !projects) {
        return undefined;
    }
    var transactionProject = projects.find(function (project) { return project.slug === trend.project; });
    return transactionProject === null || transactionProject === void 0 ? void 0 : transactionProject.id;
}
export function modifyTrendView(trendView, location, trendsType, isProjectOnly) {
    var trendFunction = getCurrentTrendFunction(location);
    var confidenceLevel = getCurrentConfidenceLevel(location);
    var transactionField = isProjectOnly ? [] : ['transaction'];
    var fields = __spread(transactionField, ['project']).map(function (field) { return ({
        field: field,
    }); });
    var trendSort = {
        field: 'trend_percentage()',
        kind: 'asc',
    };
    trendView.trendType = trendsType;
    if (trendsType === TrendChangeType.REGRESSION) {
        trendSort.kind = 'desc';
    }
    if (trendFunction) {
        trendView.trendFunction = trendFunction.field;
    }
    trendView.query = getLimitTransactionItems(trendView.query, trendsType, confidenceLevel);
    trendView.interval = getQueryInterval(location, trendView);
    trendView.sorts = [trendSort];
    trendView.fields = fields;
}
export function modifyTrendsViewDefaultPeriod(eventView, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    if (!query.statsPeriod && !hasStartAndEnd) {
        eventView.statsPeriod = DEFAULT_TRENDS_STATS_PERIOD;
    }
    return eventView;
}
function getQueryInterval(location, eventView) {
    var _a;
    var intervalFromQueryParam = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.interval);
    var start = eventView.start, end = eventView.end, statsPeriod = eventView.statsPeriod;
    var datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    var intervalFromSmoothing = getInterval(datetimeSelection, true);
    return intervalFromQueryParam || intervalFromSmoothing;
}
export function transformValueDelta(value, trendType) {
    var absoluteValue = Math.abs(value);
    var changeLabel = trendType === TrendChangeType.REGRESSION ? t('slower') : t('faster');
    var seconds = absoluteValue / 1000;
    var fixedDigits = absoluteValue > 1000 || absoluteValue < 10 ? 1 : 0;
    return (<span>
      <Duration seconds={seconds} fixedDigits={fixedDigits} abbreviation/> {changeLabel}
    </span>);
}
/**
 * This will normalize the trends transactions while the current trend function and current data are out of sync
 * To minimize extra renders with missing results.
 */
export function normalizeTrends(data) {
    var received_at = moment(); // Adding the received time for the transaction so calls to get baseline always line up with the transaction
    return data.map(function (row) {
        return __assign(__assign({}, row), { received_at: received_at, transaction: row.transaction });
    });
}
export function getSelectedQueryKey(trendChangeType) {
    return trendSelectedQueryKeys[trendChangeType];
}
export function getUnselectedSeries(trendChangeType) {
    return trendUnselectedSeries[trendChangeType];
}
export function movingAverage(data, index, size) {
    return (data
        .slice(index - size, index)
        .map(function (a) { return a.value; })
        .reduce(function (a, b) { return a + b; }, 0) / size);
}
/**
 * This function applies defaults for trend and count percentage, and adds the confidence limit to the query
 */
function getLimitTransactionItems(query, trendChangeType, confidenceLevel) {
    var limitQuery = tokenizeSearch(query);
    if (!limitQuery.hasTag('count_percentage()')) {
        limitQuery.addTagValues('count_percentage()', ['>0.25', '<4']);
    }
    if (!limitQuery.hasTag('trend_percentage()')) {
        limitQuery.addTagValues('trend_percentage()', ['>0%']);
    }
    if (!limitQuery.hasTag('t_test()')) {
        var tagValues = [];
        if (trendChangeType === TrendChangeType.REGRESSION) {
            if (confidenceLevel.hasOwnProperty('min')) {
                tagValues.push("<-" + confidenceLevel.min);
            }
            if (confidenceLevel.hasOwnProperty('max')) {
                tagValues.push(">=-" + confidenceLevel.max);
            }
        }
        else {
            if (confidenceLevel.hasOwnProperty('min')) {
                tagValues.push(">" + confidenceLevel.min);
            }
            if (confidenceLevel.hasOwnProperty('max')) {
                tagValues.push("<=" + confidenceLevel.max);
            }
        }
        limitQuery.addTagValues('t_test()', tagValues);
    }
    return limitQuery.formatString();
}
export var smoothTrend = function (data, resolution) {
    if (resolution === void 0) { resolution = 100; }
    return ASAP(data, resolution);
};
export function transformEventStatsSmoothed(data, seriesName) {
    var minValue = Number.MAX_SAFE_INTEGER;
    var maxValue = 0;
    if (!data) {
        return {
            maxValue: maxValue,
            minValue: minValue,
            smoothedResults: undefined,
        };
    }
    var currentData = data[0].data;
    var resultData = [];
    var smoothed = smoothTrend(currentData.map(function (_a) {
        var name = _a.name, value = _a.value;
        return [Number(name), value];
    }));
    for (var i = 0; i < smoothed.length; i++) {
        var point = smoothed[i];
        var value = point.y;
        resultData.push({
            name: point.x,
            value: value,
        });
        if (!isNaN(value)) {
            var rounded = Math.round(value);
            minValue = Math.min(rounded, minValue);
            maxValue = Math.max(rounded, maxValue);
        }
    }
    return {
        minValue: minValue,
        maxValue: maxValue,
        smoothedResults: [
            {
                seriesName: seriesName || 'Current',
                data: resultData,
            },
        ],
    };
}
export var StyledIconArrow = styled(IconArrow)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map