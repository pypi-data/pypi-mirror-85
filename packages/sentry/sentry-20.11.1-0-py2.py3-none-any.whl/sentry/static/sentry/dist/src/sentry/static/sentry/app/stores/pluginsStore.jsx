import { __assign, __rest } from "tslib";
import Reflux from 'reflux';
import PluginActions from 'app/actions/pluginActions';
var defaultState = {
    loading: true,
    plugins: [],
    error: null,
    pageLinks: null,
};
var PluginStoreConfig = {
    plugins: null,
    state: __assign({}, defaultState),
    updating: new Map(),
    reset: function () {
        //reset our state
        this.plugins = null;
        this.state = __assign({}, defaultState);
        this.updating = new Map();
        return this.state;
    },
    getInitialState: function () {
        return this.getState();
    },
    getState: function () {
        var _a = this.state, _plugins = _a.plugins, state = __rest(_a, ["plugins"]);
        return __assign(__assign({}, state), { plugins: this.plugins ? Array.from(this.plugins.values()) : [] });
    },
    init: function () {
        this.reset();
        this.listenTo(PluginActions.fetchAll, this.onFetchAll);
        this.listenTo(PluginActions.fetchAllSuccess, this.onFetchAllSuccess);
        this.listenTo(PluginActions.fetchAllError, this.onFetchAllError);
        this.listenTo(PluginActions.update, this.onUpdate);
        this.listenTo(PluginActions.updateSuccess, this.onUpdateSuccess);
        this.listenTo(PluginActions.updateError, this.onUpdateError);
    },
    triggerState: function () {
        this.trigger(this.getState());
    },
    onFetchAll: function (_a) {
        var resetLoading = (_a === void 0 ? {} : _a).resetLoading;
        if (resetLoading) {
            this.state.loading = true;
            this.state.error = null;
            this.plugins = null;
        }
        this.triggerState();
    },
    onFetchAllSuccess: function (data, _a) {
        var pageLinks = _a.pageLinks;
        this.plugins = new Map(data.map(function (plugin) { return [plugin.id, plugin]; }));
        this.state.pageLinks = pageLinks || null;
        this.state.loading = false;
        this.triggerState();
    },
    onFetchAllError: function (err) {
        this.plugins = null;
        this.state.loading = false;
        this.state.error = err;
        this.triggerState();
    },
    onUpdate: function (id, updateObj) {
        if (!this.plugins) {
            return;
        }
        var plugin = this.plugins.get(id);
        if (!plugin) {
            return;
        }
        var newPlugin = __assign(__assign({}, plugin), updateObj);
        this.plugins.set(id, newPlugin);
        this.updating.set(id, plugin);
        this.triggerState();
    },
    onUpdateSuccess: function (id, _updateObj) {
        this.updating.delete(id);
    },
    onUpdateError: function (id, _updateObj, err) {
        var origPlugin = this.updating.get(id);
        if (!origPlugin || !this.plugins) {
            return;
        }
        this.plugins.set(id, origPlugin);
        this.updating.delete(id);
        this.state.error = err;
        this.triggerState();
    },
};
var PluginStore = Reflux.createStore(PluginStoreConfig);
export default PluginStore;
//# sourceMappingURL=pluginsStore.jsx.map