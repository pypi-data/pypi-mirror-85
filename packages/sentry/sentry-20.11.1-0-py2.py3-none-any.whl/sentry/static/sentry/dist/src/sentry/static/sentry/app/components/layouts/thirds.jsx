import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import NavTabs from 'app/components/navTabs';
/**
 * Base container for 66/33 containers.
 */
export var Body = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"], ["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"])), space(2), function (p) { return p.theme.background; }, function (p) { return p.theme.breakpoints[0]; }, space(2), space(4), function (p) { return p.theme.breakpoints[1]; }, space(3), function (p) { return p.theme.breakpoints[2]; });
/**
 * Use HeaderContent to create horizontal regions in the header
 * that contain a heading/breadcrumbs and a button group.
 */
export var HeaderContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  margin-bottom: ", ";\n  overflow: hidden;\n  max-width: 100%;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  margin-bottom: ", ";\n  overflow: hidden;\n  max-width: 100%;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, space(1));
/**
 * Container for action buttons and secondary information that
 * flows on the top right of the header.
 */
export var HeaderActions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  min-width: max-content;\n\n  @media (max-width: ", ") {\n    width: max-content;\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  min-width: max-content;\n\n  @media (max-width: ", ") {\n    width: max-content;\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, space(2));
/**
 * Heading container that includes margins.
 */
export var Title = styled('h2')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.2;\n  color: ", ";\n  margin-top: ", ";\n  /* TODO(bootstrap) Remove important when bootstrap headings are removed */\n  margin-bottom: 0 !important;\n  min-height: 30px;\n  align-self: center;\n  ", ";\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.2;\n  color: ", ";\n  margin-top: ", ";\n  /* TODO(bootstrap) Remove important when bootstrap headings are removed */\n  margin-bottom: 0 !important;\n  min-height: 30px;\n  align-self: center;\n  ", ";\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(3), overflowEllipsis, function (p) { return p.theme.breakpoints[1]; }, space(1));
/**
 * Header container for header content and header actions.
 *
 * Uses a horizontal layout in wide viewports to put space between
 * the headings and the actions container. In narrow viewports these elements
 * are stacked vertically.
 */
export var Header = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  flex-wrap: wrap;\n  flex-grow: 0;\n  justify-content: space-between;\n  padding: ", " ", " 0 ", ";\n  margin: 0;\n\n  background-color: transparent;\n  border-bottom: 1px solid ", ";\n\n  @media (max-width: ", ") {\n    padding: ", " ", " 0 ", ";\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  flex-wrap: wrap;\n  flex-grow: 0;\n  justify-content: space-between;\n  padding: ", " ", " 0 ", ";\n  margin: 0;\n\n  background-color: transparent;\n  border-bottom: 1px solid ", ";\n\n  @media (max-width: ", ") {\n    padding: ", " ", " 0 ", ";\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n  }\n"])), space(2), space(4), space(4), function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[0]; }, space(2), space(2), space(2), function (p) { return p.theme.breakpoints[1]; });
/**
 * Styled Nav Tabs for use inside a Layout.Header component
 */
export var HeaderNavTabs = styled(NavTabs)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n  border-bottom: 0 !important;\n\n  li {\n    margin-right: ", ";\n  }\n  li > a {\n    padding: ", " 0;\n    font-size: ", ";\n    margin-bottom: 4px;\n  }\n  li.active > a {\n    margin-bottom: 0;\n  }\n"], ["\n  margin: 0;\n  border-bottom: 0 !important;\n\n  li {\n    margin-right: ", ";\n  }\n  li > a {\n    padding: ", " 0;\n    font-size: ", ";\n    margin-bottom: 4px;\n  }\n  li.active > a {\n    margin-bottom: 0;\n  }\n"])), space(3), space(1), function (p) { return p.theme.fontSizeLarge; });
/**
 * Containers for two column 66/33 layout.
 */
export var Main = styled('section')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-column: ", ";\n  max-width: 100%;\n"], ["\n  grid-column: ", ";\n  max-width: 100%;\n"])), function (p) { return (p.fullWidth ? '1/3' : '1/2'); });
export var Side = styled('aside')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-column: 2/3;\n"], ["\n  grid-column: 2/3;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=thirds.jsx.map