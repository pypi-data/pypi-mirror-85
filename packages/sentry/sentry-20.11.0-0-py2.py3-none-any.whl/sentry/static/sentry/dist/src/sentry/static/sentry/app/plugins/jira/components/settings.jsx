import { __assign, __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { Form, FormState } from 'app/components/forms';
import DefaultSettings from 'app/plugins/components/settings';
import LoadingIndicator from 'app/components/loadingIndicator';
var PAGE_FIELD_LIST = {
    0: ['instance_url', 'username', 'password'],
    1: ['default_project'],
    2: ['ignored_fields', 'default_priority', 'default_issue_type', 'auto_create'],
};
var Settings = /** @class */ (function (_super) {
    __extends(Settings, _super);
    function Settings(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.isLastPage = function () {
            return _this.state.page === 2;
        };
        _this.startEditing = function () {
            _this.setState({ editing: true });
        };
        _this.back = function (ev) {
            ev.preventDefault();
            if (_this.state.state === FormState.SAVING) {
                return;
            }
            _this.setState({
                page: _this.state.page - 1,
            });
        };
        Object.assign(_this.state, {
            page: 0,
        });
        return _this;
    }
    Settings.prototype.isConfigured = function () {
        return !!(this.state.formData && this.state.formData.default_project);
    };
    Settings.prototype.fetchData = function () {
        var _this = this;
        // This is mostly copy paste of parent class
        // except for setting edit state
        this.api.request(this.getPluginEndpoint(), {
            success: function (data) {
                var formData = {};
                var initialData = {};
                data.config.forEach(function (field) {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                });
                _this.setState({
                    fieldList: data.config,
                    formData: formData,
                    initialData: initialData,
                    // start off in edit mode if there isn't a project set
                    editing: !(formData && formData.default_project),
                }, _this.onLoadSuccess);
            },
            error: this.onLoadError,
        });
    };
    Settings.prototype.onSubmit = function () {
        var _this = this;
        var _a;
        if (isEqual(this.state.initialData, this.state.formData)) {
            if (this.isLastPage()) {
                this.setState({ editing: false, page: 0 });
            }
            else {
                this.setState({ page: this.state.page + 1 });
            }
            this.onSaveSuccess(this.onSaveComplete);
            return;
        }
        var body = Object.assign({}, this.state.formData);
        // if the project has changed, it's likely these values aren't valid anymore
        if (body.default_project !== ((_a = this.state.initialData) === null || _a === void 0 ? void 0 : _a.default_project)) {
            body.default_issue_type = null;
            body.default_priority = null;
        }
        this.api.request(this.getPluginEndpoint(), {
            data: body,
            method: 'PUT',
            success: this.onSaveSuccess.bind(this, function (data) {
                var formData = {};
                var initialData = {};
                data.config.forEach(function (field) {
                    formData[field.name] = field.value || field.defaultValue;
                    initialData[field.name] = field.value;
                });
                var state = {
                    formData: formData,
                    initialData: initialData,
                    errors: {},
                    fieldList: data.config,
                    page: _this.state.page,
                    editing: _this.state.editing,
                };
                if (_this.isLastPage()) {
                    state.editing = false;
                    state.page = 0;
                }
                else {
                    state.page = _this.state.page + 1;
                }
                _this.setState(state);
            }),
            error: this.onSaveError.bind(this, function (error) {
                _this.setState({
                    errors: (error.responseJSON || {}).errors || {},
                });
            }),
            complete: this.onSaveComplete,
        });
    };
    Settings.prototype.render = function () {
        var _this = this;
        var _a, _b;
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
        var fields;
        var onSubmit;
        var submitLabel;
        if (this.state.editing) {
            fields = (_a = this.state.fieldList) === null || _a === void 0 ? void 0 : _a.filter(function (f) {
                return PAGE_FIELD_LIST[_this.state.page].includes(f.name);
            });
            onSubmit = this.onSubmit;
            submitLabel = this.isLastPage() ? 'Finish' : 'Save and Continue';
        }
        else {
            fields = (_b = this.state.fieldList) === null || _b === void 0 ? void 0 : _b.map(function (f) { return (__assign(__assign({}, f), { readonly: true })); });
            onSubmit = this.startEditing;
            submitLabel = 'Edit';
        }
        return (<Form onSubmit={onSubmit} submitDisabled={isSaving} submitLabel={submitLabel} extraButton={this.state.page === 0 ? null : (<a href="#" className={'btn btn-default pull-left' + (isSaving ? ' disabled' : '')} onClick={this.back}>
              Back
            </a>)}>
        {this.state.errors.__all__ && (<div className="alert alert-block alert-error">
            <ul>
              <li>{this.state.errors.__all__}</li>
            </ul>
          </div>)}
        {fields === null || fields === void 0 ? void 0 : fields.map(function (f) {
            return _this.renderField({
                config: f,
                formData: _this.state.formData,
                formErrors: _this.state.errors,
                onChange: _this.changeField.bind(_this, f.name),
            });
        })}
      </Form>);
    };
    return Settings;
}(DefaultSettings));
export default Settings;
//# sourceMappingURL=settings.jsx.map