import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import SidebarMenuItemLink from './sidebarMenuItemLink';
import { OrgSummary } from './sidebarOrgSummary';
var SidebarMenuItem = function (_a) {
    var to = _a.to, children = _a.children, href = _a.href, props = __rest(_a, ["to", "children", "href"]);
    var hasMenu = !to && !href;
    return (<StyledSidebarMenuItemLink to={to} href={href} {...props}>
      <MenuItemLabel hasMenu={hasMenu}>{children}</MenuItemLabel>
    </StyledSidebarMenuItemLink>);
};
var menuItemStyles = function (p) { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n  display: flex;\n  font-size: ", ";\n  line-height: 32px;\n  padding: 0 ", ";\n  position: relative;\n  transition: 0.1s all linear;\n  ", ";\n\n  &:hover,\n  &:active,\n  &.focus-visible {\n    background: ", ";\n    color: ", ";\n    outline: none;\n  }\n\n  ", " {\n    padding-left: 0;\n    padding-right: 0;\n  }\n"], ["\n  color: ", ";\n  cursor: pointer;\n  display: flex;\n  font-size: ", ";\n  line-height: 32px;\n  padding: 0 ", ";\n  position: relative;\n  transition: 0.1s all linear;\n  ", ";\n\n  &:hover,\n  &:active,\n  &.focus-visible {\n    background: ", ";\n    color: ", ";\n    outline: none;\n  }\n\n  ", " {\n    padding-left: 0;\n    padding-right: 0;\n  }\n"])), p.theme.textColor, p.theme.fontSizeMedium, p.theme.sidebar.menuSpacing, (!!p.to || !!p.href) && 'overflow: hidden', p.theme.backgroundSecondary, p.theme.textColor, OrgSummary); };
var MenuItemLabel = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n  ", ";\n"], ["\n  flex: 1;\n  ",
    ";\n"])), function (p) {
    return p.hasMenu
        ? css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n          margin: 0 -15px;\n          padding: 0 15px;\n        "], ["\n          margin: 0 -15px;\n          padding: 0 15px;\n        "]))) : css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n          overflow: hidden;\n        "], ["\n          overflow: hidden;\n        "])));
});
var StyledSidebarMenuItemLink = styled(SidebarMenuItemLink)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), menuItemStyles);
export { menuItemStyles };
export default SidebarMenuItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebarMenuItem.jsx.map