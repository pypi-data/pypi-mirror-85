import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
var Switch = function (_a) {
    var forwardRef = _a.forwardRef, _b = _a.size, size = _b === void 0 ? 'sm' : _b, isActive = _a.isActive, isLoading = _a.isLoading, isDisabled = _a.isDisabled, toggle = _a.toggle, id = _a.id, name = _a.name, className = _a.className;
    return (<SwitchButton ref={forwardRef} id={id} name={name} type="button" className={className} onClick={isDisabled ? undefined : toggle} role="checkbox" aria-checked={isActive} isLoading={isLoading} isDisabled={isDisabled} isActive={isActive} size={size} data-test-id="switch">
    <Toggle isDisabled={isDisabled} isActive={isActive} size={size}/>
  </SwitchButton>);
};
Switch.propTypes = {
    id: PropTypes.string,
    forwardRef: PropTypes.any,
    size: PropTypes.oneOf(['sm', 'lg']),
    isActive: PropTypes.bool,
    isLoading: PropTypes.bool,
    isDisabled: PropTypes.bool,
    toggle: PropTypes.func.isRequired,
};
var getSize = function (p) { return (p.size === 'sm' ? 16 : 24); };
var getToggleSize = function (p) { return getSize(p) - (p.size === 'sm' ? 6 : 10); };
var getToggleTop = function (p) { return (p.size === 'sm' ? 2 : 4); };
var getTranslateX = function (p) {
    return p.isActive ? getToggleTop(p) + getSize(p) : getToggleTop(p);
};
var SwitchButton = styled('button')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  background: none;\n  padding: 0;\n  border: 1px solid ", ";\n  position: relative;\n  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.04);\n  transition: 0.15s border ease;\n  cursor: ", ";\n  pointer-events: ", ";\n  height: ", "px;\n  width: ", "px;\n  border-radius: ", "px;\n\n  &:hover,\n  &:focus {\n    outline: none;\n    border-color: ", ";\n  }\n\n  &:focus,\n  &.focus-visible {\n    outline: none;\n    box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;\n  }\n"], ["\n  display: inline-block;\n  background: none;\n  padding: 0;\n  border: 1px solid ", ";\n  position: relative;\n  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.04);\n  transition: 0.15s border ease;\n  cursor: ", ";\n  pointer-events: ", ";\n  height: ", "px;\n  width: ", "px;\n  border-radius: ", "px;\n\n  &:hover,\n  &:focus {\n    outline: none;\n    border-color: ", ";\n  }\n\n  &:focus,\n  &.focus-visible {\n    outline: none;\n    box-shadow: rgba(209, 202, 216, 0.5) 0 0 0 3px;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return (p.isLoading || p.isDisabled ? 'not-allowed' : 'pointer'); }, function (p) { return (p.isLoading || p.isDisabled ? 'none' : null); }, getSize, function (p) { return getSize(p) * 2; }, getSize, function (p) { return p.theme.border; });
var Toggle = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  position: absolute;\n  border-radius: 50%;\n  transition: 0.25s all ease;\n  top: ", "px;\n  transform: translateX(", "px);\n  width: ", "px;\n  height: ", "px;\n  background: ", ";\n  opacity: ", ";\n"], ["\n  display: block;\n  position: absolute;\n  border-radius: 50%;\n  transition: 0.25s all ease;\n  top: ", "px;\n  transform: translateX(", "px);\n  width: ", "px;\n  height: ", "px;\n  background: ", ";\n  opacity: ", ";\n"])), getToggleTop, getTranslateX, getToggleSize, getToggleSize, function (p) { return (p.isActive ? p.theme.green300 : p.theme.gray200); }, function (p) { return (p.isDisabled ? 0.4 : null); });
export default React.forwardRef(function (props, ref) { return (<Switch {...props} forwardRef={ref}/>); });
var templateObject_1, templateObject_2;
//# sourceMappingURL=switch.jsx.map