import { __extends } from "tslib";
import React from 'react';
import AlertLink from 'app/components/alertLink';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { IconAdd } from 'app/icons';
import { removeSentryApp } from 'app/actionCreators/sentryApps';
import SentryTypes from 'app/sentryTypes';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import SentryApplicationRow from 'app/views/settings/organizationDeveloperSettings/sentryApplicationRow';
import withOrganization from 'app/utils/withOrganization';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
var OrganizationDeveloperSettings = /** @class */ (function (_super) {
    __extends(OrganizationDeveloperSettings, _super);
    function OrganizationDeveloperSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeApp = function (app) {
            var apps = _this.state.applications.filter(function (a) { return a.slug !== app.slug; });
            removeSentryApp(_this.api, app).then(function () {
                _this.setState({ applications: apps });
            }, function () { });
        };
        _this.renderApplicationRow = function (app) {
            var organization = _this.props.organization;
            return (<SentryApplicationRow key={app.uuid} app={app} organization={organization} onRemoveApp={_this.removeApp}/>);
        };
        return _this;
    }
    OrganizationDeveloperSettings.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitleGen(t('Developer Settings'), orgId, false);
    };
    OrganizationDeveloperSettings.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['applications', "/organizations/" + orgId + "/sentry-apps/"]];
    };
    OrganizationDeveloperSettings.prototype.renderInternalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var integrations = this.state.applications.filter(function (app) { return app.status === 'internal'; });
        var isEmpty = integrations.length === 0;
        var action = (<Button priority="primary" size="small" to={"/settings/" + orgId + "/developer-settings/new-internal/"} icon={<IconAdd size="xs" isCircled/>}>
        {t('New Internal Integration')}
      </Button>);
        return (<Panel>
        <PanelHeader hasButtons>
          {t('Internal Integrations')}
          {action}
        </PanelHeader>
        <PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<EmptyMessage>
              {t('No internal integrations have been created yet.')}
            </EmptyMessage>)}
        </PanelBody>
      </Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderExernalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var integrations = this.state.applications.filter(function (app) { return app.status !== 'internal'; });
        var isEmpty = integrations.length === 0;
        var action = (<Button priority="primary" size="small" to={"/settings/" + orgId + "/developer-settings/new-public/"} icon={<IconAdd size="xs" isCircled/>}>
        {t('New Public Integration')}
      </Button>);
        return (<Panel>
        <PanelHeader hasButtons>
          {t('Public Integrations')}
          {action}
        </PanelHeader>
        <PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<EmptyMessage>
              {t('No public integrations have been created yet.')}
            </EmptyMessage>)}
        </PanelBody>
      </Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderBody = function () {
        return (<div>
        <SettingsPageHeader title={t('Developer Settings')}/>
        <AlertLink href="https://docs.sentry.io/workflow/integrations/integration-platform/">
          {t('Have questions about the Integration Platform? Learn more about it in our docs.')}
        </AlertLink>
        {this.renderExernalIntegrations()}
        {this.renderInternalIntegrations()}
      </div>);
    };
    OrganizationDeveloperSettings.propTypes = {
        organization: SentryTypes.Organization.isRequired,
    };
    return OrganizationDeveloperSettings;
}(AsyncView));
export default withOrganization(OrganizationDeveloperSettings);
//# sourceMappingURL=index.jsx.map