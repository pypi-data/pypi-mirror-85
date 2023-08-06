import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
var IconWrapper = styled('div', {
    shouldForwardProp: function (prop) { return prop !== 'color'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ",
    "\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLightest; }, function (p) { return p.theme.zIndex.breadcrumbs.iconWrapper; }, function (p) { return p.theme.border; }, function (p) { return p.theme.textColor; }, function (p) {
    return p.color &&
        "\n      color: " + (p.theme[p.color] || p.color) + ";\n      border-color: " + (p.theme[p.color] || p.color) + ";\n    ";
});
var GridCell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 100%;\n  position: relative;\n  white-space: pre-wrap;\n  word-break: break-all;\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ", "\n  ", ";\n"], ["\n  height: 100%;\n  position: relative;\n  white-space: pre-wrap;\n  word-break: break-all;\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ",
    "\n  ", ";\n"])), function (p) { return p.theme.innerBorder; }, space(1), function (p) { return p.theme.breakpoints[0]; }, space(1), space(2), function (p) {
    return p.hasError &&
        "\n      border-bottom: 1px solid " + p.theme.red300 + ";\n      :after {\n        content: '';\n        position: absolute;\n        top: -1px;\n        left: 0;\n        height: 1px;\n        width: 100%;\n        background: " + p.theme.red300 + ";\n      }\n    ";
}, function (p) { return p.isLastItem && "border-bottom: none"; });
var GridCellLeft = styled(GridCell)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"], ["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"])), space(1), space(0.5), space(1), space(1), function (p) { return (p.hasError ? p.theme.red300 : p.theme.innerBorder); }, function (p) { return p.theme.breakpoints[0]; });
var aroundContentStyle = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  z-index: 1;\n"], ["\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  z-index: 1;\n"])), theme.border, theme.borderRadius, theme.dropShadowLightest);
export { GridCell, GridCellLeft, IconWrapper, aroundContentStyle };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map