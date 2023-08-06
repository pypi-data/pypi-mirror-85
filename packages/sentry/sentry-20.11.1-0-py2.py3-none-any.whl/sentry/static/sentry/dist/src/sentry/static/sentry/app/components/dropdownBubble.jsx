import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import SettingsHeader from 'app/views/settings/components/settingsHeader';
/**
 * If `blendCorner` is false, then we apply border-radius to all corners
 *
 * Otherwise apply radius to opposite side of `alignMenu` *unles it is fixed width*
 */
var getMenuBorderRadius = function (_a) {
    var blendWithActor = _a.blendWithActor, blendCorner = _a.blendCorner, alignMenu = _a.alignMenu, width = _a.width, theme = _a.theme;
    var radius = theme.borderRadius;
    if (!blendCorner) {
        return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      border-radius: ", ";\n    "], ["\n      border-radius: ", ";\n    "])), radius);
    }
    // If menu width is the same width as the control
    var isFullWidth = width === '100%';
    // No top border radius if widths match
    var hasTopLeftRadius = !blendWithActor && !isFullWidth && alignMenu !== 'left';
    var hasTopRightRadius = !blendWithActor && !isFullWidth && !hasTopLeftRadius;
    return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n    border-radius: ", " ", "\n      ", " ", ";\n  "], ["\n    border-radius: ", " ", "\n      ", " ", ";\n  "])), hasTopLeftRadius ? radius : 0, hasTopRightRadius ? radius : 0, radius, radius);
};
var getMenuArrow = function (_a) {
    var menuWithArrow = _a.menuWithArrow, alignMenu = _a.alignMenu, theme = _a.theme;
    if (!menuWithArrow) {
        return '';
    }
    var alignRight = alignMenu === 'right';
    return css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n    top: 32px;\n\n    &::before {\n      width: 0;\n      height: 0;\n      border-left: 9px solid transparent;\n      border-right: 9px solid transparent;\n      border-bottom: 9px solid rgba(52, 60, 69, 0.35);\n      content: '';\n      display: block;\n      position: absolute;\n      top: -9px;\n      left: 10px;\n      z-index: -2;\n      ", ";\n      ", ";\n    }\n\n    &:after {\n      width: 0;\n      height: 0;\n      border-left: 8px solid transparent;\n      border-right: 8px solid transparent;\n      border-bottom: 8px solid ", ";\n      content: '';\n      display: block;\n      position: absolute;\n      top: -8px;\n      left: 11px;\n      z-index: -1;\n      ", ";\n      ", ";\n    }\n  "], ["\n    top: 32px;\n\n    &::before {\n      width: 0;\n      height: 0;\n      border-left: 9px solid transparent;\n      border-right: 9px solid transparent;\n      border-bottom: 9px solid rgba(52, 60, 69, 0.35);\n      content: '';\n      display: block;\n      position: absolute;\n      top: -9px;\n      left: 10px;\n      z-index: -2;\n      ", ";\n      ", ";\n    }\n\n    &:after {\n      width: 0;\n      height: 0;\n      border-left: 8px solid transparent;\n      border-right: 8px solid transparent;\n      border-bottom: 8px solid ", ";\n      content: '';\n      display: block;\n      position: absolute;\n      top: -8px;\n      left: 11px;\n      z-index: -1;\n      ", ";\n      ", ";\n    }\n  "])), alignRight && 'left: auto;', alignRight && 'right: 10px;', theme.background, alignRight && 'left: auto;', alignRight && 'right: 11px;');
};
var DropdownBubble = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: calc(100% - 1px);\n  ", ";\n  right: 0;\n  box-shadow: ", ";\n  overflow: hidden;\n\n  ", ";\n  ", ";\n\n  ", ";\n\n  /* This is needed to be able to cover e.g. pagination buttons, but also be\n   * below dropdown actor button's zindex */\n  z-index: ", ";\n\n  ", " & {\n    z-index: ", ";\n  }\n"], ["\n  background: ", ";\n  color: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: calc(100% - 1px);\n  ", ";\n  right: 0;\n  box-shadow: ", ";\n  overflow: hidden;\n\n  ", ";\n  ", ";\n\n  ", ";\n\n  /* This is needed to be able to cover e.g. pagination buttons, but also be\n   * below dropdown actor button's zindex */\n  z-index: ", ";\n\n  " /* sc-selector */, " & {\n    z-index: ", ";\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.border; }, function (p) { return (p.width ? "width: " + p.width : ''); }, function (p) { return p.theme.dropShadowLight; }, getMenuBorderRadius, function (_a) {
    var alignMenu = _a.alignMenu;
    return (alignMenu === 'left' ? 'left: 0;' : '');
}, getMenuArrow, function (p) { return p.theme.zIndex.dropdownAutocomplete.menu; }, /* sc-selector */ SettingsHeader, function (p) { return p.theme.zIndex.dropdownAutocomplete.menu + 2; });
export default DropdownBubble;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=dropdownBubble.jsx.map