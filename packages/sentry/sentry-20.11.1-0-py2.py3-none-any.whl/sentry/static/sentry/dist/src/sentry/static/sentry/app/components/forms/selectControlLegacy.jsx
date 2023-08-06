import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import ReactSelect, { Async, Creatable, AsyncCreatable } from 'react-select-legacy';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { IconChevron } from 'app/icons';
import convertFromSelect2Choices from 'app/utils/convertFromSelect2Choices';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
/**
 * The library has `value` defined as `PropTypes.object`, but this
 * is not the case when `multiple` is true :/
 */
ReactSelect.Value.propTypes = __assign(__assign({}, ReactSelect.Value.propTypes), { value: PropTypes.any });
var SelectControlLegacy = /** @class */ (function (_super) {
    __extends(SelectControlLegacy, _super);
    function SelectControlLegacy() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderArrow = function () { return <StyledIconChevron direction="down" size="xs"/>; };
        return _this;
    }
    SelectControlLegacy.prototype.render = function () {
        var _a = this.props, async = _a.async, creatable = _a.creatable, options = _a.options, choices = _a.choices, clearable = _a.clearable, noMenu = _a.noMenu, placeholder = _a.placeholder, props = __rest(_a, ["async", "creatable", "options", "choices", "clearable", "noMenu", "placeholder"]);
        // Compatibility with old select2 API
        var choicesOrOptions = convertFromSelect2Choices(typeof choices === 'function' ? choices(this.props) : choices) || options;
        var noMenuProps = {
            arrowRenderer: function () { return null; },
            menuRenderer: function () { return null; },
            openOnClick: false,
            menuContainerStyle: { display: 'none' },
        };
        // "-Removes" props should match `clearable` unless explicitly defined in props
        // rest props should be after "-Removes" so that it can be overridden
        return (<StyledSelect arrowRenderer={this.renderArrow} async={async} creatable={creatable} clearable={clearable} backspaceRemoves={clearable} deleteRemoves={clearable} noMenu={noMenu} {...(noMenu ? noMenuProps : {})} {...props} multi={this.props.multiple || this.props.multi} options={choicesOrOptions} placeholder={callIfFunction(placeholder, this.props) || placeholder}/>);
    };
    SelectControlLegacy.propTypes = __assign(__assign({}, ReactSelect.propTypes), { options: PropTypes.arrayOf(PropTypes.shape({
            label: PropTypes.node,
            value: PropTypes.any,
        })), 
        // react-select knows this as multi, but for standardization
        // and compatibility we use multiple
        multiple: PropTypes.bool, 
        // multi is supported for compatibility
        multi: PropTypes.bool, 
        // disable rendering a menu
        noMenu: PropTypes.bool, choices: PropTypes.oneOfType([
            PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string, PropTypes.array])),
            PropTypes.func,
        ]), placeholder: PropTypes.oneOfType([ReactSelect.propTypes.placeholder, PropTypes.func]) });
    SelectControlLegacy.defaultProps = {
        clearable: false,
        multiple: false,
        height: 36,
    };
    return SelectControlLegacy;
}(React.Component));
var SelectPicker = function (_a) {
    var async = _a.async, creatable = _a.creatable, forwardedRef = _a.forwardedRef, props = __rest(_a, ["async", "creatable", "forwardedRef"]);
    // Pick the right component to use
    var Component;
    if (async && creatable) {
        Component = AsyncCreatable;
    }
    else if (async && !creatable) {
        Component = Async;
    }
    else if (creatable) {
        Component = Creatable;
    }
    else {
        Component = ReactSelect;
    }
    return <Component ref={forwardedRef} {...props}/>;
};
SelectPicker.propTypes = {
    async: PropTypes.bool,
    creatable: PropTypes.bool,
    forwardedRef: PropTypes.any,
};
var StyledSelect = styled(SelectPicker)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 15px;\n\n  .Select-control {\n    border: 1px solid ", ";\n    height: ", "px;\n    overflow: visible;\n  }\n\n  &.Select.is-focused > .Select-control {\n    border: 1px solid ", ";\n    border-color: ", ";\n    box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;\n  }\n\n  &.Select.is-focused:not(.is-open) > .Select-control {\n    height: ", "px;\n    overflow: visible;\n  }\n\n  .Select-input {\n    height: ", "px;\n    input {\n      line-height: ", "px;\n      padding: 0 0;\n    }\n  }\n\n  &.Select--multi .Select-value {\n    margin-top: 6px;\n  }\n\n  .Select-placeholder,\n  &.Select--single > .Select-control .Select-value {\n    height: ", "px;\n    line-height: ", "px;\n    &:focus {\n      border: 1px solid ", ";\n    }\n  }\n\n  &.Select--single.is-disabled .Select-control .Select-value .Select-value-label {\n    color: ", ";\n  }\n\n  .Select-option.is-focused {\n    color: ", ";\n    background-color: ", ";\n  }\n  .Select-multi-value-wrapper {\n    > a {\n      margin-left: 4px;\n    }\n  }\n\n  .Select-clear {\n    vertical-align: middle;\n  }\n\n  .Select-menu-outer {\n    z-index: ", ";\n  }\n\n  ", "\n"], ["\n  font-size: 15px;\n\n  .Select-control {\n    border: 1px solid ", ";\n    height: ", "px;\n    overflow: visible;\n  }\n\n  &.Select.is-focused > .Select-control {\n    border: 1px solid ", ";\n    border-color: ", ";\n    box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;\n  }\n\n  &.Select.is-focused:not(.is-open) > .Select-control {\n    height: ", "px;\n    overflow: visible;\n  }\n\n  .Select-input {\n    height: ", "px;\n    input {\n      line-height: ", "px;\n      padding: 0 0;\n    }\n  }\n\n  &.Select--multi .Select-value {\n    margin-top: 6px;\n  }\n\n  .Select-placeholder,\n  &.Select--single > .Select-control .Select-value {\n    height: ", "px;\n    line-height: ", "px;\n    &:focus {\n      border: 1px solid ", ";\n    }\n  }\n\n  &.Select--single.is-disabled .Select-control .Select-value .Select-value-label {\n    color: ", ";\n  }\n\n  .Select-option.is-focused {\n    color: ", ";\n    background-color: ", ";\n  }\n  .Select-multi-value-wrapper {\n    > a {\n      margin-left: 4px;\n    }\n  }\n\n  .Select-clear {\n    vertical-align: middle;\n  }\n\n  .Select-menu-outer {\n    z-index: ", ";\n  }\n\n  ",
    "\n"])), function (p) { return p.theme.border; }, function (p) { return p.height; }, function (p) { return p.theme.border; }, function (p) { return p.theme.textColor; }, function (p) { return p.height; }, function (p) { return p.height; }, function (p) { return p.height; }, function (p) { return p.height; }, function (p) { return p.height; }, function (p) { return p.theme.gray500; }, function (p) { return p.theme.disabled; }, function (p) { return p.theme.white; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.zIndex.dropdown; }, function (_a) {
    var noMenu = _a.noMenu;
    return noMenu && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      &.Select.is-focused.is-open > .Select-control {\n        border-radius: 4px;\n      }\n    "], ["\n      &.Select.is-focused.is-open > .Select-control {\n        border-radius: 4px;\n      }\n    "])));
});
var StyledIconChevron = styled(IconChevron)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
export default SelectControlLegacy;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=selectControlLegacy.jsx.map