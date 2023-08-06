import { __extends } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import { t } from 'app/locale';
import ApiForm from 'app/views/settings/components/forms/apiForm';
import BooleanField from 'app/views/settings/components/forms/booleanField';
import FormField from 'app/views/settings/components/forms/formField';
import TextField from 'app/views/settings/components/forms/textField';
import MultipleCheckbox from 'app/views/settings/components/forms/controls/multipleCheckbox';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
var EVENT_CHOICES = ['event.alert', 'event.created'].map(function (e) { return [e, e]; });
var ServiceHookSettingsForm = /** @class */ (function (_super) {
    __extends(ServiceHookSettingsForm, _super);
    function ServiceHookSettingsForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onSubmitSuccess = function () {
            var _a = _this.props, orgId = _a.orgId, projectId = _a.projectId;
            browserHistory.push("/settings/" + orgId + "/projects/" + projectId + "/hooks/");
        };
        return _this;
    }
    ServiceHookSettingsForm.prototype.render = function () {
        var _a = this.props, initialData = _a.initialData, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        var endpoint = hookId
            ? "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/"
            : "/projects/" + orgId + "/" + projectId + "/hooks/";
        return (<Panel>
        <ApiForm apiMethod={hookId ? 'PUT' : 'POST'} apiEndpoint={endpoint} initialData={initialData} onSubmitSuccess={this.onSubmitSuccess} footerStyle={{
            marginTop: 0,
            paddingRight: 20,
        }} submitLabel={hookId ? t('Save Changes') : t('Create Hook')}>
          <PanelHeader>{t('Hook Configuration')}</PanelHeader>
          <PanelBody>
            <BooleanField name="isActive" label={t('Active')}/>
            <TextField name="url" label={t('URL')} required help={t('The URL which will receive events.')}/>
            <FormField name="events" label={t('Events')} inline={false} help={t('The event types you wish to subscribe to.')}>
              {function (_a) {
            var value = _a.value, onChange = _a.onChange;
            return (<MultipleCheckbox onChange={onChange} value={value} choices={EVENT_CHOICES}/>);
        }}
            </FormField>
          </PanelBody>
        </ApiForm>
      </Panel>);
    };
    return ServiceHookSettingsForm;
}(React.Component));
export default ServiceHookSettingsForm;
//# sourceMappingURL=serviceHookSettingsForm.jsx.map