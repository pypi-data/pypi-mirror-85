import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import space from 'app/styles/space';
import { IconChevron } from 'app/icons';
var DropdownButton = function (_a) {
    var isOpen = _a.isOpen, children = _a.children, forwardedRef = _a.forwardedRef, prefix = _a.prefix, _b = _a.showChevron, showChevron = _b === void 0 ? false : _b, _c = _a.hideBottomBorder, hideBottomBorder = _c === void 0 ? true : _c, props = __rest(_a, ["isOpen", "children", "forwardedRef", "prefix", "showChevron", "hideBottomBorder"]);
    return (<StyledButton type="button" isOpen={isOpen} hideBottomBorder={hideBottomBorder} ref={forwardedRef} {...props}>
    {prefix && <LabelText>{prefix}:</LabelText>}
    {children}
    {showChevron && <StyledChevron size="10px" direction={isOpen ? 'up' : 'down'}/>}
  </StyledButton>);
};
DropdownButton.defaultProps = {
    showChevron: true,
};
var StyledChevron = styled(IconChevron)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: 0.33em;\n"], ["\n  margin-left: 0.33em;\n"])));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n  position: relative;\n  z-index: 2;\n  box-shadow: ", ";\n  border-bottom-color: ", ";\n\n  &:active,\n  &:focus,\n  &:hover {\n    border-bottom-color: ", ";\n  }\n"], ["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n  position: relative;\n  z-index: 2;\n  box-shadow: ", ";\n  border-bottom-color: ",
    ";\n\n  &:active,\n  &:focus,\n  &:hover {\n    border-bottom-color: ",
    ";\n  }\n"])), function (p) { return (p.isOpen ? 0 : p.theme.borderRadius); }, function (p) { return (p.isOpen ? 0 : p.theme.borderRadius); }, function (p) { return (p.isOpen || p.disabled ? 'none' : p.theme.dropShadowLight); }, function (p) {
    return p.isOpen && p.hideBottomBorder ? 'transparent' : p.theme.border;
}, function (p) {
    return p.isOpen && p.hideBottomBorder ? 'transparent' : p.theme.border;
});
var LabelText = styled('em')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-style: normal;\n  color: ", ";\n  padding-right: ", ";\n"], ["\n  font-style: normal;\n  color: ", ";\n  padding-right: ", ";\n"])), function (p) { return p.theme.gray300; }, space(0.75));
export default React.forwardRef(function (props, ref) { return (<DropdownButton forwardedRef={ref} {...props}/>); });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dropdownButton.jsx.map