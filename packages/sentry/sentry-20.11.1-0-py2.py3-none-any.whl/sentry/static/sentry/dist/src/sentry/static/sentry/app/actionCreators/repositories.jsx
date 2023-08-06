import * as Sentry from '@sentry/react';
import RepositoryActions from 'app/actions/repositoryActions';
import RepositoryStore from 'app/stores/repositoryStore';
export function getRepositories(api, params) {
    var orgSlug = params.orgSlug;
    var path = "/organizations/" + orgSlug + "/repos/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRepo for the same
    // repo to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    RepositoryStore.state.repositoriesLoading = true;
    RepositoryActions.loadRepositories(orgSlug);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        RepositoryActions.loadRepositoriesSuccess(res);
    })
        .catch(function (err) {
        RepositoryActions.loadRepositoriesError(err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getRepositories-action-creator']);
            Sentry.captureException(err);
        });
    });
}
//# sourceMappingURL=repositories.jsx.map