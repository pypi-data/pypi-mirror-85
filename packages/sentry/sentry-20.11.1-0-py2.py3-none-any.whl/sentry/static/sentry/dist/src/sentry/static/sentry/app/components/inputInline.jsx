import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { callIfFunction } from 'app/utils/callIfFunction';
import { IconEdit } from 'app/icons';
import space from 'app/styles/space';
/**
 * InputInline is a cool pattern and @doralchan has confirmed that this has more
 * than 50% chance of being reused elsewhere in the app. However, adding it as a
 * form component has too much overhead for Discover2, so it'll be kept outside
 * for now.
 *
 * The props for this component take some cues from InputField.tsx
 *
 * The implementation uses HTMLDivElement with `contentEditable="true"`. This is
 * because we need the width to expand along with the content inside. There
 * isn't a way to easily do this with HTMLInputElement, especially with fonts
 * which are not fixed-width.
 *
 * If you are expecting the usual HTMLInputElement, this may have some quirky
 * behaviours that'll need your help to improve.
 *
 * TODO(leedongwei): Add to storybook
 * TODO(leedongwei): Add some tests
 */
var InputInline = /** @class */ (function (_super) {
    __extends(InputInline, _super);
    function InputInline() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isFocused: false,
            isHovering: false,
        };
        _this.refInput = React.createRef();
        /**
         * Used by the parent to blur/focus on the Input
         */
        _this.blur = function () {
            if (_this.refInput.current) {
                _this.refInput.current.blur();
            }
        };
        /**
         * Used by the parent to blur/focus on the Input
         */
        _this.focus = function () {
            if (_this.refInput.current) {
                _this.refInput.current.focus();
            }
        };
        _this.onBlur = function (event) {
            _this.setState({
                isFocused: false,
                isHovering: false,
            });
            callIfFunction(_this.props.onBlur, InputInline.setValueOnEvent(event));
        };
        _this.onFocus = function (event) {
            _this.setState({ isFocused: true });
            callIfFunction(_this.props.onFocus, InputInline.setValueOnEvent(event));
        };
        /**
         * HACK(leedongwei): ContentEditable is not a Form element, and as such it
         * does not emit `onChange` events. This method using `onInput` and capture the
         * inner value to be passed along to an onChange function.
         */
        _this.onChangeUsingOnInput = function (event) {
            callIfFunction(_this.props.onChange, InputInline.setValueOnEvent(event));
        };
        _this.onKeyDown = function (event) {
            // Might make sense to add Form submission here too
            if (event.key === 'Enter') {
                // Prevents the Enter key from inserting a line-break
                event.preventDefault();
                if (_this.refInput.current) {
                    _this.refInput.current.blur();
                }
            }
            callIfFunction(_this.props.onKeyUp, InputInline.setValueOnEvent(event));
        };
        _this.onKeyUp = function (event) {
            if (event.key === 'Escape' && _this.refInput.current) {
                _this.refInput.current.blur();
            }
            callIfFunction(_this.props.onKeyUp, InputInline.setValueOnEvent(event));
        };
        _this.onMouseEnter = function () {
            _this.setState({ isHovering: !_this.props.disabled });
        };
        _this.onMouseMove = function () {
            _this.setState({ isHovering: !_this.props.disabled });
        };
        _this.onMouseLeave = function () {
            _this.setState({ isHovering: false });
        };
        _this.onClickIcon = function (event) {
            if (_this.props.disabled) {
                return;
            }
            if (_this.refInput.current) {
                _this.refInput.current.focus();
            }
            callIfFunction(_this.props.onClick, InputInline.setValueOnEvent(event));
        };
        return _this;
    }
    /**
     * HACK(leedongwei): ContentEditable does not have the property `value`. We
     * coerce its `innerText` to `value` so it will have similar behaviour as a
     * HTMLInputElement
     *
     * We probably need to attach this to every DOMAttribute event...
     */
    InputInline.setValueOnEvent = function (event) {
        var text = event.target.innerText || event.currentTarget.innerText;
        event.target.value = text;
        event.currentTarget.value = text;
        return event;
    };
    InputInline.prototype.render = function () {
        var _a = this.props, value = _a.value, placeholder = _a.placeholder, disabled = _a.disabled;
        var isFocused = this.state.isFocused;
        var innerText = value || placeholder || '';
        return (<Wrapper style={this.props.style} onMouseEnter={this.onMouseEnter} onMouseMove={this.onMouseMove} onMouseLeave={this.onMouseLeave}>
        <Input {...this.props} // Pass DOMAttributes props first, extend/overwrite below
         ref={this.refInput} suppressContentEditableWarning contentEditable={!this.props.disabled} isHovering={this.state.isHovering} isDisabled={this.props.disabled} onBlur={this.onBlur} onFocus={this.onFocus} onInput={this.onChangeUsingOnInput} onChange={this.onChangeUsingOnInput} // Overwrite onChange too, just to be 100% sure
         onKeyDown={this.onKeyDown} onKeyUp={this.onKeyUp}>
          {innerText}
        </Input>

        {!isFocused && !disabled && (<div onClick={this.onClickIcon}>
            <StyledIconEdit />
          </div>)}
      </Wrapper>);
    };
    return InputInline;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n\n  vertical-align: text-bottom;\n"], ["\n  display: inline-flex;\n  align-items: center;\n\n  vertical-align: text-bottom;\n"])));
var Input = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  min-width: 40px;\n  margin: 0;\n  border: 1px solid ", ";\n  outline: none;\n\n  line-height: inherit;\n  border-radius: ", ";\n  background: transparent;\n\n  &:focus,\n  &:active {\n    border: 1px solid ", ";\n    background-color: ", ";\n  }\n"], ["\n  min-width: 40px;\n  margin: 0;\n  border: 1px solid ", ";\n  outline: none;\n\n  line-height: inherit;\n  border-radius: ", ";\n  background: transparent;\n\n  &:focus,\n  &:active {\n    border: 1px solid ", ";\n    background-color: ", ";\n  }\n"])), function (p) { return (p.isHovering ? p.theme.border : 'transparent'); }, space(0.5), function (p) { return (p.isDisabled ? 'transparent' : p.theme.border); }, function (p) { return (p.isDisabled ? 'transparent' : p.theme.gray200); });
var StyledIconEdit = styled(IconEdit)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  color: ", ";\n  margin-left: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), function (p) { return p.theme.gray300; }, space(0.5));
export default InputInline;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=inputInline.jsx.map