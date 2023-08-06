import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import { installSentryApp, uninstallSentryApp, } from 'app/actionCreators/sentryAppInstallations';
import Button from 'app/components/button';
import CircleIndicator from 'app/components/circleIndicator';
import Confirm from 'app/components/confirm';
import { IconSubtract } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { toPermissions } from 'app/utils/consolidatedScopes';
import { getSentryAppInstallStatus } from 'app/utils/integrationUtil';
import { addQueryParamsToExistingUrl } from 'app/utils/queryString';
import { recordInteraction } from 'app/utils/recordSentryAppInteraction';
import withOrganization from 'app/utils/withOrganization';
import AbstractIntegrationDetailedView from './abstractIntegrationDetailedView';
import SplitInstallationIdModal from './SplitInstallationIdModal';
var SentryAppDetailedView = /** @class */ (function (_super) {
    __extends(SentryAppDetailedView, _super);
    function SentryAppDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tabs = ['overview'];
        _this.redirectUser = function (install) {
            var organization = _this.props.organization;
            var sentryApp = _this.state.sentryApp;
            var queryParams = {
                installationId: install.uuid,
                code: install.code,
                orgSlug: organization.slug,
            };
            if (sentryApp.redirectUrl) {
                var redirectUrl = addQueryParamsToExistingUrl(sentryApp.redirectUrl, queryParams);
                window.location.assign(redirectUrl);
            }
        };
        _this.handleInstall = function () { return __awaiter(_this, void 0, void 0, function () {
            var organization, sentryApp, install;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        sentryApp = this.state.sentryApp;
                        this.trackIntegrationEvent({
                            eventKey: 'integrations.installation_start',
                            eventName: 'Integrations: Installation Start',
                            integration_status: sentryApp.status,
                        });
                        return [4 /*yield*/, installSentryApp(this.api, organization.slug, sentryApp)];
                    case 1:
                        install = _a.sent();
                        //installation is complete if the status is installed
                        if (install.status === 'installed') {
                            this.trackIntegrationEvent({
                                eventKey: 'integrations.installation_complete',
                                eventName: 'Integrations: Installation Complete',
                                integration_status: sentryApp.status,
                            });
                        }
                        if (!sentryApp.redirectUrl) {
                            addSuccessMessage(t(sentryApp.slug + " successfully installed."));
                            this.setState({ appInstalls: __spread([install], this.state.appInstalls) });
                            //hack for split so we can show the install ID to users for them to copy
                            //Will remove once the proper fix is in place
                            if (['split', 'split-dev', 'split-testing'].includes(sentryApp.slug)) {
                                openModal(function (_a) {
                                    var closeModal = _a.closeModal;
                                    return (<SplitInstallationIdModal installationId={install.uuid} closeModal={closeModal}/>);
                                });
                            }
                        }
                        else {
                            this.redirectUser(install);
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleUninstall = function (install) { return __awaiter(_this, void 0, void 0, function () {
            var appInstalls, error_1;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, uninstallSentryApp(this.api, install)];
                    case 1:
                        _a.sent();
                        this.trackIntegrationEvent({
                            eventKey: 'integrations.uninstall_completed',
                            eventName: 'Integrations: Uninstall Completed',
                            integration_status: this.sentryApp.status,
                        });
                        appInstalls = this.state.appInstalls.filter(function (i) { return i.app.slug !== _this.sentryApp.slug; });
                        return [2 /*return*/, this.setState({ appInstalls: appInstalls })];
                    case 2:
                        error_1 = _a.sent();
                        return [2 /*return*/, addErrorMessage(t("Unable to uninstall " + this.sentryApp.name))];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.recordUninstallClicked = function () {
            var sentryApp = _this.sentryApp;
            _this.trackIntegrationEvent({
                eventKey: 'integrations.uninstall_clicked',
                eventName: 'Integrations: Uninstall Clicked',
                integration_status: sentryApp.status,
            });
        };
        return _this;
    }
    SentryAppDetailedView.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, integrationSlug = _a.params.integrationSlug;
        var baseEndpoints = [
            ['sentryApp', "/sentry-apps/" + integrationSlug + "/"],
            ['featureData', "/sentry-apps/" + integrationSlug + "/features/"],
            ['appInstalls', "/organizations/" + organization.slug + "/sentry-app-installations/"],
        ];
        return baseEndpoints;
    };
    SentryAppDetailedView.prototype.onLoadAllEndpointsSuccess = function () {
        var _a = this.props, organization = _a.organization, integrationSlug = _a.params.integrationSlug, router = _a.router;
        //redirect for internal integrations
        if (this.sentryApp.status === 'internal') {
            router.push("/settings/" + organization.slug + "/developer-settings/" + integrationSlug + "/");
            return;
        }
        _super.prototype.onLoadAllEndpointsSuccess.call(this);
        recordInteraction(integrationSlug, 'sentry_app_viewed');
    };
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationType", {
        get: function () {
            return 'sentry_app';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "sentryApp", {
        get: function () {
            return this.state.sentryApp;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "description", {
        get: function () {
            return this.state.sentryApp.overview || '';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "author", {
        get: function () {
            return this.sentryApp.author;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "resourceLinks", {
        get: function () {
            //only show links for published sentry apps
            if (this.sentryApp.status !== 'published') {
                return [];
            }
            return [
                {
                    title: 'Documentation',
                    url: "https://docs.sentry.io/product/integrations/" + this.integrationSlug + "/",
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "permissions", {
        get: function () {
            return toPermissions(this.sentryApp.scopes);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "installationStatus", {
        get: function () {
            return getSentryAppInstallStatus(this.install);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationName", {
        get: function () {
            return this.sentryApp.name;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "featureData", {
        get: function () {
            return this.state.featureData;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "install", {
        get: function () {
            var _this = this;
            return this.state.appInstalls.find(function (i) { return i.app.slug === _this.sentryApp.slug; });
        },
        enumerable: false,
        configurable: true
    });
    SentryAppDetailedView.prototype.renderPermissions = function () {
        var permissions = this.permissions;
        if (!Object.keys(permissions).some(function (scope) { return permissions[scope].length > 0; })) {
            return null;
        }
        return (<PermissionWrapper>
        <Title>Permissions</Title>
        {permissions.read.length > 0 && (<Permission>
            <Indicator />
            <Text key="read">
              {tct('[read] access to [resources] resources', {
            read: <strong>Read</strong>,
            resources: permissions.read.join(', '),
        })}
            </Text>
          </Permission>)}
        {permissions.write.length > 0 && (<Permission>
            <Indicator />
            <Text key="write">
              {tct('[read] and [write] access to [resources] resources', {
            read: <strong>Read</strong>,
            write: <strong>Write</strong>,
            resources: permissions.write.join(', '),
        })}
            </Text>
          </Permission>)}
        {permissions.admin.length > 0 && (<Permission>
            <Indicator />
            <Text key="admin">
              {tct('[admin] access to [resources] resources', {
            admin: <strong>Admin</strong>,
            resources: permissions.admin.join(', '),
        })}
            </Text>
          </Permission>)}
      </PermissionWrapper>);
    };
    SentryAppDetailedView.prototype.renderTopButton = function (disabledFromFeatures, userHasAccess) {
        var _this = this;
        var install = this.install;
        if (install) {
            return (<Confirm disabled={!userHasAccess} message={tct('Are you sure you want to remove the [slug] installation?', {
                slug: this.integrationSlug,
            })} onConfirm={function () { return _this.handleUninstall(install); }} //called when the user confirms the action
             onConfirming={this.recordUninstallClicked} //called when the confirm modal opens
             priority="danger">
          <StyledUninstallButton size="small" data-test-id="sentry-app-uninstall">
            <IconSubtract isCircled style={{ marginRight: space(0.75) }}/>
            {t('Uninstall')}
          </StyledUninstallButton>
        </Confirm>);
        }
        if (userHasAccess) {
            return (<InstallButton data-test-id="install-button" disabled={disabledFromFeatures} onClick={function () { return _this.handleInstall(); }} priority="primary" size="small" style={{ marginLeft: space(1) }}>
          {t('Accept & Install')}
        </InstallButton>);
        }
        return this.renderRequestIntegrationButton();
    };
    //no configurations for sentry apps
    SentryAppDetailedView.prototype.renderConfigurations = function () {
        return null;
    };
    return SentryAppDetailedView;
}(AbstractIntegrationDetailedView));
var Text = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0px 6px;\n"], ["\n  margin: 0px 6px;\n"])));
var Permission = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var PermissionWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space(2));
var Title = styled('p')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-weight: bold;\n"], ["\n  margin-bottom: ", ";\n  font-weight: bold;\n"])), space(1));
var Indicator = styled(function (p) { return <CircleIndicator size={7} {...p}/>; })(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-top: 3px;\n  color: ", ";\n"], ["\n  margin-top: 3px;\n  color: ", ";\n"])), function (p) { return p.theme.success; });
var InstallButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledUninstallButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  background: ", ";\n\n  border: ", ";\n  box-sizing: border-box;\n  box-shadow: 0px 2px 1px rgba(0, 0, 0, 0.08);\n  border-radius: 4px;\n"], ["\n  color: ", ";\n  background: ", ";\n\n  border: ", ";\n  box-sizing: border-box;\n  box-shadow: 0px 2px 1px rgba(0, 0, 0, 0.08);\n  border-radius: 4px;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.background; }, function (p) { return "1px solid " + p.theme.gray300; });
export default withOrganization(SentryAppDetailedView);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=sentryAppDetailedView.jsx.map