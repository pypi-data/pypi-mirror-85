import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import TextBlock from 'app/views/settings/components/text/textBlock';
import space from 'app/styles/space';
var EmptyMessage = styled(function (_a) {
    var title = _a.title, description = _a.description, icon = _a.icon, children = _a.children, action = _a.action, _leftAligned = _a.leftAligned, props = __rest(_a, ["title", "description", "icon", "children", "action", "leftAligned"]);
    return (<div data-test-id="empty-message" {...props}>
      {icon && <IconWrapper>{icon}</IconWrapper>}
      {title && <Title>{title}</Title>}
      {description && <Description>{description}</Description>}
      {children && <Description noMargin>{children}</Description>}
      {action && <Action>{action}</Action>}
    </div>);
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  ", ";\n  flex-direction: column;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  ",
    ";\n  flex-direction: column;\n  color: ", ";\n  font-size: ",
    ";\n"])), function (p) {
    return p.leftAligned
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n          max-width: 70%;\n          align-items: flex-start;\n          padding: ", ";\n        "], ["\n          max-width: 70%;\n          align-items: flex-start;\n          padding: ", ";\n        "])), space(4)) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n          text-align: center;\n          align-items: center;\n          padding: ", " 15%;\n        "], ["\n          text-align: center;\n          align-items: center;\n          padding: ", " 15%;\n        "])), space(4));
}, function (p) { return p.theme.textColor; }, function (p) {
    return p.size && p.size === 'large' ? p.theme.fontSizeExtraLarge : p.theme.fontSizeLarge;
});
EmptyMessage.propTypes = {
    title: PropTypes.node,
    description: PropTypes.node,
    icon: PropTypes.node,
    action: PropTypes.element,
    // Currently only the `large` option changes the size - can add more size options as necessary
    size: PropTypes.oneOf(['large', 'medium']),
};
var IconWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray200; }, space(1));
var Title = styled('strong')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var Description = styled(TextBlock)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var Action = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
export default EmptyMessage;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=emptyMessage.jsx.map