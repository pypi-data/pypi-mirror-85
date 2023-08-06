import { __assign } from "tslib";
import Reflux from 'reflux';
import PreferencesActions from '../actions/preferencesActions';
var preferenceStoreConfig = {
    prefs: {},
    init: function () {
        this.reset();
        this.listenTo(PreferencesActions.hideSidebar, this.onHideSidebar);
        this.listenTo(PreferencesActions.showSidebar, this.onShowSidebar);
        this.listenTo(PreferencesActions.loadInitialState, this.loadInitialState);
    },
    getInitialState: function () {
        return this.prefs;
    },
    reset: function () {
        this.prefs = {
            collapsed: false,
        };
    },
    loadInitialState: function (prefs) {
        this.prefs = __assign({}, prefs);
        this.trigger(this.prefs);
    },
    onHideSidebar: function () {
        this.prefs.collapsed = true;
        this.trigger(this.prefs);
    },
    onShowSidebar: function () {
        this.prefs.collapsed = false;
        this.trigger(this.prefs);
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
export default Reflux.createStore(preferenceStoreConfig);
//# sourceMappingURL=preferencesStore.jsx.map