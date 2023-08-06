import { __assign, __makeTemplateObject, __read, __spread } from "tslib";
import orderBy from 'lodash/orderBy';
import Papa from 'papaparse';
import React from 'react';
import styled from '@emotion/styled';
import { formatVersion } from 'app/utils/formatters';
import { NUMBER_OF_SERIES_BY_DAY } from '../data';
var CHART_KEY = '__CHART_KEY__';
/**
 * Returns data formatted for basic line and bar charts, with each aggregation
 * representing a series.
 *
 * @param data Data returned from Snuba
 * @param query Query state corresponding to data
 * @returns {Array}
 */
export function getChartData(data, query) {
    var fields = query.fields;
    return query.aggregations.map(function (aggregation) { return ({
        seriesName: aggregation[2],
        animation: false,
        data: data.map(function (res) { return ({
            value: res[aggregation[2]],
            name: fields.map(function (field) { return field + " " + res[field]; }).join(' '),
        }); }),
    }); });
}
export function getChartDataForWidget(data, query, options) {
    if (options === void 0) { options = {}; }
    var fields = query.fields;
    var totalsBySeries = new Map();
    if (options.includePercentages) {
        query.aggregations.forEach(function (aggregation) {
            totalsBySeries.set(aggregation[2], data.reduce(function (acc, res) {
                acc += res[aggregation[2]];
                return acc;
            }, 0));
        });
    }
    return query.aggregations.map(function (aggregation) {
        var total = options.includePercentages && totalsBySeries.get(aggregation[2]);
        return {
            seriesName: aggregation[2],
            data: data.map(function (res) {
                var obj = {
                    value: res[aggregation[2]],
                    name: fields.map(function (field) { return "" + res[field]; }).join(', '),
                    fieldValues: fields.map(function (field) { return res[field]; }),
                };
                if (options.includePercentages && total) {
                    obj.percentage = Math.round((res[aggregation[2]] / total) * 10000) / 100;
                }
                return obj;
            }),
        };
    });
}
/**
 * Returns time series data formatted for line and bar charts, with each day
 * along the x-axis
 *
 * @param {Array} data Data returned from Snuba
 * @param {Object} query Query state corresponding to data
 * @param {Object} [options] Options object
 * @param {Boolean} [options.allSeries] (default: false) Return all series instead of top 10
 * @param {Object} [options.fieldLabelMap] (default: false) Maps value from Snuba to a defined label
 * @returns {Array}
 */
export function getChartDataByDay(rawData, query, options) {
    if (options === void 0) { options = {}; }
    // We only chart the first aggregation for now
    var aggregate = query.aggregations[0][2];
    var data = getDataWithKeys(rawData, query, options);
    // We only want to show the top 10 series
    var top10Series = getTopSeries(data, aggregate, options.allSeries ? -1 : options.allSeries);
    // Reverse to get ascending dates - we request descending to ensure latest
    // day data is complete in the case of limits being hit
    var dates = __spread(new Set(rawData.map(function (entry) { return formatDate(entry.time); }))).reverse();
    // Temporarily store series as object with series names as keys
    var seriesHash = getEmptySeriesHash(top10Series, dates);
    // Insert data into series if it's in a top 10 series
    data.forEach(function (row) {
        var key = row[CHART_KEY];
        var dateIdx = dates.indexOf(formatDate(row.time));
        if (top10Series.has(key)) {
            seriesHash[key][dateIdx].value = row[aggregate] === null ? 0 : row[aggregate];
        }
    });
    // Format for echarts
    return Object.entries(seriesHash).map(function (_a) {
        var _b = __read(_a, 2), seriesName = _b[0], series = _b[1];
        return ({
            seriesName: seriesName,
            data: series,
        });
    });
}
/**
 * Given result data and the location query, return the correct visualization
 * @param data data object for result
 * @param current visualization from querystring
 */
export function getVisualization(data, current) {
    if (current === void 0) { current = 'table'; }
    var baseQuery = data.baseQuery, byDayQuery = data.byDayQuery;
    if (!byDayQuery.data && ['line-by-day', 'bar-by-day'].includes(current)) {
        return 'table';
    }
    if (!baseQuery.query.aggregations.length && ['line', 'bar'].includes(current)) {
        return 'table';
    }
    return ['table', 'line', 'bar', 'line-by-day', 'bar-by-day'].includes(current)
        ? current
        : 'table';
}
/**
 * Returns the page ranges of paginated tables, i.e. Results 1-100
 * @param {Object} baseQuery data
 * @returns {String}
 */
