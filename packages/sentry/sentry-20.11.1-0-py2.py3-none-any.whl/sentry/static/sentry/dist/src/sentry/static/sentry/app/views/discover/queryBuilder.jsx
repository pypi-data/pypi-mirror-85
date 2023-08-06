import { __assign, __read, __spread } from "tslib";
import React from 'react';
import uniq from 'lodash/uniq';
import partition from 'lodash/partition';
import moment from 'moment-timezone';
import { Client } from 'app/api';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { openModal } from 'app/actionCreators/modal';
import ConfigStore from 'app/stores/configStore';
import MissingProjectWarningModal from './missingProjectWarningModal';
import { COLUMNS, PROMOTED_TAGS, SPECIAL_TAGS, HIDDEN_TAGS } from './data';
import { isValidAggregation } from './aggregations/utils';
var API_LIMIT = 10000;
var DEFAULTS = {
    projects: [],
    fields: ['id', 'issue', 'project.name', 'platform', 'timestamp'],
    conditions: [],
    aggregations: [],
    orderby: '-timestamp',
    limit: 1000,
};
function applyDefaults(query) {
    Object.entries(DEFAULTS).forEach(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        if (!(key in query)) {
            query[key] = value;
        }
    });
    return query;
}
/**
 * This function is responsible for storing and managing updates to query state,
 * It applies sensible defaults if query parameters are not provided on
 * initialization.
 */
