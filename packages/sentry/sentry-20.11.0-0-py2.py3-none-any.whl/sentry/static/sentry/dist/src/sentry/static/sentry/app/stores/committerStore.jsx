import { __assign } from "tslib";
import Reflux from 'reflux';
import CommitterActions from 'app/actions/committerActions';
export var CommitterStoreConfig = {
    listenables: CommitterActions,
    state: {},
    init: function () {
        this.reset();
    },
    reset: function () {
        this.state = {};
        this.trigger(this.state);
    },
    load: function (orgSlug, projectSlug, eventId) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = __assign(__assign({}, this.state), (_a = {}, _a[key] = {
            committers: undefined,
            committersLoading: true,
            committersError: undefined,
        }, _a));
        this.trigger(this.state);
    },
    loadError: function (orgSlug, projectSlug, eventId, err) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = __assign(__assign({}, this.state), (_a = {}, _a[key] = {
            committers: undefined,
            committersLoading: false,
            committersError: err,
        }, _a));
        this.trigger(this.state);
    },
    loadSuccess: function (orgSlug, projectSlug, eventId, data) {
        var _a;
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        this.state = __assign(__assign({}, this.state), (_a = {}, _a[key] = {
            committers: data,
            committersLoading: false,
            committersError: undefined,
        }, _a));
        this.trigger(this.state);
    },
    get: function (orgSlug, projectSlug, eventId) {
        var key = getCommitterStoreKey(orgSlug, projectSlug, eventId);
        return __assign({}, this.state[key]);
    },
};
export function getCommitterStoreKey(orgSlug, projectSlug, eventId) {
    return orgSlug + " " + projectSlug + " " + eventId;
}
export default Reflux.createStore(CommitterStoreConfig);
//# sourceMappingURL=committerStore.jsx.map