export function getRowsPageRange(baseQuery) {
    var dataLength = baseQuery.data.data.length;
    if (!dataLength) {
        return '0 rows';
    }
    else if (baseQuery.query.aggregations.length) {
        return dataLength + " " + (dataLength === 1 ? 'row' : 'rows');
    }
    else {
        var startRange = parseInt(baseQuery.current.split(':')[1], 10);
        return "rows " + (startRange + 1) + " - " + (startRange + dataLength);
    }
}
// Return placeholder empty series object with all series and dates listed and
// all values set to null
function getEmptySeriesHash(seriesSet, dates) {
    var output = {};
    __spread(seriesSet).forEach(function (series) {
        output[series] = getEmptySeries(dates);
    });
    return output;
}
function getEmptySeries(dates) {
    return dates.map(function (date) { return ({
        value: 0,
        name: date,
    }); });
}
// Get the top series ranked by latest time / largest aggregate
function getTopSeries(data, aggregate, limit) {
    if (limit === void 0) { limit = NUMBER_OF_SERIES_BY_DAY; }
    var allData = orderBy(data, ['time', aggregate], ['desc', 'desc']);
    var orderedData = __spread(new Set(allData
        // `row` can be an empty time bucket, in which case it will have no `CHART_KEY` property
        .filter(function (row) { return typeof row[CHART_KEY] !== 'undefined'; })
        .map(function (row) { return row[CHART_KEY]; })));
    return new Set(limit <= 0 ? orderedData : orderedData.slice(0, limit));
}
function getDataWithKeys(data, query, options) {
    if (options === void 0) { options = {}; }
    var aggregations = query.aggregations, fields = query.fields;
    // We only chart the first aggregation for now
    var aggregate = aggregations[0][2];
    return data.map(function (row) {
        var _a;
        // `row` can be an empty time bucket, in which case it has no value
        // for `aggregate`
        if (!row.hasOwnProperty(aggregate)) {
            return row;
        }
        var key = fields.length
            ? fields.map(function (field) { return getLabel(row[field], options); }).join(',')
            : aggregate;
        return __assign(__assign({}, row), (_a = {}, _a[CHART_KEY] = key, _a));
    });
}
function formatDate(datetime) {
    return datetime * 1000;
}
// Converts a value to a string for the chart label. This could
// potentially cause incorrect grouping, e.g. if the value null and string
// 'null' are both present in the same series they will be merged into 1 value
function getLabel(value, options) {
    if (typeof value === 'object') {
        try {
            value = JSON.stringify(value);
        }
        catch (err) {
            // eslint-disable-next-line no-console
            console.error(err);
        }
    }
    if (options.fieldLabelMap && options.fieldLabelMap.hasOwnProperty(value)) {
        return options.fieldLabelMap[value];
    }
    return options.formatVersion && typeof value === 'string'
        ? formatVersion(value, true)
        : value;
}
/**
 * Takes any value and returns a display version of that value for rendering in
 * the "discover" result table. Only expected to handle the 4 types that we
 * would expect to be present in Snuba data - string, number, null and array
 *
 * @param val Value to display in table cell
 * @param idx Index if part of array
 * @returns Formatted cell contents
 */
export function getDisplayValue(val, idx) {
    if (typeof val === 'string') {
        return <DarkGray key={idx}>{"\"" + val + "\""}</DarkGray>;
    }
    if (typeof val === 'number') {
        return <span>{val.toLocaleString()}</span>;
    }
    if (val === null) {
        return <LightGray key={idx}>null</LightGray>;
    }
    if (Array.isArray(val)) {
        return (<span>
        [
        {val.map(getDisplayValue).reduce(function (acc, curr, arrayIdx) {
            if (arrayIdx !== 0) {
                return __spread(acc, [',', curr]);
            }
            return __spread(acc, [curr]);
        }, [])}
        ]
      </span>);
    }
    return <span>{val}</span>;
}
/**
 * Takes any value and returns the text-only version of that value that will be
 * rendered in the table. Only expected to handle the 4 types that we would
 * expect to be present in Snuba data - string, number, null and array. This
 * function is required for dynamically calculating column width based on cell
 * contents.
 *
 * @param {*} val Value to display in table cell
 * @returns {String} Cell contents as string
 */
export function getDisplayText(val) {
    if (typeof val === 'string') {
        return "\"" + val + "\"";
    }
    if (typeof val === 'number') {
        return val.toLocaleString();
    }
    if (val === null) {
        return 'null';
    }
    if (Array.isArray(val)) {
        return "[" + val.map(getDisplayText) + "]";
    }
    return "" + val;
}
var LightGray = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
var DarkGray = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
/**
 * Downloads a Snuba result object as CSV format
 *
 * @param {Object} result Result received from Snuba
 * @param {Object} result.data Result data object from Snuba
 * @param {String} result.meta Result metadata from Snuba
 * @returns {Void}
 */
export function downloadAsCsv(result) {
    var meta = result.meta, data = result.data;
    var headings = meta.map(function (_a) {
        var name = _a.name;
        return name;
    });
    var csvContent = Papa.unparse({
        fields: headings,
        data: data.map(function (row) { return headings.map(function (col) { return disableMacros(row[col]); }); }),
    });
    // Need to also manually replace # since encodeURI skips them
    var encodedDataUrl = "data:text/csv;charset=utf8," + encodeURIComponent(csvContent);
    window.location.assign(encodedDataUrl);
}
export function disableMacros(value) {
    var unsafeCharacterRegex = /^[\=\+\-\@]/;
    if (typeof value === 'string' && ("" + value).match(unsafeCharacterRegex)) {
        return "'" + value;
    }
    return value;
}
var templateObject_1, templateObject_2;
//# sourceMappingURL=utils.jsx.map