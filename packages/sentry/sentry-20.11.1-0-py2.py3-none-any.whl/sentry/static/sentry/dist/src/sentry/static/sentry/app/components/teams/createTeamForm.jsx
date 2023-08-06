import { __extends } from "tslib";
import React from 'react';
import { callIfFunction } from 'app/utils/callIfFunction';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import TextField from 'app/views/settings/components/forms/textField';
import slugify from 'app/utils/slugify';
var CreateTeamForm = /** @class */ (function (_super) {
    __extends(CreateTeamForm, _super);
    function CreateTeamForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (data, onSuccess, onError) {
            callIfFunction(_this.props.onSubmit, data, onSuccess, onError);
        };
        _this.handleCreateTeamSuccess = function (data) {
            callIfFunction(_this.props.onSuccess, data);
        };
        return _this;
    }
    CreateTeamForm.prototype.render = function () {
        var organization = this.props.organization;
        return (<React.Fragment>
        <p>
          {t('Members of a team have access to specific areas, such as a new release or a new application feature.')}
        </p>

        <Form submitLabel={t('Create Team')} apiEndpoint={"/organizations/" + organization.slug + "/teams/"} apiMethod="POST" onSubmit={this.handleSubmit} onSubmitSuccess={this.handleCreateTeamSuccess} requireChanges data-test-id="create-team-form" {...this.props.formProps}>
          <TextField name="slug" label={t('Team Name')} placeholder={t('e.g. operations, web-frontend, desktop')} help={t('May contain lowercase letters, numbers, dashes and underscores.')} required stacked flexibleControlStateSize inline={false} transformInput={slugify}/>
        </Form>
      </React.Fragment>);
    };
    return CreateTeamForm;
}(React.Component));
export default CreateTeamForm;
//# sourceMappingURL=createTeamForm.jsx.map