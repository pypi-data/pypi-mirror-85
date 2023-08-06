import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import ExternalLink from 'app/components/links/externalLink';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import { updateOrganization } from 'app/actionCreators/organizations';
import withOrganization from 'app/utils/withOrganization';
var fields = [
    {
        title: t('General'),
        fields: [
            {
                name: 'apdexThreshold',
                type: 'number',
                required: true,
                label: t('Response Time Threshold (Apdex)'),
                help: tct("Set a response time threshold in milliseconds to help define what satisfactory\n                and tolerable response times are. This value will be reflected in the\n                calculation of your [link:Apdex], a standard measurement in performance.", {
                    link: (<ExternalLink href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                }),
            },
        ],
    },
];
var OrganizationPerformance = /** @class */ (function (_super) {
    __extends(OrganizationPerformance, _super);
    function OrganizationPerformance() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSuccess = function (data) {
            updateOrganization(data);
        };
        return _this;
    }
    OrganizationPerformance.prototype.render = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var features = new Set(organization.features);
        var access = new Set(organization.access);
        var endpoint = "/organizations/" + organization.slug + "/";
        var jsonFormSettings = {
            location: location,
            features: features,
            access: access,
            disabled: !(access.has('org:write') && features.has('performance-view')),
        };
        return (<React.Fragment>
        <SettingsPageHeader title="Performance"/>
        <PermissionAlert />

        <Form data-test-id="organization-performance-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={organization} onSubmitSuccess={this.handleSuccess} onSubmitError={function () { return addErrorMessage('Unable to save changes'); }}>
          <JsonForm {...jsonFormSettings} forms={fields}/>
        </Form>
      </React.Fragment>);
    };
    return OrganizationPerformance;
}(React.Component));
export default withOrganization(OrganizationPerformance);
//# sourceMappingURL=index.jsx.map