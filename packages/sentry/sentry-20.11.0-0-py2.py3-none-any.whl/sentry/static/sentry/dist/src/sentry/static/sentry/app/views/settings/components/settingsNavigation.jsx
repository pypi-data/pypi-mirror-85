import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import SettingsNavigationGroup from 'app/views/settings/components/settingsNavigationGroup';
var SettingsNavigation = /** @class */ (function (_super) {
    __extends(SettingsNavigation, _super);
    function SettingsNavigation() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsNavigation.prototype.componentDidCatch = function (error, errorInfo) {
        Sentry.withScope(function (scope) {
            Object.keys(errorInfo).forEach(function (key) {
                scope.setExtra(key, errorInfo[key]);
            });
            scope.setExtra('url', window.location.href);
            Sentry.captureException(error);
        });
    };
    SettingsNavigation.prototype.render = function () {
        var _a = this.props, navigationObjects = _a.navigationObjects, hooks = _a.hooks, hookConfigs = _a.hookConfigs, stickyTop = _a.stickyTop, otherProps = __rest(_a, ["navigationObjects", "hooks", "hookConfigs", "stickyTop"]);
        var navWithHooks = navigationObjects.concat(hookConfigs);
        return (<PositionStickyWrapper stickyTop={stickyTop}>
        {navWithHooks.map(function (config) { return (<SettingsNavigationGroup key={config.name} {...otherProps} {...config}/>); })}
        {hooks.map(function (Hook, i) { return React.cloneElement(Hook, { key: "hook-" + i }); })}
      </PositionStickyWrapper>);
    };
    SettingsNavigation.defaultProps = {
        hooks: [],
        hookConfigs: [],
        stickyTop: '70px',
    };
    return SettingsNavigation;
}(React.Component));
var PositionStickyWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  padding-right: ", ";\n\n  @media (min-width: ", ") {\n    position: sticky;\n    top: ", ";\n    overflow: scroll;\n    height: calc(100vh - ", ");\n    -ms-overflow-style: none;\n    scrollbar-width: none;\n\n    &::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"], ["\n  padding: ", ";\n  padding-right: ", ";\n\n  @media (min-width: ", ") {\n    position: sticky;\n    top: ", ";\n    overflow: scroll;\n    height: calc(100vh - ", ");\n    -ms-overflow-style: none;\n    scrollbar-width: none;\n\n    &::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"])), space(4), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.stickyTop; }, function (p) { return p.stickyTop; });
export default SettingsNavigation;
var templateObject_1;
//# sourceMappingURL=settingsNavigation.jsx.map