import { __assign, __rest } from "tslib";
import Reflux from 'reflux';
import ReleaseActions from 'app/actions/releaseActions';
import OrganizationActions from 'app/actions/organizationActions';
export var getReleaseStoreKey = function (projectSlug, releaseVersion) {
    return "" + projectSlug + releaseVersion;
};
var ReleaseStoreConfig = {
    state: {
        orgSlug: undefined,
        release: new Map(),
        releaseLoading: new Map(),
        releaseError: new Map(),
        deploys: new Map(),
        deploysLoading: new Map(),
        deploysError: new Map(),
    },
    listenables: ReleaseActions,
    init: function () {
        this.listenTo(OrganizationActions.update, this.updateOrganization);
        this.reset();
    },
    reset: function () {
        this.state = {
            orgSlug: undefined,
            release: new Map(),
            releaseLoading: new Map(),
            releaseError: new Map(),
            deploys: new Map(),
            deploysLoading: new Map(),
            deploysError: new Map(),
        };
        this.trigger(this.state);
    },
    updateOrganization: function (org) {
        this.reset();
        this.state.orgSlug = org.slug;
        this.trigger(this.state);
    },
    loadRelease: function (orgSlug, projectSlug, releaseVersion) {
        var _a, _b;
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, releaseLoading = _c.releaseLoading, releaseError = _c.releaseError, state = __rest(_c, ["releaseLoading", "releaseError"]);
        this.state = __assign(__assign({}, state), { releaseLoading: __assign(__assign({}, releaseLoading), (_a = {}, _a[releaseKey] = true, _a)), releaseError: __assign(__assign({}, releaseError), (_b = {}, _b[releaseKey] = undefined, _b)) });
        this.trigger(this.state);
    },
    loadReleaseError: function (projectSlug, releaseVersion, error) {
        var _a, _b;
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, releaseLoading = _c.releaseLoading, releaseError = _c.releaseError, state = __rest(_c, ["releaseLoading", "releaseError"]);
        this.state = __assign(__assign({}, state), { releaseLoading: __assign(__assign({}, releaseLoading), (_a = {}, _a[releaseKey] = false, _a)), releaseError: __assign(__assign({}, releaseError), (_b = {}, _b[releaseKey] = error, _b)) });
        this.trigger(this.state);
    },
    loadReleaseSuccess: function (projectSlug, releaseVersion, data) {
        var _a, _b, _c;
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _d = this.state, release = _d.release, releaseLoading = _d.releaseLoading, releaseError = _d.releaseError, state = __rest(_d, ["release", "releaseLoading", "releaseError"]);
        this.state = __assign(__assign({}, state), { release: __assign(__assign({}, release), (_a = {}, _a[releaseKey] = data, _a)), releaseLoading: __assign(__assign({}, releaseLoading), (_b = {}, _b[releaseKey] = false, _b)), releaseError: __assign(__assign({}, releaseError), (_c = {}, _c[releaseKey] = undefined, _c)) });
        this.trigger(this.state);
    },
    loadDeploys: function (orgSlug, projectSlug, releaseVersion) {
        var _a, _b;
        // Wipe entire store if the user switched organizations
        if (!this.orgSlug || this.orgSlug !== orgSlug) {
            this.reset();
            this.orgSlug = orgSlug;
        }
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, deploysLoading = _c.deploysLoading, deploysError = _c.deploysError, state = __rest(_c, ["deploysLoading", "deploysError"]);
        this.state = __assign(__assign({}, state), { deploysLoading: __assign(__assign({}, deploysLoading), (_a = {}, _a[releaseKey] = true, _a)), deploysError: __assign(__assign({}, deploysError), (_b = {}, _b[releaseKey] = undefined, _b)) });
        this.trigger(this.state);
    },
    loadDeploysError: function (projectSlug, releaseVersion, error) {
        var _a, _b;
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _c = this.state, deploysLoading = _c.deploysLoading, deploysError = _c.deploysError, state = __rest(_c, ["deploysLoading", "deploysError"]);
        this.state = __assign(__assign({}, state), { deploysLoading: __assign(__assign({}, deploysLoading), (_a = {}, _a[releaseKey] = false, _a)), deploysError: __assign(__assign({}, deploysError), (_b = {}, _b[releaseKey] = error, _b)) });
        this.trigger(this.state);
    },
    loadDeploysSuccess: function (projectSlug, releaseVersion, data) {
        var _a, _b, _c;
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        var _d = this.state, deploys = _d.deploys, deploysLoading = _d.deploysLoading, deploysError = _d.deploysError, state = __rest(_d, ["deploys", "deploysLoading", "deploysError"]);
        this.state = __assign(__assign({}, state), { deploys: __assign(__assign({}, deploys), (_a = {}, _a[releaseKey] = data, _a)), deploysLoading: __assign(__assign({}, deploysLoading), (_b = {}, _b[releaseKey] = false, _b)), deploysError: __assign(__assign({}, deploysError), (_c = {}, _c[releaseKey] = undefined, _c)) });
        this.trigger(this.state);
    },
    get: function (projectSlug, releaseVersion) {
        var releaseKey = getReleaseStoreKey(projectSlug, releaseVersion);
        return {
            release: this.state.release[releaseKey],
            releaseLoading: this.state.releaseLoading[releaseKey],
            releaseError: this.state.releaseError[releaseKey],
            deploys: this.state.deploys[releaseKey],
            deploysLoading: this.state.deploysLoading[releaseKey],
            deploysError: this.state.deploysError[releaseKey],
        };
    },
};
export default Reflux.createStore(ReleaseStoreConfig);
//# sourceMappingURL=releaseStore.jsx.map