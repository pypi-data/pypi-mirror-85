import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Heading = styled('h5')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  &:after {\n    flex: 1;\n    display: block;\n    content: '';\n    border-top: 1px solid ", ";\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  &:after {\n    flex: 1;\n    display: block;\n    content: '';\n    border-top: 1px solid ", ";\n    margin-left: ", ";\n  }\n"])), space(2), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; }, space(1));
var Subheading = styled('h6')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  font-size: ", ";\n  text-transform: uppercase;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  display: flex;\n  font-size: ", ";\n  text-transform: uppercase;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeExtraSmall; }, space(1));
/**
 * Used to add a new section in Issue Details's sidebar.
 */
function SidebarSection(_a) {
    var title = _a.title, children = _a.children, secondary = _a.secondary, props = __rest(_a, ["title", "children", "secondary"]);
    var HeaderComponent = secondary ? Subheading : Heading;
    return (<React.Fragment>
      <HeaderComponent {...props}>{title}</HeaderComponent>
      <SectionContent secondary={secondary}>{children}</SectionContent>
    </React.Fragment>);
}
var SectionContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), function (p) { return (p.secondary ? space(2) : space(3)); });
export default SidebarSection;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sidebarSection.jsx.map