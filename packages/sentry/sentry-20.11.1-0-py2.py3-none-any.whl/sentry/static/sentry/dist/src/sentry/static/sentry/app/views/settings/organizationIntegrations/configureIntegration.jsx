import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import AddIntegration from 'app/views/organizationIntegrations/addIntegration';
import BreadcrumbTitle from 'app/views/settings/components/settingsBreadcrumb/breadcrumbTitle';
import Button from 'app/components/button';
import { IconAdd, IconArrow } from 'app/icons';
import Form from 'app/views/settings/components/forms/form';
import IntegrationAlertRules from 'app/views/organizationIntegrations/integrationAlertRules';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import IntegrationRepos from 'app/views/organizationIntegrations/integrationRepos';
import IntegrationCodeMappings from 'app/views/organizationIntegrations/integrationCodeMappings';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withOrganization from 'app/utils/withOrganization';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import { singleLineRenderer } from 'app/utils/marked';
import Alert from 'app/components/alert';
import NavTabs from 'app/components/navTabs';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
var ConfigureIntegration = /** @class */ (function (_super) {
    __extends(ConfigureIntegration, _super);
    function ConfigureIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onTabChange = function (value) {
            _this.setState({ tab: value });
        };
        _this.onUpdateIntegration = function () {
            _this.setState(_this.getDefaultState(), _this.fetchData);
        };
        _this.getAction = function (provider) {
            var integration = _this.state.integration;
            var action = provider && provider.key === 'pagerduty' ? (<AddIntegration provider={provider} onInstall={_this.onUpdateIntegration} account={integration.domainName}>
          {function (onClick) { return (<Button priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>} onClick={function () { return onClick(); }}>
              {t('Add Services')}
            </Button>); }}
        </AddIntegration>) : null;
            return action;
        };
        return _this;
    }
    ConfigureIntegration.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, integrationId = _a.integrationId;
        return [
            ['config', "/organizations/" + orgId + "/config/integrations/"],
            ['integration', "/organizations/" + orgId + "/integrations/" + integrationId + "/"],
        ];
    };
    ConfigureIntegration.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey !== 'integration') {
            return;
        }
        trackIntegrationEvent({
            eventKey: 'integrations.details_viewed',
            eventName: 'Integrations: Details Viewed',
            integration: data.provider.key,
            integration_type: 'first_party',
        }, this.props.organization);
    };
    ConfigureIntegration.prototype.getTitle = function () {
        return this.state.integration
            ? this.state.integration.provider.name
            : 'Configure Integration';
    };
    ConfigureIntegration.prototype.hasStacktraceLinking = function (provider) {
        return !!provider.hasStacktraceLinking;
    };
    Object.defineProperty(ConfigureIntegration.prototype, "tab", {
        get: function () {
            return this.state.tab || 'repos';
        },
        enumerable: false,
        configurable: true
    });
    //TODO(Steve): Refactor components into separate tabs and use more generic tab logic
    ConfigureIntegration.prototype.renderMainTab = function (provider) {
        var _a, _b, _c, _d;
        var orgId = this.props.params.orgId;
        var integration = this.state.integration;
        var instructions = (_b = (_a = integration.dynamicDisplayInformation) === null || _a === void 0 ? void 0 : _a.configure_integration) === null || _b === void 0 ? void 0 : _b.instructions;
        return (<React.Fragment>
        <BreadcrumbTitle routes={this.props.routes} title={integration.provider.name}/>

        {integration.configOrganization.length > 0 && (<Form hideFooter saveOnBlur allowUndo apiMethod="POST" initialData={integration.configData} apiEndpoint={"/organizations/" + orgId + "/integrations/" + integration.id + "/"}>
            <JsonForm fields={integration.configOrganization} title={((_c = integration.provider.aspects.configure_integration) === null || _c === void 0 ? void 0 : _c.title) ||
            t('Organization Integration Settings')}/>
          </Form>)}

        {instructions && instructions.length > 0 && (<Alert type="info">
            {(instructions === null || instructions === void 0 ? void 0 : instructions.length) === 1 ? (<span dangerouslySetInnerHTML={{ __html: singleLineRenderer(instructions[0]) }}/>) : (<List symbol={<IconArrow size="xs" direction="right"/>}>
                {(_d = instructions === null || instructions === void 0 ? void 0 : instructions.map(function (instruction, i) { return (<ListItem key={i}>
                    <span dangerouslySetInnerHTML={{ __html: singleLineRenderer(instruction) }}/>
                  </ListItem>); })) !== null && _d !== void 0 ? _d : []}
              </List>)}
          </Alert>)}

        {provider.features.includes('alert-rule') && (<IntegrationAlertRules integration={integration}/>)}

        {provider.features.includes('commits') && (<IntegrationRepos {...this.props} integration={integration}/>)}
      </React.Fragment>);
    };
    ConfigureIntegration.prototype.renderBody = function () {
        var integration = this.state.integration;
        var provider = this.state.config.providers.find(function (p) { return p.key === integration.provider.key; });
        if (!provider) {
            return null;
        }
        var title = <IntegrationItem integration={integration}/>;
        var header = (<SettingsPageHeader noTitleStyles title={title} action={this.getAction(provider)}/>);
        return (<React.Fragment>
        {header}
        {this.renderMainContent(provider)}
      </React.Fragment>);
    };
    //renders everything below header
    ConfigureIntegration.prototype.renderMainContent = function (provider) {
        var _this = this;
        var integration = this.state.integration;
        //if no code mappings, render the single tab
        if (!this.hasStacktraceLinking(provider)) {
            return this.renderMainTab(provider);
        }
        //otherwise render the tab view
        var tabs = [
            ['repos', t('Repositories')],
            ['codeMappings', t('Code Mappings')],
        ];
        return (<React.Fragment>
        <NavTabs underlined>
          {tabs.map(function (tabTuple) { return (<li key={tabTuple[0]} className={_this.tab === tabTuple[0] ? 'active' : ''} onClick={function () { return _this.onTabChange(tabTuple[0]); }}>
              <CapitalizedLink>{tabTuple[1]}</CapitalizedLink>
            </li>); })}
        </NavTabs>
        {this.tab === 'codeMappings' ? (<IntegrationCodeMappings integration={integration}/>) : (this.renderMainTab(provider))}
      </React.Fragment>);
    };
    return ConfigureIntegration;
}(AsyncView));
export default withOrganization(ConfigureIntegration);
var CapitalizedLink = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var templateObject_1;
//# sourceMappingURL=configureIntegration.jsx.map