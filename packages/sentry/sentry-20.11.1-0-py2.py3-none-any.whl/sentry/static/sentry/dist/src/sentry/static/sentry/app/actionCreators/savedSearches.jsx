import { MAX_AUTOCOMPLETE_RECENT_SEARCHES } from 'app/constants';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import SavedSearchesActions from 'app/actions/savedSearchesActions';
import handleXhrErrorResponse from 'app/utils/handleXhrErrorResponse';
import { SavedSearchType } from 'app/types';
export function resetSavedSearches() {
    SavedSearchesActions.resetSavedSearches();
}
export function fetchSavedSearches(api, orgSlug) {
    var url = "/organizations/" + orgSlug + "/searches/";
    SavedSearchesActions.startFetchSavedSearches();
    var promise = api.requestPromise(url, {
        method: 'GET',
    });
    promise
        .then(function (resp) {
        SavedSearchesActions.fetchSavedSearchesSuccess(resp);
    })
        .catch(function (err) {
        SavedSearchesActions.fetchSavedSearchesError(err);
        addErrorMessage(t('Unable to load saved searches'));
    });
    return promise;
}
export function fetchProjectSavedSearches(api, orgSlug, projectId) {
    var url = "/projects/" + orgSlug + "/" + projectId + "/searches/";
    return api.requestPromise(url, {
        method: 'GET',
    });
}
var getRecentSearchUrl = function (orgSlug) {
    return "/organizations/" + orgSlug + "/recent-searches/";
};
/**
 * Saves search term for `user` + `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query The search term that was used
 */
export function saveRecentSearch(api, orgSlug, type, query) {
    var url = getRecentSearchUrl(orgSlug);
    var promise = api.requestPromise(url, {
        method: 'POST',
        data: {
            query: query,
            type: type,
        },
    });
    promise.catch(handleXhrErrorResponse('Unable to save a recent search'));
    return promise;
}
/**
 * Creates a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param name Saved search name
 * @param query Query to save
 */
export function createSavedSearch(api, orgSlug, name, query) {
    var promise = api.requestPromise("/organizations/" + orgSlug + "/searches/", {
        method: 'POST',
        data: {
            type: SavedSearchType.ISSUE,
            query: query,
            name: name,
        },
    });
    // Need to wait for saved search to save unfortunately because we need to redirect
    // to saved search URL
    promise.then(function (resp) {
        SavedSearchesActions.createSavedSearchSuccess(resp);
    });
    return promise;
}
/**
 * Fetches a list of recent search terms conducted by `user` for `orgSlug`
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param type Context for where search happened, 0 for issue, 1 for event
 * @param query A query term used to filter results
 *
 * @return Returns a list of objects of recent search queries performed by user
 */
export function fetchRecentSearches(api, orgSlug, type, query) {
    var url = getRecentSearchUrl(orgSlug);
    var promise = api.requestPromise(url, {
        query: {
            query: query,
            type: type,
            limit: MAX_AUTOCOMPLETE_RECENT_SEARCHES,
        },
    });
    promise.catch(function (resp) {
        if (resp.status !== 401 && resp.status !== 403) {
            handleXhrErrorResponse('Unable to fetch recent searches')(resp);
        }
    });
    return promise;
}
var getPinSearchUrl = function (orgSlug) {
    return "/organizations/" + orgSlug + "/pinned-searches/";
};
export function pinSearch(api, orgSlug, type, query) {
    var url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    SavedSearchesActions.pinSearch(type, query);
    var promise = api.requestPromise(url, {
        method: 'PUT',
        data: {
            query: query,
            type: type,
        },
    });
    promise.then(SavedSearchesActions.pinSearchSuccess);
    promise.catch(handleXhrErrorResponse('Unable to pin search'));
    promise.catch(function () {
        SavedSearchesActions.unpinSearch(type);
    });
    return promise;
}
export function unpinSearch(api, orgSlug, type, pinnedSearch) {
    var url = getPinSearchUrl(orgSlug);
    // Optimistically update store
    SavedSearchesActions.unpinSearch(type);
    var promise = api.requestPromise(url, {
        method: 'DELETE',
        data: {
            type: type,
        },
    });
    promise.catch(handleXhrErrorResponse('Unable to un-pin search'));
    promise.catch(function () {
        var pinnedType = pinnedSearch.type, query = pinnedSearch.query;
        SavedSearchesActions.pinSearch(pinnedType, query);
    });
    return promise;
}
/**
 * Send a DELETE request to remove a saved search
 *
 * @param api API client
 * @param orgSlug Organization slug
 * @param search The search to remove.
 */
export function deleteSavedSearch(api, orgSlug, search) {
    var url = "/organizations/" + orgSlug + "/searches/" + search.id + "/";
    var promise = api
        .requestPromise(url, {
        method: 'DELETE',
    })
        .then(function () { return SavedSearchesActions.deleteSavedSearchSuccess(search); })
        .catch(handleXhrErrorResponse('Unable to delete a saved search'));
    return promise;
}
//# sourceMappingURL=savedSearches.jsx.map