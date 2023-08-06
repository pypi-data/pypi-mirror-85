import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
var ListItem = styled(function (_a) {
    var children = _a.children, className = _a.className, symbol = _a.symbol;
    return (<li className={className}>
    {symbol && <Symbol>{symbol}</Symbol>}
    {children}
  </li>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  ", "\n"], ["\n  position: relative;\n  ", "\n"])), function (p) { return p.symbol && "padding-left: 34px;"; });
var Symbol = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: absolute;\n  top: 0;\n  left: 0;\n  min-height: 22.5px;\n"], ["\n  display: flex;\n  align-items: center;\n  position: absolute;\n  top: 0;\n  left: 0;\n  min-height: 22.5px;\n"])));
export default ListItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=listItem.jsx.map