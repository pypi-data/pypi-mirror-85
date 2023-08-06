import { __read, __rest, __spread } from "tslib";
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import moment from 'moment';
import * as qs from 'query-string';
import { Client } from 'app/api';
import { isValidAggregation } from './aggregations/utils';
import { NON_SNUBA_FIELDS } from './data';
var VALID_QUERY_KEYS = [
    'projects',
    'fields',
    'conditions',
    'aggregations',
    'range',
    'start',
    'end',
    'orderby',
    'limit',
];
export function getQueryFromQueryString(queryString) {
    var queryKeys = new Set(__spread(VALID_QUERY_KEYS, ['utc']));
    var result = {};
    var parsedQuery = queryString.replace(/^\?|\/$/g, '').split('&');
    parsedQuery.forEach(function (item) {
        if (item.includes('=')) {
            var _a = __read(item.split('='), 2), key = _a[0], value = _a[1];
            if (queryKeys.has(key)) {
                result[key] = JSON.parse(decodeURIComponent(value));
            }
        }
    });
    return result;
}
export function getQueryStringFromQuery(query, queryParams) {
    if (queryParams === void 0) { queryParams = {}; }
    var queryProperties = Object.entries(query).map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return key + "=" + encodeURIComponent(JSON.stringify(value));
    });
    Object.entries(queryParams).forEach(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        queryProperties.push(key + "=" + value);
    });
    return "?" + queryProperties.sort().join('&');
}
export function getOrderbyFields(queryBuilder) {
    var columns = queryBuilder.getColumns();
    var query = queryBuilder.getInternal();
    // If there are valid aggregations, only allow summarized fields and aggregations in orderby
    var validAggregations = query.aggregations.filter(function (agg) {
        return isValidAggregation(agg, columns);
    });
    var hasAggregations = validAggregations.length > 0;
    var hasFields = query.fields.length > 0;
    var columnOptions = columns.reduce(function (acc, _a) {
        var name = _a.name;
        if (hasAggregations) {
            var isInvalidField = hasFields && !query.fields.includes(name);
            if (!hasFields || isInvalidField) {
                return acc;
            }
        }
        // Never allow ordering by project.name or issue.id since this can't be done in Snuba
        if (NON_SNUBA_FIELDS.includes(name)) {
            return acc;
        }
        return __spread(acc, [{ value: name, label: name }]);
    }, []);
    var aggregationOptions = validAggregations
        .map(function (aggregation) { return aggregation[2]; })
        .reduce(function (acc, agg) { return __spread(acc, [{ value: agg, label: agg }]); }, []);
    return __spread(columnOptions, aggregationOptions);
}
/**
 * Takes the params object and the requested view querystring and returns the
 * correct view to be displayed
 */
export function getView(params, requestedView) {
    var defaultRequestedView = requestedView;
    if (typeof params.savedQueryId !== 'undefined') {
        defaultRequestedView = 'saved';
    }
    switch (defaultRequestedView) {
        case 'saved':
            return 'saved';
        default:
            return 'query';
    }
}
/**
 * Returns true if the underlying discover query has changed based on the
 * querystring, otherwise false.
 *
 * @param prev previous location.search string
 * @param next next location.search string
 */
export function queryHasChanged(prev, next) {
    return !isEqual(pick(qs.parse(prev), VALID_QUERY_KEYS), pick(qs.parse(next), VALID_QUERY_KEYS));
}
/**
 * Takes a saved query and strips associated query metadata in order to match
 * our internal representation of queries.
 */
export function parseSavedQuery(savedQuery) {
    var _id = savedQuery.id, _name = savedQuery.name, _dateCreated = savedQuery.dateCreated, _dateUpdated = savedQuery.dateUpdated, _createdBy = savedQuery.createdBy, query = __rest(savedQuery, ["id", "name", "dateCreated", "dateUpdated", "createdBy"]);
    return query;
}
export function fetchSavedQuery(organization, queryId) {
    var api = new Client();
    var endpoint = "/organizations/" + organization.slug + "/discover/saved/" + queryId + "/";
    return api.requestPromise(endpoint, {
        method: 'GET',
    }); // TODO(ts): Remove as any
}
export function fetchSavedQueries(organization) {
    var api = new Client();
    var endpoint = "/organizations/" + organization.slug + "/discover/saved/";
    return api.requestPromise(endpoint, {
        method: 'GET',
        query: { all: 1, query: 'version:1', sortBy: '-dateUpdated' },
    }); // TODO(ts): Remove as any
}
export function createSavedQuery(organization, data) {
    var api = new Client();
    var endpoint = "/organizations/" + organization.slug + "/discover/saved/";
    return api.requestPromise(endpoint, {
        data: data,
        method: 'POST',
    }); // TODO(ts): Remove as any
}
export function updateSavedQuery(organization, id, data) {
    var api = new Client();
    var endpoint = "/organizations/" + organization.slug + "/discover/saved/" + id + "/";
    return api.requestPromise(endpoint, {
        data: data,
        method: 'PUT',
    }); // TODO(ts): Remove as any
}
export function deleteSavedQuery(organization, id) {
    var api = new Client();
    var endpoint = "/organizations/" + organization.slug + "/discover/saved/" + id + "/";
    return api.requestPromise(endpoint, {
        method: 'DELETE',
    }); // TODO(ts): Remove as any
}
/**
 * Generate a saved query name based on the current timestamp
 */
export function generateQueryName() {
    return "Result - " + moment.utc().format('MMM DD HH:mm:ss');
}
//# sourceMappingURL=utils.jsx.map