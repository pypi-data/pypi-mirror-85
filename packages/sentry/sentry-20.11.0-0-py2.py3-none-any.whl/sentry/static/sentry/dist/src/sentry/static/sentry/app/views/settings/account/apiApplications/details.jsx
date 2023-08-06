import { __extends } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import ConfigStore from 'app/stores/configStore';
import Form from 'app/views/settings/components/forms/form';
import FormField from 'app/views/settings/components/forms/formField';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import apiApplication from 'app/data/forms/apiApplication';
import getDynamicText from 'app/utils/getDynamicText';
var ApiApplicationsDetails = /** @class */ (function (_super) {
    __extends(ApiApplicationsDetails, _super);
    function ApiApplicationsDetails() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ApiApplicationsDetails.prototype.getEndpoints = function () {
        return [['app', "/api-applications/" + this.props.params.appId + "/"]];
    };
    ApiApplicationsDetails.prototype.getTitle = function () {
        return t('Application Details');
    };
    ApiApplicationsDetails.prototype.renderBody = function () {
        var urlPrefix = ConfigStore.get('urlPrefix');
        return (<div>
        <SettingsPageHeader title={this.getTitle()}/>

        <Form apiMethod="PUT" apiEndpoint={"/api-applications/" + this.props.params.appId + "/"} saveOnBlur allowUndo initialData={this.state.app} onSubmitError={function () { return addErrorMessage('Unable to save change'); }}>
          <JsonForm location={this.props.location} forms={apiApplication}/>

          <Panel>
            <PanelHeader>{t('Credentials')}</PanelHeader>

            <PanelBody>
              <FormField name="clientID" label="Client ID">
                {function (_a) {
            var value = _a.value;
            return (<div>
                    <TextCopyInput>
                      {getDynamicText({ value: value, fixed: 'CI_CLIENT_ID' })}
                    </TextCopyInput>
                  </div>);
        }}
              </FormField>

              <FormField name="clientSecret" label="Client Secret" help={t("Your secret is only available briefly after application creation. Make\n                  sure to save this value!")}>
                {function (_a) {
            var value = _a.value;
            return value ? (<TextCopyInput>
                      {getDynamicText({ value: value, fixed: 'CI_CLIENT_SECRET' })}
                    </TextCopyInput>) : (<em>hidden</em>);
        }}
              </FormField>

              <FormField name="" label="Authorization URL">
                {function () { return <TextCopyInput>{urlPrefix + "/oauth/authorize/"}</TextCopyInput>; }}
              </FormField>

              <FormField name="" label="Token URL">
                {function () { return <TextCopyInput>{urlPrefix + "/oauth/token/"}</TextCopyInput>; }}
              </FormField>
            </PanelBody>
          </Panel>
        </Form>
      </div>);
    };
    return ApiApplicationsDetails;
}(AsyncView));
export default ApiApplicationsDetails;
//# sourceMappingURL=details.jsx.map