import { __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Button from 'app/components/button';
import { slideInLeft, fadeIn } from 'app/styles/animations';
import { IconClose, IconMenu } from 'app/icons';
import SettingsBreadcrumb from './settingsBreadcrumb';
import SettingsHeader from './settingsHeader';
import SettingsSearch from './settingsSearch';
var SettingsLayout = /** @class */ (function (_super) {
    __extends(SettingsLayout, _super);
    function SettingsLayout() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            navVisible: false,
            navOffsetTop: 0,
        };
        _this.headerRef = React.createRef();
        return _this;
    }
    SettingsLayout.prototype.componentDidMount = function () {
        var _this = this;
        // Close the navigation when navigating.
        this.unlisten = browserHistory.listen(function () { return _this.toggleNav(false); });
    };
    SettingsLayout.prototype.componentWillUnmount = function () {
        this.unlisten();
    };
    SettingsLayout.prototype.toggleNav = function (navVisible) {
        var _a, _b;
        // when the navigation is opened, body should be scroll-locked
        this.toggleBodyScrollLock(navVisible);
        this.setState({
            navOffsetTop: (_b = (_a = this.headerRef.current) === null || _a === void 0 ? void 0 : _a.getBoundingClientRect().bottom) !== null && _b !== void 0 ? _b : 0,
            navVisible: navVisible,
        });
    };
    SettingsLayout.prototype.toggleBodyScrollLock = function (lock) {
        var bodyElement = document.getElementsByTagName('body')[0];
        if (window.scrollTo) {
            window.scrollTo(0, 0);
        }
        bodyElement.classList[lock ? 'add' : 'remove']('scroll-lock');
    };
    SettingsLayout.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, routes = _a.routes, route = _a.route, router = _a.router, renderNavigation = _a.renderNavigation, children = _a.children;
        var _b = this.state, navVisible = _b.navVisible, navOffsetTop = _b.navOffsetTop;
        // We want child's view's props
        var childProps = children && React.isValidElement(children) ? children.props : this.props;
        var childRoutes = childProps.routes || routes || [];
        var childRoute = childProps.route || route || {};
        var shouldRenderNavigation = typeof renderNavigation === 'function';
        return (<SettingsColumn>
        <SettingsHeader ref={this.headerRef}>
          <HeaderContent>
            {shouldRenderNavigation && (<NavMenuToggle priority="link" label={t('Open the menu')} icon={navVisible ? <IconClose aria-hidden/> : <IconMenu aria-hidden/>} onClick={function () { return _this.toggleNav(!navVisible); }}/>)}
            <StyledSettingsBreadcrumb params={params} routes={childRoutes} route={childRoute}/>
            <SettingsSearch routes={routes} router={router} params={params}/>
          </HeaderContent>
        </SettingsHeader>

        <MaxWidthContainer>
          {shouldRenderNavigation && (<SidebarWrapper isVisible={navVisible} offsetTop={navOffsetTop}>
              {renderNavigation()}
            </SidebarWrapper>)}
          <NavMask isVisible={navVisible} onClick={function () { return _this.toggleNav(false); }}/>
          <Content>{children}</Content>
        </MaxWidthContainer>
      </SettingsColumn>);
    };
    SettingsLayout.propTypes = {
        renderNavigation: PropTypes.func,
        route: PropTypes.object,
        router: PropTypes.object,
        routes: PropTypes.array,
    };
    return SettingsLayout;
}(React.Component));
var SettingsColumn = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex: 1; /* so this stretches vertically so that footer is fixed at bottom */\n  min-width: 0; /* fixes problem when child content stretches beyond layout width */\n  footer {\n    margin-top: 0;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex: 1; /* so this stretches vertically so that footer is fixed at bottom */\n  min-width: 0; /* fixes problem when child content stretches beyond layout width */\n  footer {\n    margin-top: 0;\n  }\n"])));
var HeaderContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var NavMenuToggle = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: none;\n  margin: -", " ", " -", " -", ";\n  padding: ", ";\n  color: ", ";\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: none;\n  margin: -", " ", " -", " -", ";\n  padding: ", ";\n  color: ", ";\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(1), space(1), space(1), space(1), space(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.breakpoints[0]; });
var StyledSettingsBreadcrumb = styled(SettingsBreadcrumb)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var MaxWidthContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  max-width: ", ";\n  flex: 1;\n"], ["\n  display: flex;\n  max-width: ", ";\n  flex: 1;\n"])), function (p) { return p.theme.settings.containerWidth; });
var SidebarWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex-shrink: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n\n  @media (max-width: ", ") {\n    display: ", ";\n    position: fixed;\n    top: ", "px;\n    bottom: 0;\n    overflow-y: auto;\n    animation: ", " 100ms ease-in-out;\n    z-index: ", ";\n    box-shadow: ", ";\n  }\n"], ["\n  flex-shrink: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n\n  @media (max-width: ", ") {\n    display: ", ";\n    position: fixed;\n    top: ", "px;\n    bottom: 0;\n    overflow-y: auto;\n    animation: ", " 100ms ease-in-out;\n    z-index: ", ";\n    box-shadow: ", ";\n  }\n"])), function (p) { return p.theme.settings.sidebarWidth; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[0]; }, function (p) { return (p.isVisible ? 'block' : 'none'); }, function (p) { return p.offsetTop; }, slideInLeft, function (p) { return p.theme.zIndex.settingsSidebarNav; }, function (p) { return p.theme.dropShadowHeavy; });
var NavMask = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: none;\n  @media (max-width: ", ") {\n    display: ", ";\n    background: rgba(0, 0, 0, 0.35);\n    height: 100%;\n    width: 100%;\n    position: absolute;\n    z-index: ", ";\n    animation: ", " 250ms ease-in-out;\n  }\n"], ["\n  display: none;\n  @media (max-width: ", ") {\n    display: ", ";\n    background: rgba(0, 0, 0, 0.35);\n    height: 100%;\n    width: 100%;\n    position: absolute;\n    z-index: ", ";\n    animation: ", " 250ms ease-in-out;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return (p.isVisible ? 'block' : 'none'); }, function (p) { return p.theme.zIndex.settingsSidebarNavMask; }, fadeIn);
/**
 * Note: `overflow: hidden` will cause some buttons in `SettingsPageHeader` to be cut off because it has negative margin.
 * Will also cut off tooltips.
 */
var Content = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n  min-width: 0; /* keep children from stretching container */\n"], ["\n  flex: 1;\n  padding: ", ";\n  min-width: 0; /* keep children from stretching container */\n"])), space(4));
export default SettingsLayout;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=settingsLayout.jsx.map