import { __assign, __extends, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import { Observer } from 'mobx-react';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { defined } from 'app/utils';
import { sanitizeQuerySelector } from 'app/utils/sanitizeQuerySelector';
import { t } from 'app/locale';
import Button from 'app/components/button';
import Field from 'app/views/settings/components/forms/field';
import FieldControl from 'app/views/settings/components/forms/field/fieldControl';
import FieldErrorReason from 'app/views/settings/components/forms/field/fieldErrorReason';
import FormFieldControlState from 'app/views/settings/components/forms/formField/controlState';
import PanelAlert from 'app/components/panels/panelAlert';
import ReturnButton from 'app/views/settings/components/forms/returnButton';
import space from 'app/styles/space';
/**
 * Some fields don't need to implement their own onChange handlers, in
 * which case we will receive an Event, but if they do we should handle
 * the case where they return a value as the first argument.
 */
var getValueFromEvent = function (valueOrEvent, e) {
    var event = e || valueOrEvent;
    var value = defined(e) ? valueOrEvent : event && event.target && event.target.value;
    return {
        value: value,
        event: event,
    };
};
// MockedModel that returns values from props
// Disables a lot of functionality but allows you to use fields
// without wrapping them in a Form
var MockModel = /** @class */ (function () {
    function MockModel(props) {
        var _a;
        this.props = props;
        this.initialData = (_a = {},
            _a[props.name] = props.value,
            _a);
    }
    MockModel.prototype.setValue = function () { };
    MockModel.prototype.setFieldDescriptor = function () { };
    MockModel.prototype.removeField = function () { };
    MockModel.prototype.handleBlurField = function () { };
    MockModel.prototype.getValue = function () {
        return this.props.value;
    };
    MockModel.prototype.getError = function () {
        return this.props.error;
    };
    MockModel.prototype.getFieldState = function () {
        return false;
    };
    return MockModel;
}());
/**
 * This is a list of field properties that can accept a function taking the
 * form model, that will be called to determine the value of the prop upon an
 * observed change in the model.
 */
var propsToObserver = ['help', 'inline', 'highlighted', 'visible', 'disabled'];
var FormField = /** @class */ (function (_super) {
    __extends(FormField, _super);
    function FormField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Only works for styled inputs
        // Attempts to autofocus input field if field's name is in url hash
        _this.handleInputMount = function (ref) {
            if (ref && !_this.input) {
                var hash = _this.context.location && _this.context.location.hash;
                if (!hash) {
                    return;
                }
                if (hash !== "#" + _this.props.name) {
                    return;
                }
                // Not all form fields have this (e.g. Select fields)
                if (typeof ref.focus === 'function') {
                    ref.focus();
                }
            }
            _this.input = ref;
        };
        /**
         * Update field value in form model
         */
        _this.handleChange = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, name = _a.name, onChange = _a.onChange;
            var _b = getValueFromEvent.apply(void 0, __spread(args)), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (onChange) {
                onChange(value, event);
            }
            model.setValue(name, value);
        };
        /**
         * Notify model of a field being blurred
         */
        _this.handleBlur = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, name = _a.name, onBlur = _a.onBlur;
            var _b = getValueFromEvent.apply(void 0, __spread(args)), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (onBlur) {
                onBlur(value, event);
            }
            // Always call this, so model can decide what to do
            model.handleBlurField(name, value);
        };
        /**
         * Handle keydown to trigger a save on Enter
         */
        _this.handleKeyDown = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, onKeyDown = _a.onKeyDown, name = _a.name;
            var _b = getValueFromEvent.apply(void 0, __spread(args)), value = _b.value, event = _b.event;
            var model = _this.getModel();
            if (event.key === 'Enter') {
                model.handleBlurField(name, value);
            }
            if (onKeyDown) {
                onKeyDown(value, event);
            }
        };
        /**
         * Handle saving an individual field via UI button
         */
        _this.handleSaveField = function () {
            var name = _this.props.name;
            var model = _this.getModel();
            model.handleSaveField(name, model.getValue(name));
        };
        _this.handleCancelField = function () {
            var name = _this.props.name;
            var model = _this.getModel();
            model.handleCancelSaveField(name);
        };
        return _this;
    }
    FormField.prototype.componentDidMount = function () {
        // Tell model about this field's props
        this.getModel().setFieldDescriptor(this.props.name, this.props);
    };
    FormField.prototype.componentWillUnmount = function () {
        this.getModel().removeField(this.props.name);
    };
    FormField.prototype.getError = function () {
        return this.getModel().getError(this.props.name);
    };
    FormField.prototype.getId = function () {
        return sanitizeQuerySelector(this.props.name);
    };
    FormField.prototype.getModel = function () {
        if (this.context.form === undefined) {
            return new MockModel(this.props);
        }
        return this.context.form;
    };
    FormField.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, name = _a.name, hideErrorMessage = _a.hideErrorMessage, flexibleControlStateSize = _a.flexibleControlStateSize, saveOnBlur = _a.saveOnBlur, saveMessage = _a.saveMessage, saveMessageAlertType = _a.saveMessageAlertType, selectionInfoFunction = _a.selectionInfoFunction, hideControlState = _a.hideControlState, 
        // Don't pass `defaultValue` down to input fields, will be handled in form model
        _defaultValue = _a.defaultValue, props = __rest(_a, ["className", "name", "hideErrorMessage", "flexibleControlStateSize", "saveOnBlur", "saveMessage", "saveMessageAlertType", "selectionInfoFunction", "hideControlState", "defaultValue"]);
        var id = this.getId();
        var model = this.getModel();
        var saveOnBlurFieldOverride = typeof saveOnBlur !== 'undefined' && !saveOnBlur;
        //TODO(TS): This is difficult to type because of the reducer
        var makeField = function (extraProps) { return (<React.Fragment>
        <Field id={id} name={name} className={className} flexibleControlStateSize={flexibleControlStateSize} {...props} {...extraProps}>
          {function (_a) {
            var alignRight = _a.alignRight, inline = _a.inline, disabled = _a.disabled, disabledReason = _a.disabledReason;
            return (<FieldControl disabled={disabled} disabledReason={disabledReason} inline={inline} alignRight={alignRight} flexibleControlStateSize={flexibleControlStateSize} hideControlState={hideControlState} controlState={<FormFieldControlState model={model} name={name}/>} errorState={<Observer>
                  {function () {
                var error = _this.getError();
                var shouldShowErrorMessage = error && !hideErrorMessage;
                if (!shouldShowErrorMessage) {
                    return null;
                }
                return <FieldErrorReason>{error}</FieldErrorReason>;
            }}
                </Observer>}>
              <Observer>
                {function () {
                var error = _this.getError();
                var value = model.getValue(name);
                var showReturnButton = model.getFieldState(name, 'showReturnButton');
                return (<React.Fragment>
                      {_this.props.children(__assign(__assign({ ref: _this.handleInputMount }, props), { model: model,
                    name: name,
                    id: id, onKeyDown: _this.handleKeyDown, onChange: _this.handleChange, onBlur: _this.handleBlur, 
                    // Fixes react warnings about input switching from controlled to uncontrolled
                    // So force to empty string for null values
                    value: value === null ? '' : value, error: error,
                    disabled: disabled, initialData: model.initialData }))}
                      {showReturnButton && <StyledReturnButton />}
                    </React.Fragment>);
            }}
              </Observer>
            </FieldControl>);
        }}
        </Field>
        {selectionInfoFunction && (<Observer>
            {function () {
            var error = _this.getError();
            var value = model.getValue(name);
            return (((typeof props.visible === 'function'
                ? props.visible(_this.props)
                : true) &&
                selectionInfoFunction(__assign(__assign({}, props), { error: error, value: value }))) ||
                null);
        }}
          </Observer>)}
        {saveOnBlurFieldOverride && (<Observer>
            {function () {
            var showFieldSave = model.getFieldState(name, 'showSave');
            var value = model.getValue(name);
            if (!showFieldSave) {
                return null;
            }
            return (<PanelAlert type={saveMessageAlertType}>
                  <MessageAndActions>
                    <div>
                      {typeof saveMessage === 'function'
                ? saveMessage(__assign(__assign({}, props), { value: value }))
                : saveMessage}
                    </div>
                    <Actions>
                      <CancelButton onClick={_this.handleCancelField}>
                        {t('Cancel')}
                      </CancelButton>
                      <SaveButton priority="primary" type="button" onClick={_this.handleSaveField}>
                        {t('Save')}
                      </SaveButton>
                    </Actions>
                  </MessageAndActions>
                </PanelAlert>);
        }}
          </Observer>)}
      </React.Fragment>); };
        var observedProps = propsToObserver
            .filter(function (p) { return typeof _this.props[p] === 'function'; })
            .map(function (p) { return [
            p,
            function () {
                var innerProps = _this.props;
                return innerProps[p](__assign(__assign({}, _this.props), { model: model }));
            },
        ]; });
        // This field has no properties that require observation to compute their
        // value, this field is static and will not be re-rendered.
        if (observedProps.length === 0) {
            return makeField();
        }
        var reducer = function (a, _a) {
            var _b;
            var _c = __read(_a, 2), prop = _c[0], fn = _c[1];
            return (__assign(__assign({}, a), (_b = {}, _b[prop] = fn(), _b)));
        };
        var observedPropsFn = function () { return makeField(observedProps.reduce(reducer, {})); };
        return <Observer>{observedPropsFn}</Observer>;
    };
    FormField.propTypes = {
        name: PropTypes.string.isRequired,
        /** Inline style */
        style: PropTypes.object,
        /**
         * Iff false, disable saveOnBlur for field, instead show a save/cancel button
         */
        saveOnBlur: PropTypes.bool,
        /**
         * If saveOnBlur is false, then an optional saveMessage can be used to let
         * the user know what's going to happen when they save a field.
         */
        saveMessage: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
        /**
         * The "alert type" to use for the save message.
         * Probably only "info"/"warning" should be used.
         */
        saveMessageAlertType: PropTypes.oneOf(['', 'info', 'warning', 'success', 'error']),
        /**
         * A function producing an optional component with extra information.
         */
        selectionInfoFunction: PropTypes.func,
        /**
         * Should hide error message?
         */
        hideErrorMessage: PropTypes.bool,
        /**
         * Hides control state component
         */
        flexibleControlStateSize: PropTypes.bool,
        // Default value to use for form field if value is not specified in `<Form>` parent
        defaultValue: PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.number,
            PropTypes.func,
        ]),
        // the following should only be used without form context
        onChange: PropTypes.func,
        onBlur: PropTypes.func,
        onKeyDown: PropTypes.func,
        onMouseOver: PropTypes.func,
        onMouseOut: PropTypes.func,
    };
    FormField.contextTypes = {
        location: PropTypes.object,
        form: PropTypes.object,
    };
    FormField.defaultProps = {
        hideErrorMessage: false,
        flexibleControlStateSize: false,
    };
    return FormField;
}(React.Component));
export default FormField;
var MessageAndActions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var Actions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var CancelButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(2));
var SaveButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledReturnButton = styled(ReturnButton)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  right: 0;\n  top: 0;\n"], ["\n  position: absolute;\n  right: 0;\n  top: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map