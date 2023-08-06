import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Pill = React.memo(function (_a) {
    var name = _a.name, value = _a.value, children = _a.children, type = _a.type, className = _a.className;
    var getTypeAndValue = function () {
        if (value === undefined) {
            return {};
        }
        switch (value) {
            case 'true':
            case true:
                return {
                    valueType: 'positive',
                    renderValue: 'true',
                };
            case 'false':
            case false:
                return {
                    valueType: 'negative',
                    renderValue: 'false',
                };
            case null:
            case undefined:
                return {
                    valueType: 'error',
                    renderValue: 'n/a',
                };
            default:
                return {
                    valueType: undefined,
                    renderValue: String(value),
                };
        }
    };
    var _b = getTypeAndValue(), valueType = _b.valueType, renderValue = _b.renderValue;
    return (<StyledPill type={type !== null && type !== void 0 ? type : valueType} className={className}>
      <PillName>{name}</PillName>
      <PillValue>{children !== null && children !== void 0 ? children : renderValue}</PillValue>
    </StyledPill>);
});
var getPillStyle = function (_a) {
    var type = _a.type, theme = _a.theme;
    switch (type) {
        case 'error':
            return "\n        background: " + theme.red100 + ";\n        background: " + theme.red100 + ";\n        border: 1px solid " + theme.red300 + ";\n      ";
        default:
            return "\n        border: 1px solid " + theme.border + ";\n      ";
    }
};
var getPillValueStyle = function (_a) {
    var type = _a.type, theme = _a.theme;
    switch (type) {
        case 'positive':
            return "\n        background: " + theme.green100 + ";\n        border: 1px solid " + theme.green300 + ";\n        border-left-color: " + theme.green300 + ";\n        font-family: " + theme.text.familyMono + ";\n        margin: -1px;\n      ";
        case 'error':
            return "\n        border-left-color: " + theme.red300 + ";\n        background: " + theme.red100 + ";\n        border: 1px solid " + theme.red300 + ";\n        margin: -1px;\n      ";
        case 'negative':
            return "\n        border-left-color: " + theme.red300 + ";\n        background: " + theme.red100 + ";\n        border: 1px solid " + theme.red300 + ";\n        font-family: " + theme.text.familyMono + ";\n        margin: -1px;\n      ";
        default:
            return "\n        background: " + theme.backgroundSecondary + ";\n        font-family: " + theme.text.familyMono + ";\n      ";
    }
};
var PillName = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  min-width: 0;\n  white-space: nowrap;\n  display: flex;\n  align-items: center;\n"], ["\n  padding: ", " ", ";\n  min-width: 0;\n  white-space: nowrap;\n  display: flex;\n  align-items: center;\n"])), space(0.5), space(1));
var PillValue = styled(PillName)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-left: 1px solid ", ";\n  border-radius: ", ";\n  max-width: 100%;\n  display: flex;\n  align-items: center;\n\n  > a {\n    max-width: 100%;\n    text-overflow: ellipsis;\n    overflow: hidden;\n    white-space: nowrap;\n    display: inline-block;\n    vertical-align: text-bottom;\n  }\n\n  .pill-icon,\n  .external-icon {\n    display: inline;\n    margin: 0 0 0 ", ";\n    color: ", ";\n    &:hover {\n      color: ", ";\n    }\n  }\n"], ["\n  border-left: 1px solid ", ";\n  border-radius: ",
    ";\n  max-width: 100%;\n  display: flex;\n  align-items: center;\n\n  > a {\n    max-width: 100%;\n    text-overflow: ellipsis;\n    overflow: hidden;\n    white-space: nowrap;\n    display: inline-block;\n    vertical-align: text-bottom;\n  }\n\n  .pill-icon,\n  .external-icon {\n    display: inline;\n    margin: 0 0 0 ", ";\n    color: ", ";\n    &:hover {\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.border; }, function (p) {
    return "0 " + p.theme.button.borderRadius + " " + p.theme.button.borderRadius + " 0";
}, space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
var StyledPill = styled('li')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n  margin: 0 ", " ", " 0;\n  display: flex;\n  border-radius: ", ";\n  box-shadow: ", ";\n  line-height: 1.2;\n  max-width: 100%;\n  :last-child {\n    margin-right: 0;\n  }\n\n  ", ";\n\n  ", " {\n    ", ";\n  }\n"], ["\n  white-space: nowrap;\n  margin: 0 ", " ", " 0;\n  display: flex;\n  border-radius: ", ";\n  box-shadow: ", ";\n  line-height: 1.2;\n  max-width: 100%;\n  :last-child {\n    margin-right: 0;\n  }\n\n  ", ";\n\n  ", " {\n    ", ";\n  }\n"])), space(1), space(1), function (p) { return p.theme.button.borderRadius; }, function (p) { return p.theme.dropShadowLightest; }, getPillStyle, PillValue, getPillValueStyle);
export default Pill;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=pill.jsx.map