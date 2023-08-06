import { __assign, __awaiter, __generator } from "tslib";
import 'bootstrap/js/alert';
import 'bootstrap/js/tab';
import 'bootstrap/js/dropdown';
import 'focus-visible';
import 'app/utils/statics-setup';
import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';
import Reflux from 'reflux';
import * as Router from 'react-router';
import SentryRRWeb from '@sentry/rrweb';
import createReactClass from 'create-react-class';
import jQuery from 'jquery';
import moment from 'moment';
import { Integrations } from '@sentry/tracing';
import { ExtraErrorData } from '@sentry/integrations';
import * as Sentry from '@sentry/react';
import { NODE_ENV, DISABLE_RR_WEB, SPA_DSN } from 'app/constants';
import { metric } from 'app/utils/analytics';
import { setupColorScheme } from 'app/utils/matchMedia';
import { init as initApiSentryClient } from 'app/utils/apiSentryClient';
import ConfigStore from 'app/stores/configStore';
import Main from 'app/main';
import ajaxCsrfSetup from 'app/utils/ajaxCsrfSetup';
import plugins from 'app/plugins';
import routes from 'app/routes';
if (NODE_ENV === 'development') {
    import(
    /* webpackChunkName: "SilenceReactUnsafeWarnings" */ /* webpackMode: "eager" */ 'app/utils/silence-react-unsafe-warnings');
}
// App setup
if (window.__initialData) {
    ConfigStore.loadInitialData(window.__initialData);
    if (window.__initialData.dsn_requests) {
        initApiSentryClient(window.__initialData.dsn_requests);
    }
}
// SDK INIT  --------------------------------------------------------
var config = ConfigStore.getConfig();
var tracesSampleRate = config ? config.apmSampling : 0;
function getSentryIntegrations(hasReplays) {
    if (hasReplays === void 0) { hasReplays = false; }
    var integrations = [
        new ExtraErrorData({
            // 6 is arbitrary, seems like a nice number
            depth: 6,
        }),
        new Integrations.BrowserTracing({
            routingInstrumentation: Sentry.reactRouterV3Instrumentation(Router.browserHistory, Router.createRoutes(routes()), Router.match),
            idleTimeout: 5000,
        }),
    ];
    if (hasReplays) {
        // eslint-disable-next-line no-console
        console.log('[sentry] Instrumenting session with rrweb');
        // TODO(ts): The type returned by SentryRRWeb seems to be somewhat
        // incompatible. It's a newer plugin, so this can be expected, but we
        // should fix.
        integrations.push(new SentryRRWeb({
            checkoutEveryNms: 60 * 1000,
        }));
    }
    return integrations;
}
var hasReplays = window.__SENTRY__USER && window.__SENTRY__USER.isStaff && !DISABLE_RR_WEB;
Sentry.init(__assign(__assign({}, window.__SENTRY__OPTIONS), { 
    /**
     * For SPA mode, we need a way to overwrite the default DSN from backend
     * as well as `whitelistUrls`
     */
    dsn: SPA_DSN || window.__SENTRY__OPTIONS.dsn, whitelistUrls: SPA_DSN
        ? ['localhost', 'dev.getsentry.net', 'sentry.dev', 'webpack-internal://']
        : window.__SENTRY__OPTIONS.whitelistUrls, integrations: getSentryIntegrations(hasReplays), tracesSampleRate: tracesSampleRate, autoSessionTracking: true }));
if (window.__SENTRY__USER) {
    Sentry.setUser(window.__SENTRY__USER);
}
if (window.__SENTRY__VERSION) {
    Sentry.setTag('sentry_version', window.__SENTRY__VERSION);
}
Sentry.setTag('rrweb.active', hasReplays ? 'yes' : 'no');
// Used for operational metrics to determine that the application js
// bundle was loaded by browser.
metric.mark({ name: 'sentry-app-init' });
// setup jquery for CSRF tokens
jQuery.ajaxSetup({
    //jQuery won't allow using the ajaxCsrfSetup function directly
    beforeSend: ajaxCsrfSetup,
});
var render = function (Component) {
    var rootEl = document.getElementById('blk_router');
    try {
        ReactDOM.render(<Component />, rootEl);
    }
    catch (err) {
        // eslint-disable-next-line no-console
        console.error(new Error('An unencoded "%" has appeared, it is super effective! (See https://github.com/ReactTraining/history/issues/505)'));
        if (err.message === 'URI malformed') {
            window.location.assign(window.location.pathname);
        }
    }
};
// setup darkmode + favicon
setupColorScheme();
// The password strength component is very heavyweight as it includes the
// zxcvbn, a relatively byte-heavy password strength estimation library. Load
// it on demand.
function loadPasswordStrength(callback) {
    return __awaiter(this, void 0, void 0, function () {
        var module_1, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, import(
                        /* webpackChunkName: "passwordStrength" */ 'app/components/passwordStrength')];
                case 1:
                    module_1 = _a.sent();
                    callback(module_1);
                    return [3 /*break*/, 3];
                case 2:
                    err_1 = _a.sent();
                    return [3 /*break*/, 3];
                case 3: return [2 /*return*/];
            }
        });
    });
}
var globals = {
    // This is the primary entrypoint for rendering the sentry app.
    SentryRenderApp: function () { return render(Main); },
    // The following globals are used in sentry-plugins webpack externals
    // configuration.
    PropTypes: PropTypes,
    React: React,
    Reflux: Reflux,
    Router: Router,
    Sentry: Sentry,
    moment: moment,
    ReactDOM: {
        findDOMNode: ReactDOM.findDOMNode,
        render: ReactDOM.render,
    },
    // jQuery is still exported to the window as some bootsrap functionality
    // and legacy plugins like youtrack make use of it.
    $: jQuery,
    jQuery: jQuery,
    // django templates make use of these globals
    createReactClass: createReactClass,
    SentryApp: {},
};
// The SentryApp global contains exported app modules for use in javascript
// modules that are not compiled with the sentry bundle.
globals.SentryApp = {
    // The following components are used in sentry-plugins.
    Form: require('app/components/forms/form').default,
    FormState: require('app/components/forms/index').FormState,
    LoadingIndicator: require('app/components/loadingIndicator').default,
    plugins: {
        add: plugins.add,
        addContext: plugins.addContext,
        BasePlugin: plugins.BasePlugin,
        DefaultIssuePlugin: plugins.DefaultIssuePlugin,
    },
    // The following components are used in legacy django HTML views
    passwordStrength: { load: loadPasswordStrength },
    U2fSign: require('app/components/u2f/u2fsign').default,
    ConfigStore: require('app/stores/configStore').default,
    SystemAlerts: require('app/views/app/systemAlerts').default,
    Indicators: require('app/components/indicators').default,
    SetupWizard: require('app/components/setupWizard').default,
};
// Make globals available on the window object
Object.keys(globals).forEach(function (name) { return (window[name] = globals[name]); });
export default globals;
//# sourceMappingURL=bootstrap.jsx.map