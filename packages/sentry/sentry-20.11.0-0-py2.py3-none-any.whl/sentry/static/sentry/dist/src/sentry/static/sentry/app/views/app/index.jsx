import { __decorate, __extends, __read, __spread } from "tslib";
import $ from 'jquery';
import { browserHistory } from 'react-router';
import Cookies from 'js-cookie';
import PropTypes from 'prop-types';
import React from 'react';
import isEqual from 'lodash/isEqual';
import keydown from 'react-keydown';
import { DEPLOY_PREVIEW_CONFIG, EXPERIMENTAL_SPA } from 'app/constants';
import { displayDeployPreviewAlert, displayExperimentalSpaAlert, } from 'app/actionCreators/deployPreview';
import { fetchGuides } from 'app/actionCreators/guides';
import { openCommandPalette } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import AlertActions from 'app/actions/alertActions';
import ConfigStore from 'app/stores/configStore';
import ErrorBoundary from 'app/components/errorBoundary';
import GlobalModal from 'app/components/globalModal';
import HookStore from 'app/stores/hookStore';
import Indicators from 'app/components/indicators';
import LoadingIndicator from 'app/components/loadingIndicator';
import NewsletterConsent from 'app/views/newsletterConsent';
import OrganizationsStore from 'app/stores/organizationsStore';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import SystemAlerts from './systemAlerts';
// TODO: Need better way of identifying anonymous pages that don't trigger redirect
var ALLOWED_ANON_PAGES = [
    /^\/accept\//,
    /^\/share\//,
    /^\/auth\/login\//,
    /^\/join-request\//,
];
function getAlertTypeForProblem(problem) {
    switch (problem.severity) {
        case 'critical':
            return 'error';
        default:
            return 'warning';
    }
}
var App = /** @class */ (function (_super) {
    __extends(App, _super);
    function App() {
        var _a, _b, _c;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.state = {
            loading: false,
            error: false,
            needsUpgrade: ((_a = ConfigStore.get('user')) === null || _a === void 0 ? void 0 : _a.isSuperuser) && ConfigStore.get('needsUpgrade'),
            newsletterConsentPrompt: (_c = (_b = ConfigStore.get('user')) === null || _b === void 0 ? void 0 : _b.flags) === null || _c === void 0 ? void 0 : _c.newsletter_consent_prompt,
        };
        _this.mainContainerRef = React.createRef();
        _this.onConfigured = function () { return _this.setState({ needsUpgrade: false }); };
        // this is somewhat hackish
        _this.handleNewsletterConsent = function () {
            return _this.setState({
                newsletterConsentPrompt: false,
            });
        };
        _this.handleGlobalModalClose = function () {
            var _a;
            if (typeof ((_a = _this.mainContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus) === 'function') {
                // Focus the main container to get hotkeys to keep working after modal closes
                _this.mainContainerRef.current.focus();
            }
        };
        return _this;
    }
    App.prototype.getChildContext = function () {
        return {
            location: this.props.location,
        };
    };
    App.prototype.componentDidMount = function () {
        var _this = this;
        this.props.api.request('/organizations/', {
            query: {
                member: '1',
            },
            success: function (data) {
                OrganizationsStore.load(data);
                _this.setState({
                    loading: false,
                });
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
        this.props.api.request('/internal/health/', {
            success: function (data) {
                if (data && data.problems) {
                    data.problems.forEach(function (problem) {
                        AlertActions.addAlert({
                            id: problem.id,
                            message: problem.message,
                            type: getAlertTypeForProblem(problem),
                            url: problem.url,
                        });
                    });
                }
            },
            error: function () { },
        });
        ConfigStore.get('messages').forEach(function (msg) {
            AlertActions.addAlert({
                message: msg.message,
                type: msg.level,
                neverExpire: true,
            });
        });
        if (DEPLOY_PREVIEW_CONFIG) {
            displayDeployPreviewAlert();
        }
        else if (EXPERIMENTAL_SPA) {
            displayExperimentalSpaAlert();
        }
        $(document).ajaxError(function (_evt, jqXHR) {
            var _a, _b, _c, _d;
            var pageAllowsAnon = ALLOWED_ANON_PAGES.find(function (regex) {
                return regex.test(window.location.pathname);
            });
            // Ignore error unless it is a 401
            if (!jqXHR || jqXHR.status !== 401 || pageAllowsAnon) {
                return;
            }
            var code = (_b = (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
            var extra = (_d = (_c = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra;
            // 401s can also mean sudo is required or it's a request that is allowed to fail
            // Ignore if these are the cases
            if (code === 'sudo-required' || code === 'ignore') {
                return;
            }
            // If user must login via SSO, redirect to org login page
            if (code === 'sso-required') {
                window.location.assign(extra.loginUrl);
                return;
            }
            // Otherwise, the user has become unauthenticated. Send them to auth
            Cookies.set('session_expired', '1');
            if (EXPERIMENTAL_SPA) {
                browserHistory.replace('/auth/login/');
            }
            else {
                window.location.reload();
            }
        });
        var user = ConfigStore.get('user');
        if (user) {
            HookStore.get('analytics:init-user').map(function (cb) { return cb(user); });
        }
        fetchGuides();
    };
    App.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (!isEqual(config, prevProps.config)) {
            this.handleConfigStoreChange(config);
        }
    };
    App.prototype.componentWillUnmount = function () {
        OrganizationsStore.load([]);
    };
    App.prototype.handleConfigStoreChange = function (config) {
        var newState = {};
        if (config.needsUpgrade !== undefined) {
            newState.needsUpgrade = config.needsUpgrade;
        }
        if (config.user !== undefined) {
            newState.user = config.user;
        }
        if (Object.keys(newState).length > 0) {
            this.setState(newState);
        }
    };
    App.prototype.openCommandPalette = function (e) {
        openCommandPalette();
        e.preventDefault();
        e.stopPropagation();
    };
    App.prototype.renderBody = function () {
        var _a = this.state, needsUpgrade = _a.needsUpgrade, newsletterConsentPrompt = _a.newsletterConsentPrompt;
        if (needsUpgrade) {
            var InstallWizard = React.lazy(function () {
                return import(/* webpackChunkName: "InstallWizard" */ 'app/views/admin/installWizard');
            });
            return (<React.Suspense fallback={null}>
          <InstallWizard onConfigured={this.onConfigured}/>;
        </React.Suspense>);
        }
        if (newsletterConsentPrompt) {
            return <NewsletterConsent onSubmitSuccess={this.handleNewsletterConsent}/>;
        }
        return this.props.children;
    };
    App.prototype.render = function () {
        if (this.state.loading) {
            return (<LoadingIndicator triangle>
          {t('Getting a list of all of your organizations.')}
        </LoadingIndicator>);
        }
        return (<div className="main-container" tabIndex={-1} ref={this.mainContainerRef}>
        <GlobalModal onClose={this.handleGlobalModalClose}/>
        <SystemAlerts className="messages-container"/>
        <Indicators className="indicators-container"/>
        <ErrorBoundary>{this.renderBody()}</ErrorBoundary>
      </div>);
    };
    App.childContextTypes = {
        location: PropTypes.object,
    };
    __decorate([
        keydown('meta+shift+p', 'meta+k')
    ], App.prototype, "openCommandPalette", null);
    return App;
}(React.Component));
export default withApi(withConfig(App));
//# sourceMappingURL=index.jsx.map