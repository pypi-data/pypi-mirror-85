import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import Form from 'app/views/settings/components/forms/form';
import AsyncView from 'app/views/asyncView';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { updateOrganization } from 'app/actionCreators/organizations';
import organizationSecurityAndPrivacyGroups from 'app/data/forms/organizationSecurityAndPrivacyGroups';
import withOrganization from 'app/utils/withOrganization';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import DataScrubbing from '../components/dataScrubbing';
var OrganizationSecurityAndPrivacyContent = /** @class */ (function (_super) {
    __extends(OrganizationSecurityAndPrivacyContent, _super);
    function OrganizationSecurityAndPrivacyContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateOrganization = function (data) {
            // This will update OrganizationStore (as well as OrganizationsStore
            // which is slightly incorrect because it has summaries vs a detailed org)
            updateOrganization(data);
        };
        return _this;
    }
    OrganizationSecurityAndPrivacyContent.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['authProvider', "/organizations/" + orgId + "/auth-provider/"]];
    };
    OrganizationSecurityAndPrivacyContent.prototype.renderBody = function () {
        var organization = this.props.organization;
        var orgId = this.props.params.orgId;
        var initialData = organization;
        var endpoint = "/organizations/" + orgId + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = organization.relayPiiConfig;
        var authProvider = this.state.authProvider;
        var title = t('Security & Privacy');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={organization.slug}/>
        <SettingsPageHeader title={title}/>
        <Form data-test-id="organization-settings-security-and-privacy" apiMethod="PUT" apiEndpoint={endpoint} initialData={initialData} additionalFieldProps={{ hasSsoEnabled: !!authProvider }} onSubmitSuccess={this.handleUpdateOrganization} onSubmitError={function () { return addErrorMessage(t('Unable to save change')); }} saveOnBlur allowUndo>
          <JsonForm features={features} forms={organizationSecurityAndPrivacyGroups} disabled={!access.has('org:write')}/>
        </Form>
        <DataScrubbing additionalContext={t('These rules can be configured for each project.')} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('org:write')} organization={organization} onSubmitSuccess={this.handleUpdateOrganization}/>
      </React.Fragment>);
    };
    return OrganizationSecurityAndPrivacyContent;
}(AsyncView));
export default withOrganization(OrganizationSecurityAndPrivacyContent);
//# sourceMappingURL=index.jsx.map