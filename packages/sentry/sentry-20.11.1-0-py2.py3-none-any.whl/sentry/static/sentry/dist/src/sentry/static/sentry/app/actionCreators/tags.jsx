import { __assign } from "tslib";
import { t } from 'app/locale';
import TagStore from 'app/stores/tagStore';
import TagActions from 'app/actions/tagActions';
import AlertActions from 'app/actions/alertActions';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
var MAX_TAGS = 1000;
function tagFetchSuccess(tags) {
    // We occasionally get undefined passed in when APIs are having a bad time.
    tags = tags || [];
    var trimmedTags = tags.slice(0, MAX_TAGS);
    if (tags.length > MAX_TAGS) {
        AlertActions.addAlert({
            message: t('You have too many unique tags and some have been truncated'),
            type: 'warn',
        });
    }
    TagActions.loadTagsSuccess(trimmedTags);
}
/**
 * Load an organization's tags based on a global selection value.
 */
export function loadOrganizationTags(api, orgId, selection) {
    TagStore.reset();
    var url = "/organizations/" + orgId + "/tags/";
    var query = selection.datetime ? __assign({}, getParams(selection.datetime)) : {};
    query.use_cache = '1';
    if (selection.projects) {
        query.project = selection.projects.map(String);
    }
    var promise = api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
    promise.then(tagFetchSuccess, TagActions.loadTagsError);
    return promise;
}
/**
 * Fetch tags for an organization or a subset or projects.
 */
export function fetchOrganizationTags(api, orgId, projectIds) {
    if (projectIds === void 0) { projectIds = null; }
    TagStore.reset();
    var url = "/organizations/" + orgId + "/tags/";
    var query = { use_cache: '1' };
    if (projectIds) {
        query.project = projectIds;
    }
    var promise = api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
    promise.then(tagFetchSuccess, TagActions.loadTagsError);
    return promise;
}
/**
 * Fetch tag values for an organization.
 * The `projectIds` argument can be used to subset projects.
 */
export function fetchTagValues(api, orgId, tagKey, search, projectIds, endpointParams, includeTransactions) {
    if (search === void 0) { search = null; }
    if (projectIds === void 0) { projectIds = null; }
    if (endpointParams === void 0) { endpointParams = null; }
    if (includeTransactions === void 0) { includeTransactions = false; }
    var url = "/organizations/" + orgId + "/tags/" + tagKey + "/values/";
    var query = {};
    if (search) {
        query.query = search;
    }
    if (projectIds) {
        query.project = projectIds;
    }
    if (endpointParams) {
        if (endpointParams.start) {
            query.start = endpointParams.start;
        }
        if (endpointParams.end) {
            query.end = endpointParams.end;
        }
        if (endpointParams.statsPeriod) {
            query.statsPeriod = endpointParams.statsPeriod;
        }
    }
    if (includeTransactions) {
        query.includeTransactions = '1';
    }
    return api.requestPromise(url, {
        method: 'GET',
        query: query,
    });
}
//# sourceMappingURL=tags.jsx.map