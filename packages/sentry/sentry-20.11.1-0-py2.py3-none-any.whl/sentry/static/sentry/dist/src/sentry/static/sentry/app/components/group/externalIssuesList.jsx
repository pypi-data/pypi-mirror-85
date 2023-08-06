import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AlertLink from 'app/components/alertLink';
import AsyncComponent from 'app/components/asyncComponent';
import ErrorBoundary from 'app/components/errorBoundary';
import ExternalIssueActions from 'app/components/group/externalIssueActions';
import ExternalIssueStore from 'app/stores/externalIssueStore';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import Placeholder from 'app/components/placeholder';
import PluginActions from 'app/components/group/pluginActions';
import { IconGeneric } from 'app/icons';
import SentryAppComponentsStore from 'app/stores/sentryAppComponentsStore';
import SentryAppExternalIssueActions from 'app/components/group/sentryAppExternalIssueActions';
import SentryAppInstallationStore from 'app/stores/sentryAppInstallationsStore';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import SidebarSection from './sidebarSection';
var ExternalIssueList = /** @class */ (function (_super) {
    __extends(ExternalIssueList, _super);
    function ExternalIssueList(props) {
        var _this = _super.call(this, props, {}) || this;
        _this.unsubscribables = [];
        _this.onSentryAppInstallationChange = function (sentryAppInstallations) {
            _this.setState({ sentryAppInstallations: sentryAppInstallations });
        };
        _this.onExternalIssueChange = function (externalIssues) {
            _this.setState({ externalIssues: externalIssues });
        };
        _this.onSentryAppComponentsChange = function (sentryAppComponents) {
            var components = sentryAppComponents.filter(function (c) { return c.type === 'issue-link'; });
            _this.setState({ components: components });
        };
        _this.state = Object.assign({}, _this.state, {
            components: SentryAppComponentsStore.getInitialState(),
            sentryAppInstallations: SentryAppInstallationStore.getInitialState(),
            externalIssues: ExternalIssueStore.getInitialState(),
        });
        return _this;
    }
    ExternalIssueList.prototype.getEndpoints = function () {
        var group = this.props.group;
        return [['integrations', "/groups/" + group.id + "/integrations/"]];
    };
    ExternalIssueList.prototype.UNSAFE_componentWillMount = function () {
        _super.prototype.UNSAFE_componentWillMount.call(this);
        this.unsubscribables = [
            SentryAppInstallationStore.listen(this.onSentryAppInstallationChange, this),
            ExternalIssueStore.listen(this.onExternalIssueChange, this),
            SentryAppComponentsStore.listen(this.onSentryAppComponentsChange, this),
        ];
        this.fetchSentryAppData();
    };
    ExternalIssueList.prototype.componentWillUnmount = function () {
        _super.prototype.componentWillUnmount.call(this);
        this.unsubscribables.forEach(function (unsubscribe) { return unsubscribe(); });
    };
    // We want to do this explicitly so that we can handle errors gracefully,
    // instead of the entire component not rendering.
    //
    // Part of the API request here is fetching data from the Sentry App, so
    // we need to be more conservative about error cases since we don't have
    // control over those services.
    //
    ExternalIssueList.prototype.fetchSentryAppData = function () {
        var _this = this;
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization;
        if (project && project.id && organization) {
            this.api
                .requestPromise("/groups/" + group.id + "/external-issues/")
                .then(function (data) {
                ExternalIssueStore.load(data);
                _this.setState({ externalIssues: data });
            })
                .catch(function (_error) { });
        }
    };
    ExternalIssueList.prototype.updateIntegrations = function (onSuccess, onError) {
        if (onSuccess === void 0) { onSuccess = function () { }; }
        if (onError === void 0) { onError = function () { }; }
        return __awaiter(this, void 0, void 0, function () {
            var group, integrations, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        group = this.props.group;
                        return [4 /*yield*/, this.api.requestPromise("/groups/" + group.id + "/integrations/")];
                    case 1:
                        integrations = _a.sent();
                        this.setState({ integrations: integrations }, function () { return onSuccess(); });
                        return [3 /*break*/, 3];
                    case 2:
                        error_1 = _a.sent();
                        onError();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    ExternalIssueList.prototype.renderIntegrationIssues = function (integrations) {
        var _this = this;
        if (integrations === void 0) { integrations = []; }
        var group = this.props.group;
        var activeIntegrations = integrations.filter(function (integration) { return integration.status === 'active'; });
        var activeIntegrationsByProvider = activeIntegrations.reduce(function (acc, curr) {
            var items = acc.get(curr.provider.key);
            if (!!items) {
                acc.set(curr.provider.key, __spread(items, [curr]));
            }
            else {
                acc.set(curr.provider.key, [curr]);
            }
            return acc;
        }, new Map());
        return activeIntegrations.length
            ? __spread(activeIntegrationsByProvider.entries()).map(function (_a) {
                var _b = __read(_a, 2), provider = _b[0], configurations = _b[1];
                return (<ExternalIssueActions key={provider} configurations={configurations} group={group} onChange={_this.updateIntegrations.bind(_this)}/>);
            })
            : null;
    };
    ExternalIssueList.prototype.renderSentryAppIssues = function () {
        var _this = this;
        var _a = this.state, externalIssues = _a.externalIssues, sentryAppInstallations = _a.sentryAppInstallations, components = _a.components;
        var group = this.props.group;
        if (components.length === 0) {
            return null;
        }
        return components.map(function (component) {
            var sentryApp = component.sentryApp;
            var installation = sentryAppInstallations.find(function (i) { return i.app.uuid === sentryApp.uuid; });
            //should always find a match but TS complains if we don't handle this case
            if (!installation) {
                return null;
            }
            var issue = (externalIssues || []).find(function (i) { return i.serviceType === sentryApp.slug; });
            return (<ErrorBoundary key={sentryApp.slug} mini>
          <SentryAppExternalIssueActions key={sentryApp.slug} group={group} event={_this.props.event} sentryAppComponent={component} sentryAppInstallation={installation} externalIssue={issue}/>
        </ErrorBoundary>);
        });
    };
    ExternalIssueList.prototype.renderPluginIssues = function () {
        var _a = this.props, group = _a.group, project = _a.project;
        return group.pluginIssues && group.pluginIssues.length
            ? group.pluginIssues.map(function (plugin, i) { return (<PluginActions group={group} project={project} plugin={plugin} key={i}/>); })
            : null;
    };
    ExternalIssueList.prototype.renderPluginActions = function () {
        var group = this.props.group;
        return group.pluginActions && group.pluginActions.length
            ? group.pluginActions.map(function (plugin, i) { return (<IssueSyncListElement externalIssueLink={plugin[1]} key={i}>
            {plugin[0]}
          </IssueSyncListElement>); })
            : null;
    };
    ExternalIssueList.prototype.renderLoading = function () {
        return (<SidebarSection data-test-id="linked-issues" title={t('Linked Issues')}>
        <Placeholder height="120px"/>
      </SidebarSection>);
    };
    ExternalIssueList.prototype.renderBody = function () {
        var sentryAppIssues = this.renderSentryAppIssues();
        var integrationIssues = this.renderIntegrationIssues(this.state.integrations);
        var pluginIssues = this.renderPluginIssues();
        var pluginActions = this.renderPluginActions();
        var showSetup = !sentryAppIssues && !integrationIssues && !pluginIssues && !pluginActions;
        return (<SidebarSection data-test-id="linked-issues" title={t('Linked Issues')}>
        {showSetup && (<AlertLink icon={<IconGeneric />} priority="muted" size="small" to={"/settings/" + this.props.organization.slug + "/integrations"}>
            {t('Set up Issue Tracking')}
          </AlertLink>)}
        {sentryAppIssues && <Wrapper>{sentryAppIssues}</Wrapper>}
        {integrationIssues && <Wrapper>{integrationIssues}</Wrapper>}
        {pluginIssues && <Wrapper>{pluginIssues}</Wrapper>}
        {pluginActions && <Wrapper>{pluginActions}</Wrapper>}
      </SidebarSection>);
    };
    return ExternalIssueList;
}(AsyncComponent));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export default withOrganization(ExternalIssueList);
var templateObject_1;
//# sourceMappingURL=externalIssuesList.jsx.map