import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { updateOrganization } from 'app/actionCreators/organizations';
import AsyncComponent from 'app/components/asyncComponent';
import AvatarChooser from 'app/components/avatarChooser';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import organizationSettingsFields from 'app/data/forms/organizationGeneralSettings';
import withOrganization from 'app/utils/withOrganization';
var OrganizationSettingsForm = /** @class */ (function (_super) {
    __extends(OrganizationSettingsForm, _super);
    function OrganizationSettingsForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationSettingsForm.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [['authProvider', "/organizations/" + organization.slug + "/auth-provider/"]];
    };
    OrganizationSettingsForm.prototype.render = function () {
        var _a = this.props, initialData = _a.initialData, organization = _a.organization, onSave = _a.onSave, access = _a.access;
        var authProvider = this.state.authProvider;
        var endpoint = "/organizations/" + organization.slug + "/";
        var jsonFormSettings = {
            additionalFieldProps: { hasSsoEnabled: !!authProvider },
            features: new Set(organization.features),
            access: access,
            location: this.props.location,
            disabled: !access.has('org:write'),
        };
        return (<Form data-test-id="organization-settings" apiMethod="PUT" apiEndpoint={endpoint} saveOnBlur allowUndo initialData={initialData} onSubmitSuccess={function (_resp, model) {
            // Special case for slug, need to forward to new slug
            if (typeof onSave === 'function') {
                onSave(initialData, model.initialData);
            }
        }} onSubmitError={function () { return addErrorMessage('Unable to save change'); }}>
        <JsonForm {...jsonFormSettings} forms={organizationSettingsFields}/>
        <AvatarChooser type="organization" allowGravatar={false} endpoint={endpoint + "avatar/"} model={initialData} onSave={updateOrganization} disabled={!access.has('org:write')}/>
      </Form>);
    };
    return OrganizationSettingsForm;
}(AsyncComponent));
export default withOrganization(OrganizationSettingsForm);
//# sourceMappingURL=organizationSettingsForm.jsx.map