export default function createQueryBuilder(initial, organization, specificProjects) {
    if (initial === void 0) { initial = {}; }
    var api = new Client();
    var query = applyDefaults(initial);
    if (!query.start && !query.end && !query.range) {
        query.range = DEFAULT_STATS_PERIOD;
    }
    var hasGlobalProjectAccess = ConfigStore.get('user').isSuperuser || organization.access.includes('org:admin');
    // TODO(lightweight-org): This needs to be refactored so that queries
    // do not depend on organization.projects
    var projectsToUse = specificProjects !== null && specificProjects !== void 0 ? specificProjects : organization.projects;
    var defaultProjects = projectsToUse.filter(function (projects) {
        return hasGlobalProjectAccess ? projects.hasAccess : projects.isMember;
    });
    var defaultProjectIds = getProjectIds(defaultProjects);
    var projectsToFetchTags = getProjectIds(hasGlobalProjectAccess ? projectsToUse : defaultProjects);
    var columns = COLUMNS.map(function (col) { return (__assign(__assign({}, col), { isTag: false })); });
    var tags = [];
    return {
        getInternal: getInternal,
        getExternal: getExternal,
        updateField: updateField,
        fetch: fetch,
        fetchWithoutLimit: fetchWithoutLimit,
        cancelRequests: cancelRequests,
        getQueryByType: getQueryByType,
        getColumns: getColumns,
        load: load,
        reset: reset,
    };
    /**
     * Loads tags keys for user's projects and updates `tags` with the result.
     * If the request fails updates `tags` to be the hardcoded list of predefined
     * promoted tags.
     *
     * @returns {Promise<Void>}
     */
    function load() {
        return fetch({
            projects: projectsToFetchTags,
            fields: ['tags_key'],
            aggregations: [['count()', null, 'count']],
            orderby: '-count',
            range: '90d',
            turbo: true,
        })
            .then(function (res) {
            tags = res.data
                .filter(function (tag) { return !HIDDEN_TAGS.includes(tag.tags_key); })
                .map(function (tag) {
                var type = SPECIAL_TAGS[tag.tags_key] || 'string';
                return { name: tag.tags_key, type: type, isTag: true };
            });
        })
            .catch(function () {
            tags = PROMOTED_TAGS.map(function (tag) {
                var type = SPECIAL_TAGS[tag] || 'string';
                return { name: tag, type: type, isTag: true };
            });
        });
    }
    /**
     * Returns the query object (internal state of the query)
     *
     * @returns {Object}
     */
    function getInternal() {
        return query;
    }
    /**
     * Returns the external representation of the query as required by Snuba.
     * Applies default projects and fields if these properties were not specified
     * by the user.
     *
     * @returns {Object}
     */
    function getExternal() {
        // Default to all projects if none is selected
        var projects = query.projects.length ? query.projects : defaultProjectIds;
        // Default to DEFAULT_STATS_PERIOD when no date range selected (either relative or absolute)
        var _a = getParams(__assign(__assign({}, query), { statsPeriod: query.range })), statsPeriod = _a.statsPeriod, start = _a.start, end = _a.end;
        var hasAbsolute = start && end;
        var daterange = __assign(__assign({}, (hasAbsolute && { start: start, end: end })), (statsPeriod && { range: statsPeriod }));
        // Default to all fields if there are none selected, and no aggregation is
        // specified
        var useDefaultFields = !query.fields.length && !query.aggregations.length;
        var fields = useDefaultFields ? getColumns().map(function (_a) {
            var name = _a.name;
            return name;
        }) : query.fields;
        // Remove orderby property if it is not set
        if (!query.orderby) {
            delete query.orderby;
        }
        return __assign(__assign(__assign({}, query), daterange), { projects: projects,
            fields: fields });
    }
    /**
     * Updates field in query to value provided. Also updates orderby and limit
     * parameters if this causes their values to become invalid.
     *
     * @param {String} field Name of field to be updated
     * @param {*} value Value to update field to
     * @returns {Void}
     */
    function updateField(field, value) {
        query[field] = value;
        // Ignore non valid aggregations (e.g. user halfway inputting data)
        var validAggregations = query.aggregations.filter(function (agg) {
            return isValidAggregation(agg, getColumns());
        });
        var orderbyField = (query.orderby || '').replace(/^-/, '');
        var hasOrderFieldInFields = getColumns().find(function (f) { return f.name === orderbyField; }) !== undefined;
        var hasOrderFieldInSelectedFields = query.fields.includes(orderbyField);
        var hasOrderFieldInAggregations = query.aggregations.some(function (agg) { return orderbyField === agg[2]; });
        var hasInvalidOrderbyField = validAggregations.length
            ? !hasOrderFieldInSelectedFields && !hasOrderFieldInAggregations
            : !hasOrderFieldInFields;
        // If orderby value becomes invalid, update it to the first valid aggregation
        if (hasInvalidOrderbyField) {
            if (validAggregations.length > 0) {
                query.orderby = "-" + validAggregations[0][2];
            }
            else {
                query.orderby = '-timestamp';
            }
        }
        // Snuba doesn't allow limit without orderby
        if (!query.orderby) {
            query.limit = null;
        }
    }
    /**
     * Fetches either the query provided as an argument or the current query state
     * if this is not provided and returns the result wrapped in a promise
     *
     * @param {Object} [data] Optional field to provide data to fetch
     * @returns {Promise<Object|Error>}
     */
    function fetch(data, cursor) {
        if (data === void 0) { data = getExternal(); }
        if (cursor === void 0) { cursor = '0:0:1'; }
        var limit = data.limit || 1000;
        var endpoint = "/organizations/" + organization.slug + "/discover/query/?per_page=" + limit + "&cursor=" + cursor;
        // Reject immediately if no projects are available
        if (!data.projects.length) {
            return Promise.reject(new Error(t('No projects selected')));
        }
        if (typeof data.limit === 'number') {
            if (data.limit < 1 || data.limit > 1000) {
                return Promise.reject(new Error(t('Invalid limit parameter')));
            }
        }
        if (moment.utc(data.start).isAfter(moment.utc(data.end))) {
            return Promise.reject(new Error('Start date cannot be after end date'));
        }
        var _a = getParams(__assign(__assign({}, data), { statsPeriod: data.range })), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        if (start && end) {
            data.start = start;
            data.end = end;
        }
        if (statsPeriod) {
            data.range = statsPeriod;
        }
        return api
            .requestPromise(endpoint, { includeAllArgs: true, method: 'POST', data: data })
            .then(function (_a) {
            var _b = __read(_a, 3), responseData = _b[0], _ = _b[1], utils = _b[2];
            responseData.pageLinks = utils.getResponseHeader('Link');
            return responseData;
        })
            .catch(function () {
            throw new Error(t('An error occurred'));
        });
    }
    /**
     * Fetches either the query provided as an argument or the current query state
     * if this is not provided and returns the result wrapped in a promise
     *
     * This is similar to `fetch` but does not support pagination and mirrors the API limit
     *
     * @param {Object} [data] Optional field to provide data to fetch
     * @returns {Promise<Object|Error>}
     */
    function fetchWithoutLimit(data) {
        if (data === void 0) { data = getExternal(); }
        var endpoint = "/organizations/" + organization.slug + "/discover/query/";
        // Reject immediately if no projects are available
        if (!data.projects.length) {
            return Promise.reject(new Error(t('No projects selected')));
        }
        if (typeof data.limit === 'number') {
            if (data.limit < 1 || data.limit > API_LIMIT) {
                return Promise.reject(new Error(t('Invalid limit parameter')));
            }
        }
        if (moment.utc(data.start).isAfter(moment.utc(data.end))) {
            return Promise.reject(new Error('Start date cannot be after end date'));
        }
        var _a = getParams(__assign(__assign({}, data), { statsPeriod: data.range })), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        if (start && end) {
            data.start = start;
            data.end = end;
        }
        if (statsPeriod) {
            data.range = statsPeriod;
        }
        return api.requestPromise(endpoint, { method: 'POST', data: data }).catch(function () {
            throw new Error(t('Error with query'));
        });
    }
    /**
     * Cancels any in-flight API requests made via `fetch` or `fetchWithoutLimit`
     *
     * @returns {Void}
     */
    function cancelRequests() {
        api.clear();
    }
    /**
     * Get the actual query to be run for each visualization type
     *
     * @param {Object} originalQuery Original query input by user (external query representation)
     * @param {String} Type to fetch - currently either byDay or base
     * @returns {Object} Modified query to be run for that type
     */
    function getQueryByType(originalQuery, type) {
        if (type === 'byDayQuery') {
            return __assign(__assign({}, originalQuery), { groupby: ['time'], rollup: 60 * 60 * 24, orderby: '-time', limit: 5000 });
        }
        // If id or issue.id is present in query fields, always fetch the project.id
        // so we can generate links
        if (type === 'baseQuery') {
            return (originalQuery.fields || []).some(function (field) { return field === 'id' || field === 'issue.id'; })
                ? __assign(__assign({}, originalQuery), { fields: uniq(__spread(originalQuery.fields, ['project.id'])) }) : originalQuery;
        }
        throw new Error('Invalid query type');
    }
    /**
     * Returns all column objects, including tags
     *
     * @returns {Array<{name: String, type: String}>}
     */
    function getColumns() {
        return __spread(columns, tags);
    }
    /**
     * Resets the query to defaults or the query provided
     * Displays a warning if user does not have access to any project in the query
     *
     * @param {Object} [q] optional query to reset to
     * @returns {Void}
     */
    function reset(q) {
        var _a = __read(partition(q.projects || [], function (project) {
            // -1 means all projects
            return project === -1 ? true : defaultProjectIds.includes(project);
        }), 2), validProjects = _a[0], invalidProjects = _a[1];
        if (invalidProjects.length) {
            openModal(function (deps) { return (<MissingProjectWarningModal organization={organization} validProjects={validProjects} invalidProjects={invalidProjects} {...deps}/>); });
        }
        q.projects = validProjects;
        query = applyDefaults(q);
    }
}
function getProjectIds(projects) {
    return projects.map(function (project) { return parseInt(project.id, 10); });
}
//# sourceMappingURL=queryBuilder.jsx.map