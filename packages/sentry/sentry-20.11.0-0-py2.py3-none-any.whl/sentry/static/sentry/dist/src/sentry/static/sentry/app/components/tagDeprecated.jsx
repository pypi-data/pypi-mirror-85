import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
/**
 * Get priority from alerts or badge styles
 */
var getPriority = function (p) {
    var _a, _b;
    if (p.priority) {
        return (_b = (_a = p.theme.alert[p.priority]) !== null && _a !== void 0 ? _a : p.theme.badge[p.priority]) !== null && _b !== void 0 ? _b : null;
    }
    return null;
};
var getMarginLeft = function (p) {
    return p.inline ? "margin-left: " + (p.size === 'small' ? '0.25em' : '0.5em') + ";" : '';
};
var getBorder = function (p) { var _a, _b; return p.border ? "border: 1px solid " + ((_b = (_a = getPriority(p)) === null || _a === void 0 ? void 0 : _a.border) !== null && _b !== void 0 ? _b : p.theme.border) + ";" : ''; };
var Tag = styled(function (_a) {
    var children = _a.children, icon = _a.icon, _inline = _a.inline, _priority = _a.priority, _size = _a.size, _border = _a.border, props = __rest(_a, ["children", "icon", "inline", "priority", "size", "border"]);
    return (<div {...props}>
      {icon && (<IconWrapper>
          {React.isValidElement(icon) && React.cloneElement(icon, { size: 'xs' })}
        </IconWrapper>)}
      {children}
    </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-flex;\n  box-sizing: border-box;\n  padding: ", ";\n  font-size: ", ";\n  line-height: 1;\n  color: ", ";\n  text-align: center;\n  white-space: nowrap;\n  vertical-align: middle;\n  align-items: center;\n  border-radius: ", ";\n  text-transform: lowercase;\n  font-weight: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n"], ["\n  display: inline-flex;\n  box-sizing: border-box;\n  padding: ", ";\n  font-size: ", ";\n  line-height: 1;\n  color: ", ";\n  text-align: center;\n  white-space: nowrap;\n  vertical-align: middle;\n  align-items: center;\n  border-radius: ", ";\n  text-transform: lowercase;\n  font-weight: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n"])), function (p) { return (p.size === 'small' ? '0.1em 0.4em 0.2em' : '0.35em 0.8em 0.4em'); }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return (p.priority ? p.theme.background : p.theme.textColor); }, function (p) { return (p.size === 'small' ? '0.25em' : '2em'); }, function (p) { return (p.size === 'small' ? 'bold' : 'normal'); }, function (p) { var _a, _b; return (_b = (_a = getPriority(p)) === null || _a === void 0 ? void 0 : _a.background) !== null && _b !== void 0 ? _b : p.theme.gray100; }, function (p) { return getBorder(p); }, function (p) { return getMarginLeft(p); });
var IconWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
export default Tag;
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagDeprecated.jsx.map