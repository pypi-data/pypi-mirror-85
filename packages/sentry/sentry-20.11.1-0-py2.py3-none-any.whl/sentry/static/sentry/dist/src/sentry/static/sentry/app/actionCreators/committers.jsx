import { __assign } from "tslib";
import CommitterActions from 'app/actions/committerActions';
import CommitterStore, { getCommitterStoreKey } from 'app/stores/committerStore';
export function getCommitters(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, eventId = params.eventId;
    var path = "/projects/" + orgSlug + "/" + projectSlug + "/events/" + eventId + "/committers/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRepo for the same
    // repo to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    var storeKey = getCommitterStoreKey(orgSlug, projectSlug, eventId);
    CommitterStore.state[storeKey] = __assign(__assign({}, CommitterStore.state[storeKey]), { committersLoading: true });
    CommitterActions.load(orgSlug, projectSlug, eventId);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        CommitterActions.loadSuccess(orgSlug, projectSlug, eventId, res.committers);
    })
        .catch(function (err) {
        // NOTE: Do not captureException here as EventFileCommittersEndpoint returns
        // 404 Not Found if the project did not setup Releases or Commits
        CommitterActions.loadError(orgSlug, projectSlug, eventId, err);
    });
}
//# sourceMappingURL=committers.jsx.map