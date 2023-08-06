import { __assign, __read, __spread } from "tslib";
import Papa from 'papaparse';
import { browserHistory } from 'react-router';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { t } from 'app/locale';
import { getTitle } from 'app/utils/events';
import { getUtcDateString } from 'app/utils/dates';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { disableMacros } from 'app/views/discover/result/utils';
import { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import localStorage from 'app/utils/localStorage';
import { AGGREGATIONS, FIELDS, aggregateFunctionOutputType, explodeFieldString, getAggregateAlias, TRACING_FIELDS, isMeasurement, measurementType, } from 'app/utils/discover/fields';
import { ALL_VIEWS, TRANSACTION_VIEWS, WEB_VITALS_VIEWS } from './data';
import { FieldValueKind } from './table/types';
var TEMPLATE_TABLE_COLUMN = {
    key: '',
    name: '',
    type: 'never',
    isSortable: false,
    column: Object.freeze({ kind: 'field', field: '' }),
    width: COL_WIDTH_UNDEFINED,
};
// TODO(mark) these types are coupled to the gridEditable component types and
// I'd prefer the types to be more general purpose but that will require a second pass.
export function decodeColumnOrder(fields) {
    return fields.map(function (f) {
        var column = __assign({}, TEMPLATE_TABLE_COLUMN);
        var col = explodeFieldString(f.field);
        column.key = f.field;
        column.name = f.field;
        column.width = f.width || COL_WIDTH_UNDEFINED;
        if (col.kind === 'function') {
            // Aggregations can have a strict outputType or they can inherit from their field.
            // Otherwise use the FIELDS data to infer types.
            var outputType = aggregateFunctionOutputType(col.function[0], col.function[1]);
            if (outputType !== null) {
                column.type = outputType;
            }
            var aggregate = AGGREGATIONS[col.function[0]];
            column.isSortable = aggregate && aggregate.isSortable;
        }
        else if (col.kind === 'field') {
            if (FIELDS.hasOwnProperty(col.field)) {
                column.type = FIELDS[col.field];
            }
            else if (isMeasurement(col.field)) {
                column.type = measurementType(col.field);
            }
        }
        column.column = col;
        return column;
    });
}
export function pushEventViewToLocation(props) {
    var location = props.location, nextEventView = props.nextEventView;
    var extraQuery = props.extraQuery || {};
    var queryStringObject = nextEventView.generateQueryStringObject();
    browserHistory.push(__assign(__assign({}, location), { query: __assign(__assign({}, extraQuery), queryStringObject) }));
}
export function generateTitle(_a) {
    var eventView = _a.eventView, event = _a.event, organization = _a.organization;
    var titles = [t('Discover')];
    var eventViewName = eventView.name;
    if (typeof eventViewName === 'string' && String(eventViewName).trim().length > 0) {
        titles.push(String(eventViewName).trim());
    }
    var eventTitle = event ? getTitle(event, organization).title : undefined;
    if (eventTitle) {
        titles.push(eventTitle);
    }
    titles.reverse();
    return titles.join(' - ');
}
export function getPrebuiltQueries(organization) {
    var views = __spread(ALL_VIEWS);
    if (organization.features.includes('performance-view')) {
        // insert transactions queries at index 2
        views.splice.apply(views, __spread([2, 0], TRANSACTION_VIEWS));
        views.push.apply(views, __spread(WEB_VITALS_VIEWS));
    }
    return views;
}
export function downloadAsCsv(tableData, columnOrder, filename) {
    var data = tableData.data;
    var headings = columnOrder.map(function (column) { return column.name; });
    var csvContent = Papa.unparse({
        fields: headings,
        data: data.map(function (row) {
            return headings.map(function (col) {
                col = getAggregateAlias(col);
                return disableMacros(row[col]);
            });
        }),
    });
    // Need to also manually replace # since encodeURI skips them
    var encodedDataUrl = "data:text/csv;charset=utf8," + encodeURIComponent(csvContent);
    // Create a download link then click it, this is so we can get a filename
    var link = document.createElement('a');
    var now = new Date();
    link.setAttribute('href', encodedDataUrl);
    link.setAttribute('download', filename + " " + getUtcDateString(now) + ".csv");
    link.click();
    link.remove();
    // Make testing easier
    return encodedDataUrl;
}
var ALIASED_AGGREGATES_COLUMN = {
    last_seen: 'timestamp',
};
/**
 * Convert an aggregate into the resulting column from a drilldown action.
 * The result is null if the drilldown results in the aggregate being removed.
 */
function drilldownAggregate(func) {
    var _a;
    var key = func.function[0];
    var aggregation = AGGREGATIONS[key];
    var column = func.function[1];
    if (ALIASED_AGGREGATES_COLUMN.hasOwnProperty(key)) {
        // Some aggregates are just shortcuts to other aggregates with
        // predefined arguments so we can directly map them to the result.
        column = ALIASED_AGGREGATES_COLUMN[key];
    }
    else if ((_a = aggregation === null || aggregation === void 0 ? void 0 : aggregation.parameters) === null || _a === void 0 ? void 0 : _a[0]) {
        var parameter = aggregation.parameters[0];
        if (parameter.kind !== 'column') {
            // The aggregation does not accept a column as a parameter,
            // so we clear the column.
            column = '';
        }
        else if (!column && parameter.required === false) {
            // The parameter was not given for a non-required parameter,
            // so we fall back to the default.
            column = parameter.defaultValue;
        }
    }
    else {
        // The aggregation does not exist or does not have any parameters,
        // so we clear the column.
        column = '';
    }
    return column ? { kind: 'field', field: column } : null;
}
/**
 * Convert an aggregated query into one that does not have aggregates.
 * Will also apply additions conditions defined in `additionalConditions`
 * and generate conditions based on the `dataRow` parameter and the current fields
 * in the `eventView`.
 */
export function getExpandedResults(eventView, additionalConditions, dataRow) {
    var fieldSet = new Set();
    // Expand any functions in the resulting column, and dedupe the result.
    // Mark any column as null to remove it.
    var expandedColumns = eventView.fields.map(function (field) {
        var exploded = explodeFieldString(field.field);
        var column = exploded.kind === 'function' ? drilldownAggregate(exploded) : exploded;
        if (
        // if expanding the function failed
        column === null ||
            // id is implicitly a part of all non-aggregate results
            column.field === 'id' ||
            // the new column is already present
            fieldSet.has(column.field)) {
            return null;
        }
        fieldSet.add(column.field);
        return column;
    });
    // update the columns according the the expansion above
    var nextView = expandedColumns.reduceRight(function (newView, column, index) {
        return column === null
            ? newView.withDeletedColumn(index, undefined)
            : newView.withUpdatedColumn(index, column, undefined);
    }, eventView.clone());
    nextView.query = generateExpandedConditions(nextView, additionalConditions, dataRow);
    return nextView;
}
/**
 * Create additional conditions based on the fields in an EventView
 * and a datarow/event
 */
function generateAdditionalConditions(eventView, dataRow) {
    var specialKeys = Object.values(URL_PARAM);
    var conditions = {};
    if (!dataRow) {
        return conditions;
    }
    eventView.fields.forEach(function (field) {
        var column = explodeFieldString(field.field);
        // Skip aggregate fields
        if (column.kind === 'function') {
            return;
        }
        var dataKey = getAggregateAlias(field.field);
        // Append the current field as a condition if it exists in the dataRow
        // Or is a simple key in the event. More complex deeply nested fields are
        // more challenging to get at as their location in the structure does not
        // match their name.
        if (dataRow.hasOwnProperty(dataKey)) {
            var value = dataRow[dataKey];
            // if the value will be quoted, then do not trim it as the whitespaces
            // may be important to the query and should not be trimmed
            var shouldQuote = value === null || value === undefined
                ? false
                : /[\s\(\)\\"]/g.test(String(value).trim());
            var nextValue = value === null || value === undefined
                ? ''
                : shouldQuote
                    ? String(value)
                    : String(value).trim();
            if (isMeasurement(column.field) && !nextValue) {
                // Do not add measurement conditions if nextValue is falsey.
                // It's expected that nextValue is a numeric value.
                return;
            }
            switch (column.field) {
                case 'timestamp':
                    // normalize the "timestamp" field to ensure the payload works
                    conditions[column.field] = getUtcDateString(nextValue);
                    break;
                default:
                    conditions[column.field] = nextValue;
            }
        }
        // If we have an event, check tags as well.
        if (dataRow.tags && Array.isArray(dataRow.tags)) {
            var tagIndex = dataRow.tags.findIndex(function (item) { return item.key === dataKey; });
            if (tagIndex > -1) {
                var key = specialKeys.includes(column.field)
                    ? "tags[" + column.field + "]"
                    : column.field;
                var tagValue = dataRow.tags[tagIndex].value;
                conditions[key] = tagValue;
            }
        }
    });
    return conditions;
}
function generateExpandedConditions(eventView, additionalConditions, dataRow) {
    var parsedQuery = tokenizeSearch(eventView.query);
    // Remove any aggregates from the search conditions.
    // otherwise, it'll lead to an invalid query result.
    for (var key in parsedQuery.tagValues) {
        var column = explodeFieldString(key);
        if (column.kind === 'function') {
            parsedQuery.removeTag(key);
        }
    }
    var conditions = Object.assign({}, additionalConditions, generateAdditionalConditions(eventView, dataRow));
    // Add additional conditions provided and generated.
    for (var key in conditions) {
        var value = conditions[key];
        if (key === 'project.id') {
            eventView.project = __spread(eventView.project, [parseInt(value, 10)]);
            continue;
        }
        if (key === 'environment') {
            if (!eventView.environment.includes(value)) {
                eventView.environment = __spread(eventView.environment, [value]);
            }
            continue;
        }
        var column = explodeFieldString(key);
        // Skip aggregates as they will be invalid.
        if (column.kind === 'function') {
            continue;
        }
        parsedQuery.setTagValues(key, [conditions[key]]);
    }
    return stringifyQueryObject(parsedQuery);
}
export function generateFieldOptions(_a) {
    var organization = _a.organization, tagKeys = _a.tagKeys, measurementKeys = _a.measurementKeys, _b = _a.aggregations, aggregations = _b === void 0 ? AGGREGATIONS : _b, _c = _a.fields, fields = _c === void 0 ? FIELDS : _c;
    var fieldKeys = Object.keys(fields);
    var functions = Object.keys(aggregations);
    // Strip tracing features if the org doesn't have access.
    if (!organization.features.includes('performance-view')) {
        fieldKeys = fieldKeys.filter(function (item) { return !TRACING_FIELDS.includes(item); });
        functions = functions.filter(function (item) { return !TRACING_FIELDS.includes(item); });
    }
    var fieldOptions = {};
    // Index items by prefixed keys as custom tags can overlap both fields and
    // function names. Having a mapping makes finding the value objects easier
    // later as well.
    functions.forEach(function (func) {
        var ellipsis = aggregations[func].parameters.length ? '\u2026' : '';
        var parameters = aggregations[func].parameters.map(function (param) {
            var generator = aggregations[func].generateDefaultValue;
            if (typeof generator === 'undefined') {
                return param;
            }
            return __assign(__assign({}, param), { defaultValue: generator({ parameter: param, organization: organization }) });
        });
        fieldOptions["function:" + func] = {
            label: func + "(" + ellipsis + ")",
            value: {
                kind: FieldValueKind.FUNCTION,
                meta: {
                    name: func,
                    parameters: parameters,
                },
            },
        };
    });
    fieldKeys.forEach(function (field) {
        fieldOptions["field:" + field] = {
            label: field,
            value: {
                kind: FieldValueKind.FIELD,
                meta: {
                    name: field,
                    dataType: fields[field],
                },
            },
        };
    });
    if (tagKeys !== undefined && tagKeys !== null) {
        tagKeys.forEach(function (tag) {
            var tagValue = fields.hasOwnProperty(tag) || AGGREGATIONS.hasOwnProperty(tag)
                ? "tags[" + tag + "]"
                : tag;
            fieldOptions["tag:" + tag] = {
                label: tag,
                value: {
                    kind: FieldValueKind.TAG,
                    meta: { name: tagValue, dataType: 'string' },
                },
            };
        });
    }
    if (measurementKeys !== undefined && measurementKeys !== null) {
        measurementKeys.forEach(function (measurement) {
            fieldOptions["measurement:" + measurement] = {
                label: measurement,
                value: {
                    kind: FieldValueKind.MEASUREMENT,
                    meta: { name: measurement, dataType: measurementType(measurement) },
                },
            };
        });
    }
    return fieldOptions;
}
var BANNER_DISMISSED_KEY = 'discover-banner-dismissed';
export function isBannerHidden() {
    return localStorage.getItem(BANNER_DISMISSED_KEY) === 'true';
}
export function setBannerHidden(value) {
    localStorage.setItem(BANNER_DISMISSED_KEY, value ? 'true' : 'false');
}
var RENDER_PREBUILT_KEY = 'discover-render-prebuilt';
export function shouldRenderPrebuilt() {
    var shouldRender = localStorage.getItem(RENDER_PREBUILT_KEY);
    return shouldRender === 'true' || shouldRender === null;
}
export function setRenderPrebuilt(value) {
    localStorage.setItem(RENDER_PREBUILT_KEY, value ? 'true' : 'false');
}
//# sourceMappingURL=utils.jsx.map