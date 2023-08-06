import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ListItem from 'app/components/list/listItem';
import space from 'app/styles/space';
var Item = styled(function (_a) {
    var title = _a.title, subtitle = _a.subtitle, children = _a.children, className = _a.className;
    return (<ListItem className={className}>
    {title}
    {subtitle && <small>{subtitle}</small>}
    <div>{children}</div>
  </ListItem>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
export default Item;
var templateObject_1;
//# sourceMappingURL=item.jsx.map