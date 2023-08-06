import { __extends, __makeTemplateObject } from "tslib";
import classNames from 'classnames';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { defined } from 'app/utils';
import QuestionTooltip from 'app/components/questionTooltip';
var FormField = /** @class */ (function (_super) {
    __extends(FormField, _super);
    function FormField(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onChange = function (e) {
            var value = e.target.value;
            _this.setValue(value);
        };
        _this.setValue = function (value) {
            var form = (_this.context || {}).form;
            _this.setState({
                value: value,
            }, function () {
                var finalValue = _this.coerceValue(_this.state.value);
                _this.props.onChange && _this.props.onChange(finalValue);
                form && form.onFieldChange(_this.props.name, finalValue);
            });
        };
        _this.state = {
            error: null,
            value: _this.getValue(props, context),
        };
        return _this;
    }
    FormField.prototype.componentDidMount = function () { };
    FormField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps, nextContext) {
        var newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || defined(nextContext.form)) {
            var newValue = this.getValue(nextProps, nextContext);
            if (newValue !== this.state.value) {
                this.setValue(newValue);
            }
        }
    };
    FormField.prototype.componentWillUnmount = function () { };
    FormField.prototype.getValue = function (props, context) {
        var form = (context || this.context || {}).form;
        props = props || this.props;
        if (defined(props.value)) {
            return props.value;
        }
        if (form && form.data.hasOwnProperty(props.name)) {
            return defined(form.data[props.name]) ? form.data[props.name] : '';
        }
        return defined(props.defaultValue) ? props.defaultValue : '';
    };
    FormField.prototype.getError = function (props, context) {
        var form = (context || this.context || {}).form;
        props = props || this.props;
        if (defined(props.error)) {
            return props.error;
        }
        return (form && form.errors[props.name]) || null;
    };
    FormField.prototype.getId = function () {
        return "id-" + this.props.name;
    };
    FormField.prototype.coerceValue = function (value) {
        return value;
    };
    FormField.prototype.getField = function () {
        throw new Error('Must be implemented by child.');
    };
    FormField.prototype.getClassName = function () {
        throw new Error('Must be implemented by child.');
    };
    FormField.prototype.getFinalClassNames = function () {
        var _a = this.props, className = _a.className, required = _a.required;
        var error = this.state.error;
        return classNames(className, this.getClassName(), {
            'has-error': !!error,
            required: required,
        });
    };
    FormField.prototype.renderDisabledReason = function () {
        var _a = this.props, disabled = _a.disabled, disabledReason = _a.disabledReason;
        if (!disabled) {
            return null;
        }
        if (!disabledReason) {
            return null;
        }
        return <QuestionTooltip title={disabledReason} position="top" size="sm"/>;
    };
    FormField.prototype.render = function () {
        var _a = this.props, label = _a.label, hideErrorMessage = _a.hideErrorMessage, help = _a.help, style = _a.style;
        var error = this.state.error;
        var cx = this.getFinalClassNames();
        var shouldShowErrorMessage = error && !hideErrorMessage;
        return (<div style={style} className={cx}>
        <div className="controls">
          {label && (<label htmlFor={this.getId()} className="control-label">
              {label}
            </label>)}
          {this.getField()}
          {this.renderDisabledReason()}
          {defined(help) && <p className="help-block">{help}</p>}
          {shouldShowErrorMessage && <ErrorMessage>{error}</ErrorMessage>}
        </div>
      </div>);
    };
    FormField.propTypes = {
        name: PropTypes.string.isRequired,
        /** Inline style */
        style: PropTypes.object,
        label: PropTypes.node,
        // This is actually used but eslint doesn't parse it correctly
        // eslint-disable-next-line react/no-unused-prop-types
        defaultValue: PropTypes.any,
        disabled: PropTypes.bool,
        disabledReason: PropTypes.string,
        help: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
        required: PropTypes.bool,
        hideErrorMessage: PropTypes.bool,
        className: PropTypes.string,
        // the following should only be used without form context
        onChange: PropTypes.func,
        error: PropTypes.string,
        value: PropTypes.any,
        meta: PropTypes.any,
    };
    FormField.contextTypes = {
        form: PropTypes.object,
    };
    FormField.defaultProps = {
        hideErrorMessage: false,
        disabled: false,
        required: false,
    };
    return FormField;
}(React.PureComponent));
export default FormField;
var ErrorMessage = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.red300; });
var templateObject_1;
//# sourceMappingURL=formField.jsx.map