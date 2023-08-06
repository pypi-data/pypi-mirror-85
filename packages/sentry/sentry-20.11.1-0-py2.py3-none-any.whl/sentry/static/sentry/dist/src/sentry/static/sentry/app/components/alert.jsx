import { __makeTemplateObject, __rest } from "tslib";
import { css } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var DEFAULT_TYPE = 'info';
var getAlertColorStyles = function (_a) {
    var backgroundLight = _a.backgroundLight, border = _a.border, iconColor = _a.iconColor;
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  svg {\n    color: ", ";\n  }\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  svg {\n    color: ", ";\n  }\n"])), backgroundLight, border, iconColor);
};
var getSystemAlertColorStyles = function (_a) {
    var backgroundLight = _a.backgroundLight, border = _a.border, iconColor = _a.iconColor;
    return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  border: 0;\n  border-radius: 0;\n  border-bottom: 1px solid ", ";\n  svg {\n    color: ", ";\n  }\n"], ["\n  background: ", ";\n  border: 0;\n  border-radius: 0;\n  border-bottom: 1px solid ", ";\n  svg {\n    color: ", ";\n  }\n"])), backgroundLight, border, iconColor);
};
var alertStyles = function (_a) {
    var theme = _a.theme, _b = _a.type, type = _b === void 0 ? DEFAULT_TYPE : _b, system = _a.system;
    return css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  margin: 0 0 ", ";\n  padding: ", " ", ";\n  font-size: 15px;\n  box-shadow: ", ";\n  border-radius: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n\n  a:not([role='button']) {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n  }\n\n  ", ";\n  ", ";\n"], ["\n  display: flex;\n  margin: 0 0 ", ";\n  padding: ", " ", ";\n  font-size: 15px;\n  box-shadow: ", ";\n  border-radius: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n\n  a:not([role='button']) {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n  }\n\n  ", ";\n  ", ";\n"])), space(3), space(1.5), space(2), theme.dropShadowLight, theme.borderRadius, theme.backgroundSecondary, theme.border, theme.textColor, theme.textColor, getAlertColorStyles(theme.alert[type]), system && getSystemAlertColorStyles(theme.alert[type]));
};
var IconWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 22px;\n  align-items: center;\n"], ["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 22px;\n  align-items: center;\n"])), space(1));
var StyledTextBlock = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  line-height: 1.5;\n  flex-grow: 1;\n  position: relative;\n  margin: auto;\n"], ["\n  line-height: 1.5;\n  flex-grow: 1;\n  position: relative;\n  margin: auto;\n"])));
var Alert = styled(function (_a) {
    var type = _a.type, icon = _a.icon, children = _a.children, className = _a.className, _system = _a.system, // don't forward to `div`
    props = __rest(_a, ["type", "icon", "children", "className", "system"]);
    return (<div className={classNames(type ? "ref-" + type : '', className)} {...props}>
        {icon && <IconWrapper>{icon}</IconWrapper>}
        <StyledTextBlock>{children}</StyledTextBlock>
      </div>);
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), alertStyles);
Alert.propTypes = {
    type: PropTypes.oneOf(['muted', 'info', 'warning', 'success', 'error', 'beta']),
    icon: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
    system: PropTypes.bool,
};
Alert.defaultProps = {
    type: DEFAULT_TYPE,
};
export { alertStyles };
export default Alert;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=alert.jsx.map