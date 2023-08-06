import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import overflowEllipsisLeft from 'app/styles/overflowEllipsisLeft';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var TextOverflow = styled(function (_a) {
    var isParagraph = _a.isParagraph, className = _a.className, children = _a.children;
    var Component = isParagraph ? 'p' : 'div';
    return <Component className={className}>{children}</Component>;
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  width: auto;\n"], ["\n  ", ";\n  width: auto;\n"])), function (p) { return (p.ellipsisDirection === 'right' ? overflowEllipsis : overflowEllipsisLeft); });
TextOverflow.defaultProps = {
    ellipsisDirection: 'right',
    isParagraph: false,
};
export default TextOverflow;
var templateObject_1;
//# sourceMappingURL=textOverflow.jsx.map