import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import space from 'app/styles/space';
var RangeSlider = /** @class */ (function (_super) {
    __extends(RangeSlider, _super);
    function RangeSlider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            sliderValue: _this.props.allowedValues
                ? // With `allowedValues` sliderValue will be the index to value in `allowedValues`
                    // This is so we can snap the rangeSlider using `step`
                    // This means that the range slider will have a uniform `step` in the UI
                    // and scale won't match `allowedValues
                    // e.g. with allowedValues = [0, 100, 1000, 10000] - in UI we'll have values = [0, 3] w/ step of 1
                    // so it always snaps at 25% width
                    _this.props.allowedValues.indexOf(Number(_this.props.value || 0))
                : _this.props.value,
        };
        _this.getActualValue = function (sliderValue) {
            var allowedValues = _this.props.allowedValues;
            var value;
            if (allowedValues) {
                // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
                value = allowedValues[sliderValue];
            }
            else {
                value = sliderValue;
            }
            return value;
        };
        _this.setValue = function (value) {
            _this.setState({
                sliderValue: value,
            });
        };
        _this.changeValue = function (value, e) {
            if (_this.props.onChange) {
                _this.props.onChange(_this.getActualValue(value), e);
            }
        };
        _this.handleInput = function (e) {
            var sliderValue = parseInt(e.target.value, 10);
            _this.setValue(sliderValue);
            _this.changeValue(sliderValue, e);
        };
        _this.handleBlur = function (e) {
            var onBlur = _this.props.onBlur;
            if (typeof onBlur !== 'function') {
                return;
            }
            onBlur(e);
        };
        _this.handleCustomInputChange = function (e) {
            var value = parseInt(e.target.value, 10);
            _this.setValue(isNaN(value) ? 0 : value);
        };
        _this.handleCustomInputBlur = function (e) {
            _this.handleInput(e);
        };
        return _this;
    }
    RangeSlider.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // Update local state when re-rendered with next `props.value` (e.g if this is controlled)
        if (typeof nextProps.value !== 'undefined') {
            var allowedValues = this.props.allowedValues;
            var sliderValue = nextProps.value;
            // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
            if (allowedValues && allowedValues.indexOf(Number(sliderValue || 0)) > -1) {
                sliderValue = allowedValues.indexOf(Number(sliderValue || 0));
            }
            this.setState({ sliderValue: sliderValue });
        }
    };
    RangeSlider.prototype.render = function () {
        var _a = this.props, min = _a.min, max = _a.max, step = _a.step;
        var _b = this.props, name = _b.name, disabled = _b.disabled, allowedValues = _b.allowedValues, formatLabel = _b.formatLabel, placeholder = _b.placeholder, showCustomInput = _b.showCustomInput;
        var sliderValue = this.state.sliderValue;
        var actualValue = sliderValue;
        var displayValue = actualValue;
        if (allowedValues) {
            step = 1;
            min = 0;
            max = allowedValues.length - 1;
            actualValue = allowedValues[sliderValue];
            displayValue =
                typeof actualValue !== 'undefined' ? actualValue : t('Invalid value');
        }
        displayValue =
            typeof formatLabel === 'function' ? formatLabel(actualValue) : displayValue;
        return (<div>
        {!showCustomInput && <Label htmlFor={name}>{displayValue}</Label>}
        <SliderAndInputWrapper showCustomInput={showCustomInput}>
          <Slider type="range" name={name} min={min} max={max} step={step} disabled={disabled} onInput={this.handleInput} onChange={function () { }} onMouseUp={this.handleBlur} onKeyUp={this.handleBlur} value={sliderValue} hasLabel={!showCustomInput}/>
          {showCustomInput && (<Input placeholder={placeholder} value={sliderValue} onChange={this.handleCustomInputChange} onBlur={this.handleCustomInputBlur}/>)}
        </SliderAndInputWrapper>
      </div>);
    };
    RangeSlider.propTypes = {
        name: PropTypes.string.isRequired,
        /**
         * min allowed value, not needed if using `allowedValues`
         */
        min: PropTypes.number,
        /**
         * max allowed value, not needed if using `allowedValues`
         */
        max: PropTypes.number,
        /**
         * String is a valid type here only for empty string
         * Otherwise react complains:
         * "`value` prop on `input` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components."
         *
         * And we want this to be a controlled input when value is empty
         */
        value: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        step: PropTypes.number,
        disabled: PropTypes.bool,
        onChange: PropTypes.func,
        /**
         * Render prop for slider's label
         * Is passed the value as an argument
         */
        formatLabel: PropTypes.func,
        /**
         * Array of allowed values. Make sure `value` is in this list.
         * THIS NEEDS TO BE SORTED
         */
        allowedValues: PropTypes.arrayOf(PropTypes.number),
        /**
         * Show custom input
         */
        showCustomInput: PropTypes.bool,
        // Placeholder for custom input
        placeholder: PropTypes.string,
        /**
         * This is called when *any* MouseUp or KeyUp event happens.
         * Used for "smart" Fields to trigger a "blur" event. `onChange` can
         * be triggered quite frequently
         */
        onBlur: PropTypes.func,
    };
    return RangeSlider;
}(React.Component));
export default RangeSlider;
var Slider = styled('input')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* stylelint-disable-next-line property-no-vendor-prefix */\n  -webkit-appearance: none;\n  width: 100%;\n  margin: ", "px 0 ", "px;\n\n  &::-webkit-slider-runnable-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-moz-range-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-ms-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-webkit-slider-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-moz-range-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-fill-lower {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &::-ms-fill-upper {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &:focus {\n    outline: none;\n\n    &::-webkit-slider-runnable-track {\n      background: ", ";\n    }\n\n    &::-ms-fill-upper {\n      background: ", ";\n    }\n\n    &::-ms-fill-lower {\n      background: ", ";\n    }\n  }\n\n  &[disabled] {\n    &::-webkit-slider-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-moz-range-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-ms-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-webkit-slider-runnable-track {\n      cursor: default;\n    }\n\n    &::-moz-range-track {\n      cursor: default;\n    }\n\n    &::-ms-track {\n      cursor: default;\n    }\n  }\n"], ["\n  /* stylelint-disable-next-line property-no-vendor-prefix */\n  -webkit-appearance: none;\n  width: 100%;\n  margin: ", "px 0 ", "px;\n\n  &::-webkit-slider-runnable-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-moz-range-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-ms-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-webkit-slider-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-moz-range-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-thumb {\n    box-shadow: 0 0 0 3px #fff;\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-fill-lower {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &::-ms-fill-upper {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &:focus {\n    outline: none;\n\n    &::-webkit-slider-runnable-track {\n      background: ", ";\n    }\n\n    &::-ms-fill-upper {\n      background: ", ";\n    }\n\n    &::-ms-fill-lower {\n      background: ", ";\n    }\n  }\n\n  &[disabled] {\n    &::-webkit-slider-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-moz-range-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-ms-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-webkit-slider-runnable-track {\n      cursor: default;\n    }\n\n    &::-moz-range-track {\n      cursor: default;\n    }\n\n    &::-ms-track {\n      cursor: default;\n    }\n  }\n"])), function (p) { return p.theme.grid; }, function (p) { return p.theme.grid * (p.hasLabel ? 2 : 1); }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var Label = styled('label')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 14px;\n  margin-bottom: ", "px;\n  color: ", ";\n"], ["\n  font-size: 14px;\n  margin-bottom: ", "px;\n  color: ", ";\n"])), function (p) { return p.theme.grid; }, function (p) { return p.theme.subText; });
var SliderAndInputWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-auto-flow: column;\n  grid-template-columns: 4fr ", ";\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-auto-flow: column;\n  grid-template-columns: 4fr ", ";\n  grid-gap: ", ";\n"])), function (p) { return p.showCustomInput && '1fr'; }, space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=rangeSlider.jsx.map