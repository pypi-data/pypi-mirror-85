import { __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { Form, FormState } from 'app/components/forms';
import DefaultSettings from 'app/plugins/components/settings';
import LoadingIndicator from 'app/components/loadingIndicator';
var Settings = /** @class */ (function (_super) {
    __extends(Settings, _super);
    function Settings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.REQUIRED_FIELDS = ['account_email', 'api_token', 'website_id'];
        _this.ON_PREMISES_FIELDS = ['api_url', 'player_url'];
        _this.toggleOnPremisesConfiguration = function () {
            _this.setState({
                showOnPremisesConfiguration: !_this.state.showOnPremisesConfiguration,
            });
        };
        return _this;
    }
    Settings.prototype.renderFields = function (fields) {
        var _this = this;
        return fields === null || fields === void 0 ? void 0 : fields.map(function (f) {
            return _this.renderField({
                config: f,
                formData: _this.state.formData,
                formErrors: _this.state.errors,
                onChange: _this.changeField.bind(_this, f.name),
            });
        });
    };
    Settings.prototype.filterFields = function (fields, fieldNames) {
        var _a;
        return (_a = fields === null || fields === void 0 ? void 0 : fields.filter(function (field) { return fieldNames.includes(field.name); })) !== null && _a !== void 0 ? _a : [];
    };
    Settings.prototype.render = function () {
        if (this.state.state === FormState.LOADING) {
            return <LoadingIndicator />;
        }
        if (this.state.state === FormState.ERROR && !this.state.fieldList) {
            return (<div className="alert alert-error m-b-1">
          An unknown error occurred. Need help with this?{' '}
          <a href="https://sentry.io/support/">Contact support</a>
        </div>);
        }
        var isSaving = this.state.state === FormState.SAVING;
        var hasChanges = !isEqual(this.state.initialData, this.state.formData);
        var requiredFields = this.filterFields(this.state.fieldList, this.REQUIRED_FIELDS);
        var onPremisesFields = this.filterFields(this.state.fieldList, this.ON_PREMISES_FIELDS);
        return (<Form onSubmit={this.onSubmit} submitDisabled={isSaving || !hasChanges}>
        {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
            <ul>
              <li>{this.state.errors.__all__}</li>
            </ul>
          </div>)}
        {this.renderFields(requiredFields)}
        {onPremisesFields.length > 0 ? (<div className="control-group">
            <button className="btn btn-default" type="button" onClick={this.toggleOnPremisesConfiguration}>
              Configure on-premises
            </button>
          </div>) : null}
        {this.state.showOnPremisesConfiguration
            ? this.renderFields(onPremisesFields)
            : null}
      </Form>);
    };
    return Settings;
}(DefaultSettings));
export default Settings;
//# sourceMappingURL=settings.jsx.map