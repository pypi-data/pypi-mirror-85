import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import FormState from 'app/components/forms/state';
import { t } from 'app/locale';
var Form = /** @class */ (function (_super) {
    __extends(Form, _super);
    function Form(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onSubmit = function (e) {
            e.preventDefault();
            if (!_this.props.onSubmit) {
                throw new Error('onSubmit is a required prop');
            }
            _this.props.onSubmit(_this.state.data, _this.onSubmitSuccess, _this.onSubmitError);
        };
        _this.onSubmitSuccess = function (data) {
            var curData = _this.state.data;
            var newData = {};
            if (data) {
                Object.keys(curData).forEach(function (k) {
                    if (data.hasOwnProperty(k)) {
                        newData[k] = data[k];
                    }
                    else {
                        newData[k] = curData[k];
                    }
                });
            }
            else {
                newData = curData;
            }
            _this.setState({
                state: FormState.READY,
                errors: {},
                initialData: newData,
            });
            _this.props.onSubmitSuccess && _this.props.onSubmitSuccess(data);
        };
        _this.onSubmitError = function (error) {
            _this.setState({
                state: FormState.ERROR,
                errors: error.responseJSON,
            });
            if (_this.props.resetOnError) {
                _this.setState({
                    initialData: {},
                });
            }
            _this.props.onSubmitError && _this.props.onSubmitError(error);
        };
        _this.onFieldChange = function (name, value) {
            _this.setState(function (state) {
                var _a;
                return ({
                    data: __assign(__assign({}, state.data), (_a = {}, _a[name] = value, _a)),
                });
            });
        };
        _this.state = {
            data: __assign({}, _this.props.initialData),
            errors: {},
            initialData: __assign({}, _this.props.initialData),
            state: FormState.READY,
        };
        return _this;
    }
    Form.prototype.getChildContext = function () {
        var _a = this.state, data = _a.data, errors = _a.errors;
        return {
            form: {
                data: data,
                errors: errors,
                onFieldChange: this.onFieldChange,
            },
        };
    };
    Form.prototype.render = function () {
        var isSaving = this.state.state === FormState.SAVING;
        var _a = this.state, initialData = _a.initialData, data = _a.data;
        var _b = this.props, errorMessage = _b.errorMessage, hideErrors = _b.hideErrors, requireChanges = _b.requireChanges;
        var hasChanges = requireChanges
            ? Object.keys(data).length && !isEqual(data, initialData)
            : true;
        var isError = this.state.state === FormState.ERROR;
        var nonFieldErrors = this.state.errors && this.state.errors.non_field_errors;
        return (<StyledForm onSubmit={this.onSubmit} className={this.props.className}>
        {isError && !hideErrors && (<div className="alert alert-error alert-block">
            {nonFieldErrors ? (<div>
                <p>
                  {t('Unable to save your changes. Please correct the following errors try again.')}
                </p>
                <ul>
                  {nonFieldErrors.map(function (e, i) { return (<li key={i}>{e}</li>); })}
                </ul>
              </div>) : (errorMessage)}
          </div>)}
        {this.props.children}
        <div className={this.props.footerClass} style={{ marginTop: 25 }}>
          <button className="btn btn-primary" disabled={isSaving || this.props.submitDisabled || !hasChanges} type="submit">
            {this.props.submitLabel}
          </button>
          {this.props.onCancel && (<button type="button" className="btn btn-default" disabled={isSaving} onClick={this.props.onCancel} style={{ marginLeft: 5 }}>
              {this.props.cancelLabel}
            </button>)}
          {this.props.extraButton}
        </div>
      </StyledForm>);
    };
    Form.propTypes = {
        cancelLabel: PropTypes.string,
        onCancel: PropTypes.func,
        onSubmit: PropTypes.func,
        onSubmitSuccess: PropTypes.func,
        onSubmitError: PropTypes.func,
        submitDisabled: PropTypes.bool,
        submitLabel: PropTypes.string,
        footerClass: PropTypes.string,
        extraButton: PropTypes.element,
        initialData: PropTypes.object,
        requireChanges: PropTypes.bool,
        errorMessage: PropTypes.node,
        hideErrors: PropTypes.bool,
        resetOnError: PropTypes.bool,
    };
    Form.childContextTypes = {
        form: PropTypes.object.isRequired,
    };
    Form.defaultProps = {
        cancelLabel: t('Cancel'),
        submitLabel: t('Save Changes'),
        submitDisabled: false,
        footerClass: 'form-actions align-right',
        className: 'form-stacked',
        requireChanges: false,
        hideErrors: false,
        resetOnError: false,
        errorMessage: t('Unable to save your changes. Please ensure all fields are valid and try again.'),
    };
    return Form;
}(React.Component));
// Note: this is so we can use this as a selector for SelectField
// We need to keep `Form` as a React Component because ApiForm extends it :/
export var StyledForm = styled('form')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
export default Form;
var templateObject_1;
//# sourceMappingURL=form.jsx.map