import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { getListSymbolStyle, listSymbol } from './utils';
var List = styled(function (_a) {
    var children = _a.children, className = _a.className, symbol = _a.symbol, props = __rest(_a, ["children", "className", "symbol"]);
    var getWrapperComponent = function () {
        switch (symbol) {
            case 'numeric':
            case 'colored-numeric':
                return 'ol';
            default:
                return 'ul';
        }
    };
    var Wrapper = getWrapperComponent();
    return (<Wrapper className={className} {...props}>
      {!symbol || typeof symbol === 'string'
        ? children
        : React.Children.map(children, function (child) {
            if (!React.isValidElement(child)) {
                return child;
            }
            return React.cloneElement(child, {
                symbol: symbol,
            });
        })}
    </Wrapper>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0;\n  padding: 0;\n  list-style: none;\n  display: grid;\n  grid-gap: ", ";\n  ", "\n"], ["\n  margin: 0;\n  padding: 0;\n  list-style: none;\n  display: grid;\n  grid-gap: ", ";\n  ",
    "\n"])), space(0.5), function (p) {
    return typeof p.symbol === 'string' &&
        listSymbol[p.symbol] &&
        getListSymbolStyle(p.theme, p.symbol);
});
export default List;
var templateObject_1;
//# sourceMappingURL=index.jsx.map