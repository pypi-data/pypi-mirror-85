import { __assign, __extends } from "tslib";
import React from 'react';
import { Form, FormState } from 'app/components/forms';
import DefaultIssueActions from 'app/plugins/components/issueActions';
var IssueActions = /** @class */ (function (_super) {
    __extends(IssueActions, _super);
    function IssueActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.changeField = function (action, name, value) {
            var _a, _b;
            var key = _this.getFormDataKey(action);
            var formData = __assign(__assign({}, _this.state[key]), (_a = {}, _a[name] = value, _a));
            var state = __assign(__assign({}, _this.state), (_b = {}, _b[key] = formData, _b));
            if (name === 'issuetype') {
                state.state = FormState.LOADING;
                _this.setState(state, _this.onLoad.bind(_this, function () {
                    _this.api.request(_this.getPluginCreateEndpoint() + '?issuetype=' + encodeURIComponent(value), {
                        success: function (data) {
                            // Try not to change things the user might have edited
                            // unless they're no longer valid
                            var oldData = _this.state.createFormData;
                            var createFormData = {};
                            data === null || data === void 0 ? void 0 : data.forEach(function (field) {
                                var val;
                                if (field.choices &&
                                    !field.choices.find(function (c) { return c[0] === oldData[field.name]; })) {
                                    val = field.default;
                                }
                                else {
                                    val = oldData[field.name] || field.default;
                                }
                                createFormData[field.name] = val;
                            });
                            _this.setState({
                                createFieldList: data,
                                error: undefined,
                                loading: false,
                                createFormData: createFormData,
                            }, _this.onLoadSuccess);
                        },
                        error: _this.errorHandler,
                    });
                }));
                return;
            }
            _this.setState(state);
        };
        return _this;
    }
    IssueActions.prototype.renderForm = function () {
        var _this = this;
        var form = null;
        // For create form, split into required and optional fields
        if (this.props.actionType === 'create') {
            if (this.state.createFieldList) {
                var renderField_1 = function (field) {
                    if (field.has_autocomplete) {
                        field = Object.assign({
                            url: '/api/0/issues/' +
                                _this.getGroup().id +
                                '/plugins/' +
                                _this.props.plugin.slug +
                                '/autocomplete',
                        }, field);
                    }
                    return (<div key={field.name}>
              {_this.renderField({
                        config: field,
                        formData: _this.state.createFormData,
                        onChange: _this.changeField.bind(_this, 'create', field.name),
                    })}
            </div>);
                };
                var isRequired_1 = function (f) { return (f.required !== null ? f.required : true); };
                var fields = this.state.createFieldList;
                var requiredFields = fields.filter(function (f) { return isRequired_1(f); }).map(function (f) { return renderField_1(f); });
                var optionalFields = fields
                    .filter(function (f) { return !isRequired_1(f); })
                    .map(function (f) { return renderField_1(f); });
                form = (<Form onSubmit={this.createIssue} submitLabel="Create Issue" footerClass="">
            <h5>Required Fields</h5>
            {requiredFields}
            {optionalFields.length ? <h5>Optional Fields</h5> : null}
            {optionalFields}
          </Form>);
            }
        }
        else {
            form = _super.prototype.renderForm.call(this);
        }
        return form;
    };
    return IssueActions;
}(DefaultIssueActions));
export default IssueActions;
//# sourceMappingURL=issueActions.jsx.map