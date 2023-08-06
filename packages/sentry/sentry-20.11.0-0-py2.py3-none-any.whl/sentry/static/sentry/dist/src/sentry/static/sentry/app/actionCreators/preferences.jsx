import Cookies from 'js-cookie';
import PreferencesActions from '../actions/preferencesActions';
var SIDEBAR_COOKIE_KEY = 'sidebar_collapsed';
var COOKIE_ENABLED = '1';
var COOKIE_DISABLED = '0';
export function hideSidebar() {
    PreferencesActions.hideSidebar();
    Cookies.set(SIDEBAR_COOKIE_KEY, COOKIE_ENABLED);
}
export function showSidebar() {
    PreferencesActions.showSidebar();
    Cookies.set(SIDEBAR_COOKIE_KEY, COOKIE_DISABLED);
}
export function loadPreferencesState() {
    // Set initial "collapsed" state to true or false
    PreferencesActions.loadInitialState({
        collapsed: Cookies.get(SIDEBAR_COOKIE_KEY) === COOKIE_ENABLED,
    });
}
//# sourceMappingURL=preferences.jsx.map