import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import ReleaseActions from 'app/actions/releaseActions';
import ReleaseStore, { getReleaseStoreKey } from 'app/stores/releaseStore';
import { ReleaseStatus } from 'app/types';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
export function getProjectRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRelease for the same
    // release to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    ReleaseStore.state.releaseLoading[getReleaseStoreKey(projectSlug, releaseVersion)] = true;
    ReleaseActions.loadRelease(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        ReleaseActions.loadReleaseSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        // This happens when a Project is not linked to a specific Release
        if (err.status === 404) {
            ReleaseActions.loadReleaseSuccess(projectSlug, releaseVersion, null);
            return;
        }
        ReleaseActions.loadReleaseError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getRelease-action-creator']);
            Sentry.captureException(err);
        });
    });
}
export function getReleaseDeploys(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/deploys/";
    // HACK(leedongwei): Same as above
    ReleaseStore.state.deploysLoading[getReleaseStoreKey(projectSlug, releaseVersion)] = true;
    ReleaseActions.loadDeploys(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        ReleaseActions.loadDeploysSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        // This happens when a Project is not linked to a specific Release
        if (err.status === 404) {
            ReleaseActions.loadDeploysSuccess(projectSlug, releaseVersion, null);
            return;
        }
        ReleaseActions.loadDeploysError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getReleaseDeploys-action-creator']);
            Sentry.captureException(err);
        });
    });
}
export function archiveRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    ReleaseActions.loadRelease(orgSlug, projectSlug, releaseVersion);
    addLoadingMessage(t('Archiving Release\u2026'));
    return api
        .requestPromise("/organizations/" + orgSlug + "/releases/", {
        method: 'POST',
        data: {
            status: ReleaseStatus.Archived,
            projects: [],
            version: releaseVersion,
        },
    })
        .then(function (release) {
        ReleaseActions.loadReleaseSuccess(projectSlug, releaseVersion, release);
        addSuccessMessage(t('Release was successfully archived.'));
    })
        .catch(function (error) {
        var _a, _b;
        ReleaseActions.loadReleaseError(projectSlug, releaseVersion, error);
        addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Release could not be be archived.'));
        throw error;
    });
}
export function restoreRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    ReleaseActions.loadRelease(orgSlug, projectSlug, releaseVersion);
    addLoadingMessage(t('Restoring Release\u2026'));
    return api
        .requestPromise("/organizations/" + orgSlug + "/releases/", {
        method: 'POST',
        data: {
            status: ReleaseStatus.Active,
            projects: [],
            version: releaseVersion,
        },
    })
        .then(function (release) {
        ReleaseActions.loadReleaseSuccess(projectSlug, releaseVersion, release);
        addSuccessMessage(t('Release was successfully restored.'));
    })
        .catch(function (error) {
        var _a, _b;
        ReleaseActions.loadReleaseError(projectSlug, releaseVersion, error);
        addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Release could not be be restored.'));
        throw error;
    });
}
//# sourceMappingURL=release.jsx.map