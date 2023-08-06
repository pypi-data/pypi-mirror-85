import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var CommandLine = function (_a) {
    var children = _a.children;
    return <Wrapper>{children}</Wrapper>;
};
export default CommandLine;
var Wrapper = styled('code')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n  font-family: ", ";\n  font-size: ", ";\n  white-space: nowrap;\n"], ["\n  padding: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n  font-family: ", ";\n  font-size: ", ";\n  white-space: nowrap;\n"])), space(0.5), space(1), function (p) { return p.theme.pink300; }, function (p) { return p.theme.pink100; }, function (p) { return p.theme.pink200; }, function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1;
//# sourceMappingURL=commandLine.jsx.map