import { t } from 'app/locale';
import { addErrorMessage } from 'app/actionCreators/indicator';
export function fetchSavedQueries(api, orgId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/", {
        method: 'GET',
        query: { query: 'version:2' },
    });
    promise.catch(function () {
        addErrorMessage(t('Unable to load saved queries'));
    });
    return promise;
}
export function fetchSavedQuery(api, orgId, queryId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + queryId + "/", {
        method: 'GET',
    });
    promise.catch(function () {
        addErrorMessage(t('Unable to load saved query'));
    });
    return promise;
}
export function createSavedQuery(api, orgId, query) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/", {
        method: 'POST',
        data: query,
    });
    promise.catch(function () {
        addErrorMessage(t('Unable to create your saved query'));
    });
    return promise;
}
export function updateSavedQuery(api, orgId, query) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + query.id + "/", {
        method: 'PUT',
        data: query,
    });
    promise.catch(function () {
        addErrorMessage(t('Unable to update your saved query'));
    });
    return promise;
}
export function deleteSavedQuery(api, orgId, queryId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/discover/saved/" + queryId + "/", { method: 'DELETE' });
    promise.catch(function () {
        addErrorMessage(t('Unable to delete the saved query'));
    });
    return promise;
}
//# sourceMappingURL=discoverSavedQueries.jsx.map