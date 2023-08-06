import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import DropdownButton from 'app/components/dropdownButton';
var DropDownButton = function (_a) {
    var isOpen = _a.isOpen, getActorProps = _a.getActorProps, checkedQuantity = _a.checkedQuantity;
    var buttonProps = {
        label: t('Filter By'),
        priority: 'default',
        hasDarkBorderBottomColor: false,
    };
    if (checkedQuantity > 0) {
        buttonProps.label = tn('%s Active Filter', '%s Active Filters', checkedQuantity);
        buttonProps.priority = 'primary';
        buttonProps.hasDarkBorderBottomColor = true;
    }
    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} hasDarkBorderBottomColor={buttonProps.hasDarkBorderBottomColor} size="small" priority={buttonProps.priority}>
      {buttonProps.label}
    </StyledDropdownButton>);
};
export default DropDownButton;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-right: 0;\n  &:hover,\n  &:active {\n    border-right: 0;\n    ", "\n  }\n  z-index: ", ";\n  border-radius: ", ";\n  white-space: nowrap;\n  max-width: 200px;\n  ", "\n"], ["\n  border-right: 0;\n  &:hover,\n  &:active {\n    border-right: 0;\n    ",
    "\n  }\n  z-index: ", ";\n  border-radius: ",
    ";\n  white-space: nowrap;\n  max-width: 200px;\n  ",
    "\n"])), function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n        border-bottom-color: " + p.theme.button.primary.border + ";\n      ";
}, function (p) { return p.theme.zIndex.dropdown; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " 0 0 0"
        : p.theme.borderRadius + " 0 0 " + p.theme.borderRadius;
}, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n      border-bottom-color: " + p.theme.button.primary.border + ";\n    ";
});
var templateObject_1;
//# sourceMappingURL=dropdownButton.jsx.map