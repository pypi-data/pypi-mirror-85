import { __assign, __read, __spread, __values } from "tslib";
import isString from 'lodash/isString';
import cloneDeep from 'lodash/cloneDeep';
import pick from 'lodash/pick';
import isEqual from 'lodash/isEqual';
import omit from 'lodash/omit';
import uniqBy from 'lodash/uniqBy';
import moment from 'moment';
import { DEFAULT_PER_PAGE } from 'app/constants';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import { decodeColumnOrder } from 'app/views/eventsV2/utils';
import { decodeScalar, decodeList } from 'app/utils/queryString';
import { isAggregateField, getAggregateAlias, generateFieldAsString, } from './fields';
import { getSortField } from './fieldRenderers';
import { CHART_AXIS_OPTIONS, DisplayModes, DISPLAY_MODE_OPTIONS, DISPLAY_MODE_FALLBACK_OPTIONS, } from './types';
import { statsPeriodToDays } from '../dates';
var DATETIME_QUERY_STRING_KEYS = ['start', 'end', 'utc', 'statsPeriod'];
var EXTERNAL_QUERY_STRING_KEYS = __spread(DATETIME_QUERY_STRING_KEYS, [
    'cursor',
]);
var setSortOrder = function (sort, kind) { return ({
    kind: kind,
    field: sort.field,
}); };
var reverseSort = function (sort) { return ({
    kind: sort.kind === 'desc' ? 'asc' : 'desc',
    field: sort.field,
}); };
var isSortEqualToField = function (sort, field, tableMeta) {
    var sortKey = getSortKeyFromField(field, tableMeta);
    return sort.field === sortKey;
};
var fieldToSort = function (field, tableMeta, kind) {
    var sortKey = getSortKeyFromField(field, tableMeta);
    if (!sortKey) {
        return void 0;
    }
    return {
        kind: kind || 'desc',
        field: sortKey,
    };
};
function getSortKeyFromField(field, tableMeta) {
    var alias = getAggregateAlias(field.field);
    return getSortField(alias, tableMeta);
}
export function isFieldSortable(field, tableMeta) {
    return !!getSortKeyFromField(field, tableMeta);
}
var decodeFields = function (location) {
    var query = location.query;
    if (!query || !query.field) {
        return [];
    }
    var fields = decodeList(query.field) || [];
    var widths = decodeList(query.widths) || [];
    var parsed = [];
    fields.forEach(function (field, i) {
        var w = Number(widths[i]);
        var width = !isNaN(w) ? w : COL_WIDTH_UNDEFINED;
        parsed.push({ field: field, width: width });
    });
    return parsed;
};
var parseSort = function (sort) {
    sort = sort.trim();
    if (sort.startsWith('-')) {
        return {
            kind: 'desc',
            field: sort.substring(1),
        };
    }
    return {
        kind: 'asc',
        field: sort,
    };
};
var fromSorts = function (sorts) {
    if (sorts === undefined) {
        return [];
    }
    sorts = isString(sorts) ? [sorts] : sorts;
    // NOTE: sets are iterated in insertion order
    var uniqueSorts = __spread(new Set(sorts));
    return uniqueSorts.reduce(function (acc, sort) {
        acc.push(parseSort(sort));
        return acc;
    }, []);
};
var decodeSorts = function (location) {
    var query = location.query;
    if (!query || !query.sort) {
        return [];
    }
    var sorts = decodeList(query.sort);
    return fromSorts(sorts);
};
var encodeSort = function (sort) {
    switch (sort.kind) {
        case 'desc': {
            return "-" + sort.field;
        }
        case 'asc': {
            return String(sort.field);
        }
        default: {
            throw new Error('Unexpected sort type');
        }
    }
};
var encodeSorts = function (sorts) {
    return sorts.map(encodeSort);
};
var collectQueryStringByKey = function (query, key) {
    var needle = query[key];
    var collection = decodeList(needle) || [];
    return collection.reduce(function (acc, item) {
        item = item.trim();
        if (item.length > 0) {
            acc.push(item);
        }
        return acc;
    }, []);
};
var decodeQuery = function (location) {
    if (!location.query || !location.query.query) {
        return undefined;
    }
    var queryParameter = location.query.query;
    var query = decodeScalar(queryParameter);
    return isString(query) ? query.trim() : undefined;
};
var decodeProjects = function (location) {
    if (!location.query || !location.query.project) {
        return [];
    }
    var value = location.query.project;
    return Array.isArray(value) ? value.map(function (i) { return parseInt(i, 10); }) : [parseInt(value, 10)];
};
var queryStringFromSavedQuery = function (saved) {
    if (saved.query) {
        return saved.query || '';
    }
    return '';
};
function validateTableMeta(tableMeta) {
    return tableMeta && Object.keys(tableMeta).length > 0 ? tableMeta : undefined;
}
var EventView = /** @class */ (function () {
    function EventView(props) {
        var fields = Array.isArray(props.fields) ? props.fields : [];
        var sorts = Array.isArray(props.sorts) ? props.sorts : [];
        var project = Array.isArray(props.project) ? props.project : [];
        var environment = Array.isArray(props.environment) ? props.environment : [];
        // only include sort keys that are included in the fields
        var sortKeys = fields
            .map(function (field) { return getSortKeyFromField(field, undefined); })
            .filter(function (sortKey) { return !!sortKey; });
        var sort = sorts.find(function (currentSort) { return sortKeys.includes(currentSort.field); });
        sorts = sort ? [sort] : [];
        var id = props.id !== null && props.id !== void 0 ? String(props.id) : void 0;
        this.id = id;
        this.name = props.name;
        this.fields = fields;
        this.sorts = sorts;
        this.query = typeof props.query === 'string' ? props.query : '';
        this.project = project;
        this.start = props.start;
        this.end = props.end;
        this.statsPeriod = props.statsPeriod;
        this.environment = environment;
        this.yAxis = props.yAxis;
        this.display = props.display;
        this.interval = props.interval;
        this.createdBy = props.createdBy;
    }
    EventView.fromLocation = function (location) {
        var _a = getParams(location.query), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        return new EventView({
            id: decodeScalar(location.query.id),
            name: decodeScalar(location.query.name),
            fields: decodeFields(location),
            sorts: decodeSorts(location),
            query: decodeQuery(location) || '',
            project: decodeProjects(location),
            start: decodeScalar(start),
            end: decodeScalar(end),
            statsPeriod: decodeScalar(statsPeriod),
            environment: collectQueryStringByKey(location.query, 'environment'),
            yAxis: decodeScalar(location.query.yAxis),
            display: decodeScalar(location.query.display),
            interval: decodeScalar(location.query.interval),
            createdBy: undefined,
        });
    };
    EventView.fromNewQueryWithLocation = function (newQuery, location) {
        var query = location.query;
        // apply global selection header values from location whenever possible
        var environment = Array.isArray(newQuery.environment) && newQuery.environment.length > 0
            ? newQuery.environment
            : collectQueryStringByKey(query, 'environment');
        var project = Array.isArray(newQuery.projects) && newQuery.projects.length > 0
            ? newQuery.projects
            : decodeProjects(location);
        var saved = __assign(__assign({}, newQuery), { environment: environment, projects: project, 
            // datetime selection
            start: newQuery.start || decodeScalar(query.start), end: newQuery.end || decodeScalar(query.end), range: newQuery.range || decodeScalar(query.statsPeriod) });
        return EventView.fromSavedQuery(saved);
    };
    EventView.fromSavedQuery = function (saved) {
        var fields = saved.fields.map(function (field, i) {
            var width = saved.widths && saved.widths[i] ? Number(saved.widths[i]) : COL_WIDTH_UNDEFINED;
            return { field: field, width: width };
        });
        // normalize datetime selection
        var _a = getParams({
            start: saved.start,
            end: saved.end,
            statsPeriod: saved.range,
        }), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        return new EventView({
            id: saved.id,
            name: saved.name,
            fields: fields,
            query: queryStringFromSavedQuery(saved),
            project: saved.projects,
            start: decodeScalar(start),
            end: decodeScalar(end),
            statsPeriod: decodeScalar(statsPeriod),
            sorts: fromSorts(saved.orderby),
            environment: collectQueryStringByKey({
                environment: saved.environment,
            }, 'environment'),
            yAxis: saved.yAxis,
            display: saved.display,
            createdBy: saved.createdBy,
        });
    };
    EventView.prototype.isEqualTo = function (other) {
        var e_1, _a, e_2, _b;
        var keys = [
            'id',
            'name',
            'query',
            'statsPeriod',
            'fields',
            'sorts',
            'project',
            'environment',
            'yAxis',
            'display',
        ];
        try {
            for (var keys_1 = __values(keys), keys_1_1 = keys_1.next(); !keys_1_1.done; keys_1_1 = keys_1.next()) {
                var key = keys_1_1.value;
                var currentValue = this[key];
                var otherValue = other[key];
                if (!isEqual(currentValue, otherValue)) {
                    return false;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (keys_1_1 && !keys_1_1.done && (_a = keys_1.return)) _a.call(keys_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        // compare datetime selections using moment
        var dateTimeKeys = ['start', 'end'];
        try {
            for (var dateTimeKeys_1 = __values(dateTimeKeys), dateTimeKeys_1_1 = dateTimeKeys_1.next(); !dateTimeKeys_1_1.done; dateTimeKeys_1_1 = dateTimeKeys_1.next()) {
                var key = dateTimeKeys_1_1.value;
                var currentValue = this[key];
                var otherValue = other[key];
                if (currentValue && otherValue) {
                    var currentDateTime = moment.utc(currentValue);
                    var othereDateTime = moment.utc(otherValue);
                    if (!currentDateTime.isSame(othereDateTime)) {
                        return false;
                    }
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (dateTimeKeys_1_1 && !dateTimeKeys_1_1.done && (_b = dateTimeKeys_1.return)) _b.call(dateTimeKeys_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return true;
    };
    EventView.prototype.toNewQuery = function () {
        var orderby = this.sorts.length > 0 ? encodeSorts(this.sorts)[0] : undefined;
        var newQuery = {
            version: 2,
            id: this.id,
            name: this.name || '',
            fields: this.getFields(),
            widths: this.getWidths().map(function (w) { return String(w); }),
            orderby: orderby,
            query: this.query || '',
            projects: this.project,
            start: this.start,
            end: this.end,
            range: this.statsPeriod,
            environment: this.environment,
            yAxis: this.yAxis,
            display: this.display,
        };
        if (!newQuery.query) {
            // if query is an empty string, then it cannot be saved, so we omit it
            // from the payload
            delete newQuery.query;
        }
        return newQuery;
    };
    EventView.prototype.getGlobalSelection = function () {
        var _a, _b, _c;
        return {
            projects: this.project,
            environments: this.environment,
            datetime: {
                start: (_a = this.start) !== null && _a !== void 0 ? _a : null,
                end: (_b = this.end) !== null && _b !== void 0 ? _b : null,
                period: (_c = this.statsPeriod) !== null && _c !== void 0 ? _c : '',
                // TODO(tony) Add support for the Use UTC option from
                // the global headers, currently, that option is not
                // supported and all times are assumed to be UTC
                utc: true,
            },
        };
    };
    EventView.prototype.getGlobalSelectionQuery = function () {
        var _a = this.getGlobalSelection(), environment = _a.environments, projects = _a.projects, _b = _a.datetime, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc;
        return {
            project: projects.map(function (proj) { return proj.toString(); }),
            environment: environment,
            utc: utc ? 'true' : 'false',
            // since these values are from `getGlobalSelection`
            // we know they have type `string | null`
            start: (start !== null && start !== void 0 ? start : undefined),
            end: (end !== null && end !== void 0 ? end : undefined),
            // we can't use the ?? operator here as we want to
            // convert the empty string to undefined
            statsPeriod: period ? period : undefined,
        };
    };
    EventView.prototype.generateBlankQueryStringObject = function () {
        var e_3, _a;
        var output = {
            id: undefined,
            name: undefined,
            field: undefined,
            widths: undefined,
            sort: undefined,
            tag: undefined,
            query: undefined,
            yAxis: undefined,
            display: undefined,
            interval: undefined,
        };
        try {
            for (var EXTERNAL_QUERY_STRING_KEYS_1 = __values(EXTERNAL_QUERY_STRING_KEYS), EXTERNAL_QUERY_STRING_KEYS_1_1 = EXTERNAL_QUERY_STRING_KEYS_1.next(); !EXTERNAL_QUERY_STRING_KEYS_1_1.done; EXTERNAL_QUERY_STRING_KEYS_1_1 = EXTERNAL_QUERY_STRING_KEYS_1.next()) {
                var field = EXTERNAL_QUERY_STRING_KEYS_1_1.value;
                output[field] = undefined;
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (EXTERNAL_QUERY_STRING_KEYS_1_1 && !EXTERNAL_QUERY_STRING_KEYS_1_1.done && (_a = EXTERNAL_QUERY_STRING_KEYS_1.return)) _a.call(EXTERNAL_QUERY_STRING_KEYS_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return output;
    };
    EventView.prototype.generateQueryStringObject = function () {
        var e_4, _a;
        var output = {
            id: this.id,
            name: this.name,
            field: this.getFields(),
            widths: this.getWidths(),
            sort: encodeSorts(this.sorts),
            environment: this.environment,
            project: this.project,
            query: this.query,
            yAxis: this.yAxis,
            display: this.display,
            interval: this.interval,
        };
        try {
            for (var EXTERNAL_QUERY_STRING_KEYS_2 = __values(EXTERNAL_QUERY_STRING_KEYS), EXTERNAL_QUERY_STRING_KEYS_2_1 = EXTERNAL_QUERY_STRING_KEYS_2.next(); !EXTERNAL_QUERY_STRING_KEYS_2_1.done; EXTERNAL_QUERY_STRING_KEYS_2_1 = EXTERNAL_QUERY_STRING_KEYS_2.next()) {
                var field = EXTERNAL_QUERY_STRING_KEYS_2_1.value;
                if (this[field] && this[field].length) {
                    output[field] = this[field];
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (EXTERNAL_QUERY_STRING_KEYS_2_1 && !EXTERNAL_QUERY_STRING_KEYS_2_1.done && (_a = EXTERNAL_QUERY_STRING_KEYS_2.return)) _a.call(EXTERNAL_QUERY_STRING_KEYS_2);
            }
            finally { if (e_4) throw e_4.error; }
        }
        return cloneDeep(output);
    };
    EventView.prototype.isValid = function () {
        return this.fields.length > 0;
    };
    EventView.prototype.getWidths = function () {
        return this.fields.map(function (field) { return (field.width ? field.width : COL_WIDTH_UNDEFINED); });
    };
    EventView.prototype.getFields = function () {
        return this.fields.map(function (field) { return field.field; });
    };
    EventView.prototype.getAggregateFields = function () {
        return this.fields.filter(function (field) { return isAggregateField(field.field); });
    };
    EventView.prototype.hasAggregateField = function () {
        return this.fields.some(function (field) { return isAggregateField(field.field); });
    };
    EventView.prototype.hasIdField = function () {
        return this.fields.some(function (field) { return field.field === 'id'; });
    };
    EventView.prototype.numOfColumns = function () {
        return this.fields.length;
    };
    EventView.prototype.getColumns = function () {
        return decodeColumnOrder(this.fields);
    };
    EventView.prototype.getDays = function () {
        var statsPeriod = decodeScalar(this.statsPeriod);
        return statsPeriodToDays(statsPeriod, this.start, this.end);
    };
    EventView.prototype.clone = function () {
        // NOTE: We rely on usage of Readonly from TypeScript to ensure we do not mutate
        //       the attributes of EventView directly. This enables us to quickly
        //       clone new instances of EventView.
        return new EventView({
            id: this.id,
            name: this.name,
            fields: this.fields,
            sorts: this.sorts,
            query: this.query,
            project: this.project,
            start: this.start,
            end: this.end,
            statsPeriod: this.statsPeriod,
            environment: this.environment,
            yAxis: this.yAxis,
            display: this.display,
            interval: this.interval,
            createdBy: this.createdBy,
        });
    };
    EventView.prototype.withSorts = function (sorts) {
        var newEventView = this.clone();
        var fields = newEventView.fields.map(function (field) { return getAggregateAlias(field.field); });
        newEventView.sorts = sorts.filter(function (sort) { return fields.includes(sort.field); });
        return newEventView;
    };
    EventView.prototype.withColumns = function (columns) {
        var newEventView = this.clone();
        var fields = columns
            .filter(function (col) {
            return (col.kind === 'field' && col.field) ||
                (col.kind === 'function' && col.function[0]);
        })
            .map(function (col) { return generateFieldAsString(col); })
            .map(function (field, i) {
            // newly added field
            if (!newEventView.fields[i]) {
                return { field: field, width: COL_WIDTH_UNDEFINED };
            }
            // Existing columns that were not re ordered should retain
            // their old widths.
            var existing = newEventView.fields[i];
            var width = existing.field === field && existing.width !== undefined
                ? existing.width
                : COL_WIDTH_UNDEFINED;
            return { field: field, width: width };
        });
        newEventView.fields = fields;
        // Update sorts as sorted fields may have been removed.
        if (newEventView.sorts) {
            // Filter the sort fields down to those that are still selected.
            var sortKeys_1 = fields.map(function (field) { var _a; return (_a = fieldToSort(field, undefined)) === null || _a === void 0 ? void 0 : _a.field; });
            var newSort = newEventView.sorts.filter(function (sort) { return sort && sortKeys_1.includes(sort.field); });
            // If the sort field was removed, try and find a new sortable column.
            if (newSort.length === 0) {
                var sortField = fields.find(function (field) { return isFieldSortable(field, undefined); });
                if (sortField) {
                    newSort.push({ field: sortField.field, kind: 'desc' });
                }
            }
            newEventView.sorts = newSort;
        }
        return newEventView;
    };
    EventView.prototype.withNewColumn = function (newColumn) {
        var fieldAsString = generateFieldAsString(newColumn);
        var newField = {
            field: fieldAsString,
            width: COL_WIDTH_UNDEFINED,
        };
        var newEventView = this.clone();
        newEventView.fields = __spread(newEventView.fields, [newField]);
        return newEventView;
    };
    EventView.prototype.withResizedColumn = function (columnIndex, newWidth) {
        var field = this.fields[columnIndex];
        var newEventView = this.clone();
        if (!field) {
            return newEventView;
        }
        var updateWidth = field.width !== newWidth;
        if (updateWidth) {
            var fields = __spread(newEventView.fields);
            fields[columnIndex] = __assign(__assign({}, field), { width: newWidth });
            newEventView.fields = fields;
        }
        return newEventView;
    };
    EventView.prototype.withUpdatedColumn = function (columnIndex, updatedColumn, tableMeta) {
        var columnToBeUpdated = this.fields[columnIndex];
        var fieldAsString = generateFieldAsString(updatedColumn);
        var updateField = columnToBeUpdated.field !== fieldAsString;
        if (!updateField) {
            return this;
        }
        // ensure tableMeta is non-empty
        tableMeta = validateTableMeta(tableMeta);
        var newEventView = this.clone();
        var updatedField = {
            field: fieldAsString,
            width: COL_WIDTH_UNDEFINED,
        };
        var fields = __spread(newEventView.fields);
        fields[columnIndex] = updatedField;
        newEventView.fields = fields;
        // if the updated column is one of the sorted columns, we may need to remove
        // it from the list of sorts
        var needleSortIndex = this.sorts.findIndex(function (sort) {
            return isSortEqualToField(sort, columnToBeUpdated, tableMeta);
        });
        if (needleSortIndex >= 0) {
            var needleSort_1 = this.sorts[needleSortIndex];
            var numOfColumns = this.fields.reduce(function (sum, currentField) {
                if (isSortEqualToField(needleSort_1, currentField, tableMeta)) {
                    return sum + 1;
                }
                return sum;
            }, 0);
            // do not bother deleting the sort key if there are more than one columns
            // of it in the table.
            if (numOfColumns <= 1) {
                if (isFieldSortable(updatedField, tableMeta)) {
                    // use the current updated field as the sort key
                    var sort = fieldToSort(updatedField, tableMeta);
                    // preserve the sort kind
                    sort.kind = needleSort_1.kind;
                    var sorts = __spread(newEventView.sorts);
                    sorts[needleSortIndex] = sort;
                    newEventView.sorts = sorts;
                }
                else {
                    var sorts = __spread(newEventView.sorts);
                    sorts.splice(needleSortIndex, 1);
                    newEventView.sorts = __spread(new Set(sorts));
                }
            }
            if (newEventView.sorts.length <= 0 && newEventView.fields.length > 0) {
                // establish a default sort by finding the first sortable field
                if (isFieldSortable(updatedField, tableMeta)) {
                    // use the current updated field as the sort key
                    var sort = fieldToSort(updatedField, tableMeta);
                    // preserve the sort kind
                    sort.kind = needleSort_1.kind;
                    newEventView.sorts = [sort];
                }
                else {
                    var sortableFieldIndex = newEventView.fields.findIndex(function (currentField) {
                        return isFieldSortable(currentField, tableMeta);
                    });
                    if (sortableFieldIndex >= 0) {
                        var fieldToBeSorted = newEventView.fields[sortableFieldIndex];
                        var sort = fieldToSort(fieldToBeSorted, tableMeta);
                        newEventView.sorts = [sort];
                    }
                }
            }
        }
        return newEventView;
    };
    EventView.prototype.withDeletedColumn = function (columnIndex, tableMeta) {
        // Disallow removal of the orphan column, and check for out-of-bounds
        if (this.fields.length <= 1 || this.fields.length <= columnIndex || columnIndex < 0) {
            return this;
        }
        // ensure tableMeta is non-empty
        tableMeta = validateTableMeta(tableMeta);
        // delete the column
        var newEventView = this.clone();
        var fields = __spread(newEventView.fields);
        fields.splice(columnIndex, 1);
        newEventView.fields = fields;
        // Ensure there is at least one auto width column
        // To ensure a well formed table results.
        var hasAutoIndex = fields.find(function (field) { return field.width === COL_WIDTH_UNDEFINED; });
        if (!hasAutoIndex) {
            newEventView.fields[0].width = COL_WIDTH_UNDEFINED;
        }
        // if the deleted column is one of the sorted columns, we need to remove
        // it from the list of sorts
        var columnToBeDeleted = this.fields[columnIndex];
        var needleSortIndex = this.sorts.findIndex(function (sort) {
            return isSortEqualToField(sort, columnToBeDeleted, tableMeta);
        });
        if (needleSortIndex >= 0) {
            var needleSort_2 = this.sorts[needleSortIndex];
            var numOfColumns = this.fields.reduce(function (sum, field) {
                if (isSortEqualToField(needleSort_2, field, tableMeta)) {
                    return sum + 1;
                }
                return sum;
            }, 0);
            // do not bother deleting the sort key if there are more than one columns
            // of it in the table.
            if (numOfColumns <= 1) {
                var sorts = __spread(newEventView.sorts);
                sorts.splice(needleSortIndex, 1);
                newEventView.sorts = __spread(new Set(sorts));
                if (newEventView.sorts.length <= 0 && newEventView.fields.length > 0) {
                    // establish a default sort by finding the first sortable field
                    var sortableFieldIndex = newEventView.fields.findIndex(function (field) {
                        return isFieldSortable(field, tableMeta);
                    });
                    if (sortableFieldIndex >= 0) {
                        var fieldToBeSorted = newEventView.fields[sortableFieldIndex];
                        var sort = fieldToSort(fieldToBeSorted, tableMeta);
                        newEventView.sorts = [sort];
                    }
                }
            }
        }
        return newEventView;
    };
    EventView.prototype.getSorts = function () {
        return this.sorts.map(function (sort) {
            return ({
                key: sort.field,
                order: sort.kind,
            });
        });
    };
    // returns query input for the search
    EventView.prototype.getQuery = function (inputQuery) {
        var queryParts = [];
        if (this.query) {
            queryParts.push(this.query);
        }
        if (inputQuery) {
            // there may be duplicate query in the query string
            // e.g. query=hello&query=world
            if (Array.isArray(inputQuery)) {
                inputQuery.forEach(function (query) {
                    if (typeof query === 'string' && !queryParts.includes(query)) {
                        queryParts.push(query);
                    }
                });
            }
            if (typeof inputQuery === 'string' && !queryParts.includes(inputQuery)) {
                queryParts.push(inputQuery);
            }
        }
        return queryParts.join(' ');
    };
    EventView.prototype.getFacetsAPIPayload = function (location) {
        var e_5, _a;
        var payload = this.getEventsAPIPayload(location);
        var remove = ['id', 'name', 'per_page', 'sort', 'cursor', 'field', 'interval'];
        try {
            for (var remove_1 = __values(remove), remove_1_1 = remove_1.next(); !remove_1_1.done; remove_1_1 = remove_1.next()) {
                var key = remove_1_1.value;
                delete payload[key];
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (remove_1_1 && !remove_1_1.done && (_a = remove_1.return)) _a.call(remove_1);
            }
            finally { if (e_5) throw e_5.error; }
        }
        return payload;
    };
    // Takes an EventView instance and converts it into the format required for the events API
    EventView.prototype.getEventsAPIPayload = function (location) {
        var query = (location && location.query) || {};
        // pick only the query strings that we care about
        var picked = pickRelevantLocationQueryStrings(location);
        var hasDateSelection = this.statsPeriod || (this.start && this.end);
        // an eventview's date selection has higher precedence than the date selection in the query string
        var dateSelection = hasDateSelection
            ? {
                start: this.start,
                end: this.end,
                statsPeriod: this.statsPeriod,
            }
            : {
                start: picked.start,
                end: picked.end,
                period: decodeScalar(query.period),
                statsPeriod: picked.statsPeriod,
            };
        // normalize datetime selection
        var normalizedTimeWindowParams = getParams(__assign(__assign({}, dateSelection), { utc: decodeScalar(query.utc) }));
        var sort = this.sorts.length <= 0
            ? undefined
            : this.sorts.length > 1
                ? encodeSorts(this.sorts)
                : encodeSort(this.sorts[0]);
        var fields = this.getFields();
        var project = this.project.map(function (proj) { return String(proj); });
        var environment = this.environment;
        // generate event query
        var eventQuery = Object.assign(omit(picked, DATETIME_QUERY_STRING_KEYS), normalizedTimeWindowParams, {
            project: project,
            environment: environment,
            field: __spread(new Set(fields)),
            sort: sort,
            per_page: DEFAULT_PER_PAGE,
            query: this.query,
        });
        if (!eventQuery.sort) {
            delete eventQuery.sort;
        }
        return eventQuery;
    };
    EventView.prototype.getResultsViewUrlTarget = function (slug) {
        return {
            pathname: "/organizations/" + slug + "/discover/results/",
            query: this.generateQueryStringObject(),
        };
    };
    EventView.prototype.sortForField = function (field, tableMeta) {
        if (!tableMeta) {
            return undefined;
        }
        return this.sorts.find(function (sort) { return isSortEqualToField(sort, field, tableMeta); });
    };
    EventView.prototype.sortOnField = function (field, tableMeta, kind) {
        // check if field can be sorted
        if (!isFieldSortable(field, tableMeta)) {
            return this;
        }
        var needleIndex = this.sorts.findIndex(function (sort) {
            return isSortEqualToField(sort, field, tableMeta);
        });
        if (needleIndex >= 0) {
            var newEventView_1 = this.clone();
            var currentSort = this.sorts[needleIndex];
            var sorts = __spread(newEventView_1.sorts);
            sorts[needleIndex] = kind
                ? setSortOrder(currentSort, kind)
                : reverseSort(currentSort);
            newEventView_1.sorts = sorts;
            return newEventView_1;
        }
        // field is currently not sorted; so, we sort on it
        var newEventView = this.clone();
        // invariant: this is not falsey, since sortKey exists
        var sort = fieldToSort(field, tableMeta, kind);
        newEventView.sorts = [sort];
        return newEventView;
    };
    EventView.prototype.getYAxisOptions = function () {
        // Make option set and add the default options in.
        return uniqBy(this.getAggregateFields()
            // Exclude last_seen and latest_event as they don't produce useful graphs.
            .filter(function (field) {
            return ['last_seen()', 'latest_event()'].includes(field.field) === false;
        })
            .map(function (field) { return ({ label: field.field, value: field.field }); })
            .concat(CHART_AXIS_OPTIONS), 'value');
    };
    EventView.prototype.getYAxis = function () {
        var yAxisOptions = this.getYAxisOptions();
        var yAxis = this.yAxis;
        var defaultOption = yAxisOptions[0].value;
        if (!yAxis) {
            return defaultOption;
        }
        // ensure current selected yAxis is one of the items in yAxisOptions
        var result = yAxisOptions.findIndex(function (option) { return option.value === yAxis; });
        if (result >= 0) {
            return yAxis;
        }
        return defaultOption;
    };
    EventView.prototype.getDisplayOptions = function () {
        var _this = this;
        return DISPLAY_MODE_OPTIONS.map(function (item) {
            if (item.value === DisplayModes.PREVIOUS) {
                if (_this.start || _this.end) {
                    return __assign(__assign({}, item), { disabled: true });
                }
            }
            if (item.value === DisplayModes.TOP5 || item.value === DisplayModes.DAILYTOP5) {
                if (_this.getAggregateFields().length === 0) {
                    return __assign(__assign({}, item), { disabled: true });
                }
            }
            if (item.value === DisplayModes.DAILY || item.value === DisplayModes.DAILYTOP5) {
                if (_this.getDays() < 1) {
                    return __assign(__assign({}, item), { disabled: true });
                }
            }
            return item;
        });
    };
    EventView.prototype.getDisplayMode = function () {
        var _a;
        var mode = (_a = this.display) !== null && _a !== void 0 ? _a : DisplayModes.DEFAULT;
        var displayOptions = this.getDisplayOptions();
        var display = Object.values(DisplayModes).includes(mode)
            ? mode
            : DisplayModes.DEFAULT;
        var cond = function (option) { return option.value === display; };
        // Just in case we define a fallback chain that results in an infinite loop.
        // The number 5 isn't anything special, its just larger than the longest fallback
        // chain that exists and isn't too big.
        for (var i = 0; i < 5; i++) {
            var selectedOption = displayOptions.find(cond);
            if (selectedOption && !selectedOption.disabled) {
                return display;
            }
            display = DISPLAY_MODE_FALLBACK_OPTIONS[display];
        }
        // after trying to find an enabled display mode and failing to find one,
        // we just use the default display mode
        return DisplayModes.DEFAULT;
    };
    return EventView;
}());
export var isAPIPayloadSimilar = function (current, other) {
    var e_6, _a;
    var currentKeys = new Set(Object.keys(current));
    var otherKeys = new Set(Object.keys(other));
    if (!isEqual(currentKeys, otherKeys)) {
        return false;
    }
    try {
        for (var currentKeys_1 = __values(currentKeys), currentKeys_1_1 = currentKeys_1.next(); !currentKeys_1_1.done; currentKeys_1_1 = currentKeys_1.next()) {
            var key = currentKeys_1_1.value;
            var currentValue = current[key];
            var currentTarget = Array.isArray(currentValue)
                ? new Set(currentValue)
                : currentValue;
            var otherValue = other[key];
            var otherTarget = Array.isArray(otherValue) ? new Set(otherValue) : otherValue;
            if (!isEqual(currentTarget, otherTarget)) {
                return false;
            }
        }
    }
    catch (e_6_1) { e_6 = { error: e_6_1 }; }
    finally {
        try {
            if (currentKeys_1_1 && !currentKeys_1_1.done && (_a = currentKeys_1.return)) _a.call(currentKeys_1);
        }
        finally { if (e_6) throw e_6.error; }
    }
    return true;
};
export function pickRelevantLocationQueryStrings(location) {
    var query = location.query || {};
    var picked = pick(query || {}, EXTERNAL_QUERY_STRING_KEYS);
    return picked;
}
export default EventView;
//# sourceMappingURL=eventView.jsx.map