import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var inlineStyle = function (p) {
    return p.inline
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        align-items: center;\n      "], ["\n        align-items: center;\n      "]))) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n        flex-direction: column;\n        align-items: stretch;\n      "], ["\n        flex-direction: column;\n        align-items: stretch;\n      "])));
};
var getPadding = function (p) {
    return p.stacked && !p.inline
        ? css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n        padding: 0 ", " ", " 0;\n      "], ["\n        padding: 0 ", " ", " 0;\n      "])), p.hasControlState ? 0 : space(2), space(2)) : css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n        padding: ", " ", " ", " ", ";\n      "], ["\n        padding: ", " ", " ", " ", ";\n      "])), space(2), p.hasControlState ? 0 : space(2), space(2), space(2));
};
/**
 * `hasControlState` - adds padding to right if this is false
 */
var FieldWrapper = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  ", "\n  ", "\n  display: flex;\n  transition: background 0.15s;\n\n  ", "\n\n  ", "\n\n\n  /* Better padding with form inside of a modal */\n  ", "\n\n  &:last-child {\n    border-bottom: none;\n    ", ";\n  }\n"], ["\n  ", "\n  ", "\n  display: flex;\n  transition: background 0.15s;\n\n  ",
    "\n\n  ",
    "\n\n\n  /* Better padding with form inside of a modal */\n  ",
    "\n\n  &:last-child {\n    border-bottom: none;\n    ", ";\n  }\n"])), getPadding, inlineStyle, function (p) {
    return !p.stacked && css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n      border-bottom: 1px solid ", ";\n    "], ["\n      border-bottom: 1px solid ", ";\n    "])), p.theme.innerBorder);
}, function (p) {
    return p.highlighted && css(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n      position: relative;\n\n      &:after {\n        content: '';\n        display: block;\n        position: absolute;\n        top: -1px;\n        left: -1px;\n        right: -1px;\n        bottom: -1px;\n        border: 1px solid ", ";\n        pointer-events: none;\n      }\n    "], ["\n      position: relative;\n\n      &:after {\n        content: '';\n        display: block;\n        position: absolute;\n        top: -1px;\n        left: -1px;\n        right: -1px;\n        bottom: -1px;\n        border: 1px solid ", ";\n        pointer-events: none;\n      }\n    "])), p.theme.purple300);
}, function (p) {
    return !p.hasControlState && css(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n      .modal-content & {\n        padding-right: 0;\n      }\n    "], ["\n      .modal-content & {\n        padding-right: 0;\n      }\n    "])));
}, function (p) { return (p.stacked ? 'padding-bottom: 0' : ''); });
export default FieldWrapper;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=fieldWrapper.jsx.map