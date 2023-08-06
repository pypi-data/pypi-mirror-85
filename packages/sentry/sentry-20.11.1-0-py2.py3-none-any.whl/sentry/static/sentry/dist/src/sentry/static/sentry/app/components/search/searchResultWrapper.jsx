import { __makeTemplateObject, __rest } from "tslib";
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import React from 'react';
var SearchResultWrapper = styled(function (_a) {
    var highlighted = _a.highlighted, props = __rest(_a, ["highlighted"]);
    return (<div {...props} ref={function (element) { var _a; return highlighted && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}/>);
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n  display: block;\n  color: ", ";\n  padding: 10px;\n  scroll-margin: 120px;\n\n  ", ";\n\n  &:not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n"], ["\n  cursor: pointer;\n  display: block;\n  color: ", ";\n  padding: 10px;\n  scroll-margin: 120px;\n\n  ",
    ";\n\n  &:not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) {
    return p.highlighted && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      color: ", ";\n      background: ", ";\n    "], ["\n      color: ", ";\n      background: ", ";\n    "])), p.theme.purple300, p.theme.backgroundSecondary);
}, function (p) { return p.theme.innerBorder; });
export default SearchResultWrapper;
var templateObject_1, templateObject_2;
//# sourceMappingURL=searchResultWrapper.jsx.map