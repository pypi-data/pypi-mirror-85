import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { urlEncode } from '@sentry/utils';
import { components } from 'react-select';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import { trackIntegrationEvent, getIntegrationFeatureGate, } from 'app/utils/integrationUtil';
import { singleLineRenderer } from 'app/utils/marked';
import Alert from 'app/components/alert';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Field from 'app/views/settings/components/forms/field';
import NarrowLayout from 'app/components/narrowLayout';
import SelectControl from 'app/components/forms/selectControl';
import IdBadge from 'app/components/idBadge';
import { IconFlag } from 'app/icons';
import LoadingIndicator from 'app/components/loadingIndicator';
var IntegrationOrganizationLink = /** @class */ (function (_super) {
    __extends(IntegrationOrganizationLink, _super);
    function IntegrationOrganizationLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.trackIntegrationEvent = function (options, startSession) {
            var _a = _this.state, organization = _a.organization, provider = _a.provider;
            //should have these set but need to make TS happy
            if (!organization || !provider) {
                return;
            }
            trackIntegrationEvent(__assign(__assign({}, options), { integration_type: 'first_party', integration: provider.key, 
                //We actually don't know if it's installed but neither does the user in the view and multiple installs is possible
                already_installed: false, view: 'external_install' }), organization, { startSession: !!startSession });
        };
        _this.getOrgBySlug = function (orgSlug) {
            return _this.state.organizations.find(function (org) { return org.slug === orgSlug; });
        };
        _this.onSelectOrg = function (_a) {
            var orgSlug = _a.value;
            return __awaiter(_this, void 0, void 0, function () {
                var _b, organization, providers, _err_1;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            this.setState({ selectedOrgSlug: orgSlug, reloading: true, organization: undefined });
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, Promise.all([
                                    this.api.requestPromise("/organizations/" + orgSlug + "/"),
                                    this.api.requestPromise("/organizations/" + orgSlug + "/config/integrations/?provider_key=" + this.integrationSlug),
                                ])];
                        case 2:
                            _b = __read.apply(void 0, [_c.sent(), 2]), organization = _b[0], providers = _b[1].providers;
                            // should never happen with a valid provider
                            if (providers.length === 0) {
                                throw new Error('Invalid provider');
                            }
                            this.setState({ organization: organization, reloading: false, provider: providers[0] }, this.trackOpened);
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _c.sent();
                            addErrorMessage(t('Failed to retrieve organization or integration details'));
                            this.setState({ reloading: false });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        _this.hasAccess = function () {
            var organization = _this.state.organization;
            return organization === null || organization === void 0 ? void 0 : organization.access.includes('org:integrations');
        };
        _this.customOption = function (orgProps) {
            var organization = _this.getOrgBySlug(orgProps.value);
            if (!organization) {
                return null;
            }
            return (<components.Option {...orgProps}>
        <IdBadge organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </components.Option>);
        };
        _this.customValueContainer = function (containerProps) {
            var valueList = containerProps.getValue();
            //if no value set, we want to return the default component that is rendered
            if (valueList.length === 0) {
                return <components.ValueContainer {...containerProps}/>;
            }
            var orgSlug = valueList[0].value;
            var organization = _this.getOrgBySlug(orgSlug);
            if (!organization) {
                return <components.ValueContainer {...containerProps}/>;
            }
            return (<components.ValueContainer {...containerProps}>
        <IdBadge organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </components.ValueContainer>);
        };
        return _this;
    }
    IntegrationOrganizationLink.prototype.getEndpoints = function () {
        return [['organizations', '/organizations/']];
    };
    IntegrationOrganizationLink.prototype.getTitle = function () {
        return t('Choose Installation Organization');
    };
    IntegrationOrganizationLink.prototype.trackOpened = function () {
        this.trackIntegrationEvent({
            eventKey: 'integrations.integration_viewed',
            eventName: 'Integrations: Integration Viewed',
        }, true);
    };
    IntegrationOrganizationLink.prototype.trackInstallationStart = function () {
        this.trackIntegrationEvent({
            eventKey: 'integrations.installation_start',
            eventName: 'Integrations: Installation Start',
        });
    };
    Object.defineProperty(IntegrationOrganizationLink.prototype, "integrationSlug", {
        get: function () {
            return this.props.params.integrationSlug;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationOrganizationLink.prototype, "queryParams", {
        get: function () {
            return this.props.location.query;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationOrganizationLink.prototype.onLoadAllEndpointsSuccess = function () {
        //auto select the org if there is only one
        var organizations = this.state.organizations;
        if (organizations.length === 1) {
            this.onSelectOrg({ value: organizations[0].slug });
        }
    };
    IntegrationOrganizationLink.prototype.renderAddButton = function (onClick) {
        var _this = this;
        var _a = this.state, organization = _a.organization, provider = _a.provider;
        // should never happen but we need this check for TS
        if (!provider || !organization) {
            return null;
        }
        var features = provider.metadata.features;
        // Prepare the features list
        var featuresComponents = features.map(function (f) { return ({
            featureGate: f.featureGate,
            description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: singleLineRenderer(f.description) }}/>),
        }); });
        var IntegrationDirectoryFeatures = getIntegrationFeatureGate().IntegrationDirectoryFeatures;
        return (<IntegrationDirectoryFeatures organization={organization} features={featuresComponents}>
        {function (_a) {
            var disabled = _a.disabled;
            return (<ButtonWrapper>
            <Button priority="primary" disabled={!_this.hasAccess() || disabled} onClick={onClick}>
              {t('Install %s', provider.name)}
            </Button>
          </ButtonWrapper>);
        }}
      </IntegrationDirectoryFeatures>);
    };
    IntegrationOrganizationLink.prototype.renderAddButtonContainer = function () {
        var _this = this;
        // TOOD: Implement for Github
        if (this.props.params.installationId) {
            throw new Error('Not implemented yet');
        }
        return this.renderAddButton(function () {
            // add the selected org to the query parameters and then redirect back to configure
            var selectedOrgSlug = _this.state.selectedOrgSlug;
            var query = __assign({ orgSlug: selectedOrgSlug }, _this.queryParams);
            _this.trackInstallationStart();
            window.location.assign("/extensions/" + _this.integrationSlug + "/configure/?" + urlEncode(query));
        });
    };
    IntegrationOrganizationLink.prototype.renderBottom = function () {
        var _a = this.state, organization = _a.organization, selectedOrgSlug = _a.selectedOrgSlug, provider = _a.provider, reloading = _a.reloading;
        var FeatureList = getIntegrationFeatureGate().FeatureList;
        if (reloading) {
            return <LoadingIndicator />;
        }
        return (<React.Fragment>
        {selectedOrgSlug && organization && !this.hasAccess() && (<Alert type="error" icon={<IconFlag size="md"/>}>
            <p>
              {tct("You do not have permission to install integrations in\n                [organization]. Ask an organization owner or manager to\n                visit this page to finish installing this integration.", { organization: <strong>{organization.slug}</strong> })}
            </p>
            <InstallLink>{window.location.href}</InstallLink>
          </Alert>)}

        {provider && organization && this.hasAccess() && FeatureList && (<React.Fragment>
            <p>
              {tct('The following features will be available for [organization] when installed.', { organization: <strong>{organization.slug}</strong> })}
            </p>
            <FeatureList organization={organization} features={provider.metadata.features} provider={provider}/>
          </React.Fragment>)}

        <div className="form-actions">{this.renderAddButtonContainer()}</div>
      </React.Fragment>);
    };
    IntegrationOrganizationLink.prototype.renderBody = function () {
        var selectedOrgSlug = this.state.selectedOrgSlug;
        var options = this.state.organizations.map(function (org) { return ({
            value: org.slug,
            label: org.name,
        }); });
        return (<NarrowLayout>
        <h3>{t('Finish integration installation')}</h3>
        <p>
          {tct("Please pick a specific [organization:organization] to link with\n            your integration installation of [integation].", {
            organization: <strong />,
            integation: <strong>{this.integrationSlug}</strong>,
        })}
        </p>

        <Field label={t('Organization')} inline={false} stacked required>
          <SelectControl onChange={this.onSelectOrg} value={selectedOrgSlug} placeholder={t('Select an organization')} options={options} components={{
            Option: this.customOption,
            ValueContainer: this.customValueContainer,
        }}/>
        </Field>
        {this.renderBottom()}
      </NarrowLayout>);
    };
    return IntegrationOrganizationLink;
}(AsyncView));
export default IntegrationOrganizationLink;
var InstallLink = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"], ["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"])));
var FeatureListItem = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var ButtonWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=integrationOrganizationLink.jsx.map