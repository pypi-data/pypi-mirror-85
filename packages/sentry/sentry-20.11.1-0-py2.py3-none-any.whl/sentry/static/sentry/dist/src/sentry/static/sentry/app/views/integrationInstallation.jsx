import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import { trackIntegrationEvent, getIntegrationFeatureGate, } from 'app/utils/integrationUtil';
import AddIntegration from 'app/views/organizationIntegrations/addIntegration';
import Alert from 'app/components/alert';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Field from 'app/views/settings/components/forms/field';
import { IconFlag } from 'app/icons';
import NarrowLayout from 'app/components/narrowLayout';
import SelectControl from 'app/components/forms/selectControl';
var IntegrationInstallation = /** @class */ (function (_super) {
    __extends(IntegrationInstallation, _super);
    function IntegrationInstallation() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onInstall = function (data) {
            var organization = _this.state.organization;
            var orgId = organization && organization.slug;
            _this.props.router.push("/settings/" + orgId + "/integrations/" + data.provider.key + "/" + data.id);
        };
        _this.onSelectOrg = function (_a) {
            var orgId = _a.value;
            _this.setState({ selectedOrg: orgId, reloading: true });
            var reloading = false;
            _this.api.request("/organizations/" + orgId + "/", {
                success: function (organization) {
                    return _this.setState({ organization: organization, reloading: reloading }, _this.trackOpened);
                },
                error: function () {
                    _this.setState({ reloading: reloading });
                    addErrorMessage(t('Failed to retrieve organization details'));
                },
            });
            _this.api.request("/organizations/" + orgId + "/config/integrations/", {
                success: function (providers) {
                    return _this.setState({ providers: providers.providers, reloading: reloading });
                },
                error: function () {
                    _this.setState({ reloading: reloading });
                    addErrorMessage(t('Failed to retrieve integration provider details'));
                },
            });
        };
        _this.hasAccess = function (org) { return org.access.includes('org:integrations'); };
        return _this;
    }
    IntegrationInstallation.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { selectedOrg: null, organization: null, providers: [] });
    };
    IntegrationInstallation.prototype.getEndpoints = function () {
        return [['organizations', '/organizations/']];
    };
    IntegrationInstallation.prototype.getTitle = function () {
        return t('Choose Installation Organization');
    };
    IntegrationInstallation.prototype.trackOpened = function () {
        var organization = this.state.organization;
        var provider = this.provider;
        //should have these set but need to make TS happy
        if (!organization || !provider) {
            return;
        }
        //TODO: Probably don't need this event anymore
        trackIntegrationEvent({
            eventKey: 'integrations.install_modal_opened',
            eventName: 'Integrations: Install Modal Opened',
            integration_type: 'first_party',
            integration: provider.key,
            //We actually don't know if it's installed but neither does the user in the view and multiple installs is possible
            already_installed: false,
            view: 'external_install',
        }, organization, { startSession: true });
    };
    Object.defineProperty(IntegrationInstallation.prototype, "provider", {
        get: function () {
            var _this = this;
            return this.state.providers.find(function (p) { return p.key === _this.props.params.providerId; });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationInstallation.prototype.renderAddButton = function () {
        var _this = this;
        var _a = this.state, organization = _a.organization, reloading = _a.reloading;
        var installationId = this.props.params.installationId;
        var AddButton = function (p) { return (<Button priority="primary" busy={reloading} {...p}>
        Install Integration
      </Button>); };
        if (!this.provider) {
            return <AddButton disabled/>;
        }
        return (<AddIntegration provider={this.provider} onInstall={this.onInstall}>
        {function (addIntegration) { return (<AddButton disabled={!!organization && !_this.hasAccess(organization)} onClick={function () { return addIntegration({ installation_id: installationId }); }}/>); }}
      </AddIntegration>);
    };
    IntegrationInstallation.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, organization = _a.organization, selectedOrg = _a.selectedOrg;
        var choices = this.state.organizations.map(function (org) { return [
            org.slug,
            org.slug,
        ]; });
        var FeatureList = getIntegrationFeatureGate().FeatureList;
        return (<NarrowLayout>
        <h3>{t('Finish integration installation')}</h3>
        <p>
          {tct("Please pick a specific [organization:organization] to link with\n            your integration installation.", {
            organization: <strong />,
        })}
        </p>

        {selectedOrg && organization && !this.hasAccess(organization) && (<Alert type="error" icon={<IconFlag size="md"/>}>
            <p>
              {tct("You do not have permission to install integrations in\n                  [organization]. Ask an organization owner or manager to\n                  visit this page to finish installing this integration.", { organization: <strong>{organization.slug}</strong> })}
            </p>
            <InstallLink>{window.location.href}</InstallLink>
          </Alert>)}

        {this.provider && organization && this.hasAccess(organization) && FeatureList && (<React.Fragment>
            <p>
              {tct('The following features will be available for [organization] when installed.', { organization: <strong>{organization.slug}</strong> })}
            </p>
            <FeatureList organization={organization} features={this.provider.metadata.features} provider={this.provider}/>
          </React.Fragment>)}

        <Field label={t('Organization')} inline={false} stacked required>
          {function () { return (<SelectControl deprecatedSelectControl onChange={_this.onSelectOrg} value={selectedOrg} placeholder={t('Select an organization')} options={choices.map(function (_a) {
            var _b = __read(_a, 2), value = _b[0], label = _b[1];
            return ({ value: value, label: label });
        })}/>); }}
        </Field>

        <div className="form-actions">{this.renderAddButton()}</div>
      </NarrowLayout>);
    };
    return IntegrationInstallation;
}(AsyncView));
export default IntegrationInstallation;
var InstallLink = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"], ["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"])));
var templateObject_1;
//# sourceMappingURL=integrationInstallation.jsx.map