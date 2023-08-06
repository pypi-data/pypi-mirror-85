import { __extends, __makeTemplateObject, __rest } from "tslib";
import ReactDOM from 'react-dom';
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import space from 'app/styles/space';
import { IconClose } from 'app/icons';
import { slideInLeft } from 'app/styles/animations';
/**
 * Get the container element of the sidebar that react portals into.
 */
export var getSidebarPanelContainer = function () {
    return document.getElementById('sidebar-flyout-portal');
};
var makePortal = function () {
    var portal = document.createElement('div');
    portal.setAttribute('id', 'sidebar-flyout-portal');
    document.body.appendChild(portal);
    return portal;
};
var SidebarPanel = /** @class */ (function (_super) {
    __extends(SidebarPanel, _super);
    function SidebarPanel(props) {
        var _this = _super.call(this, props) || this;
        _this.portalEl = getSidebarPanelContainer() || makePortal();
        return _this;
    }
    SidebarPanel.prototype.render = function () {
        var _a = this.props, orientation = _a.orientation, collapsed = _a.collapsed, hidePanel = _a.hidePanel, title = _a.title, children = _a.children, props = __rest(_a, ["orientation", "collapsed", "hidePanel", "title", "children"]);
        var sidebar = (<PanelContainer collapsed={collapsed} orientation={orientation} {...props}>
        {title && (<SidebarPanelHeader>
            <Title>{title}</Title>
            <PanelClose onClick={hidePanel}/>
          </SidebarPanelHeader>)}
        <SidebarPanelBody hasHeader={!!title}>{children}</SidebarPanelBody>
      </PanelContainer>);
        return ReactDOM.createPortal(sidebar, this.portalEl);
    };
    return SidebarPanel;
}(React.Component));
export default SidebarPanel;
var getPositionForOrientation = function (p) {
    return p.orientation === 'top'
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        top: ", ";\n        left: 0;\n        right: 0;\n      "], ["\n        top: ", ";\n        left: 0;\n        right: 0;\n      "])), p.theme.sidebar.mobileHeight) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n        width: 320px;\n        top: 0;\n        left: ", ";\n      "], ["\n        width: 320px;\n        top: 0;\n        left: ",
        ";\n      "])), p.collapsed
        ? p.theme.sidebar.collapsedWidth
        : p.theme.sidebar.expandedWidth);
};
var PanelContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: fixed;\n  bottom: 0;\n  display: flex;\n  flex-direction: column;\n  z-index: ", ";\n  background: ", ";\n  color: ", ";\n  border-right: 1px solid ", ";\n  box-shadow: 1px 0 2px rgba(0, 0, 0, 0.06);\n  text-align: left;\n  line-height: 24px;\n  animation: 200ms ", ";\n\n  ", ";\n"], ["\n  position: fixed;\n  bottom: 0;\n  display: flex;\n  flex-direction: column;\n  z-index: ", ";\n  background: ", ";\n  color: ", ";\n  border-right: 1px solid ", ";\n  box-shadow: 1px 0 2px rgba(0, 0, 0, 0.06);\n  text-align: left;\n  line-height: 24px;\n  animation: 200ms ", ";\n\n  ", ";\n"])), function (p) { return p.theme.zIndex.sidebarPanel; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.sidebar.background; }, function (p) { return p.theme.border; }, slideInLeft, getPositionForOrientation);
var SidebarPanelHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  background: ", ";\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);\n  height: 62px;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-shrink: 1;\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  background: ", ";\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);\n  height: 62px;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-shrink: 1;\n"])), function (p) { return p.theme.border; }, space(3), function (p) { return p.theme.background; });
var SidebarPanelBody = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n  overflow: auto;\n"], ["\n  flex-grow: 1;\n  overflow: auto;\n"])));
var PanelClose = styled(IconClose)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n  position: relative;\n  padding: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  cursor: pointer;\n  position: relative;\n  padding: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, space(0.75), function (p) { return p.theme.textColor; });
PanelClose.defaultProps = {
    size: 'lg',
};
var Title = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: 0;\n"], ["\n  font-size: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=sidebarPanel.jsx.map