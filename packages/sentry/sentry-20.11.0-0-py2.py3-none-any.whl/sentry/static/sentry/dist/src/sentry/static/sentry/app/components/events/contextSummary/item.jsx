import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import space from 'app/styles/space';
var Item = function (_a) {
    var children = _a.children, icon = _a.icon, className = _a.className;
    return (<Wrapper className={classNames('context-item', className)}>
    {icon}
    {children && <Details>{children}</Details>}
  </Wrapper>);
};
export default Item;
var Details = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-width: 100%;\n  min-height: 48px;\n"], ["\n  max-width: 100%;\n  min-height: 48px;\n"])));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: ", " 0 ", " 64px;\n  display: flex;\n  align-items: center;\n  position: relative;\n  min-height: 67px;\n\n  @media (min-width: ", ") {\n    border: 0;\n    padding: ", " 0px 0px 64px;\n    min-height: 48px;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  padding: ", " 0 ", " 64px;\n  display: flex;\n  align-items: center;\n  position: relative;\n  min-height: 67px;\n\n  @media (min-width: ", ") {\n    border: 0;\n    padding: ", " 0px 0px 64px;\n    min-height: 48px;\n  }\n"])), function (p) { return p.theme.innerBorder; }, space(2), space(2), function (p) { return p.theme.breakpoints[0]; }, space(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=item.jsx.map