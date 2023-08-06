import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Terminal = function (_a) {
    var command = _a.command;
    return (<Wrapper>
    <Prompt>{'\u0024'}</Prompt>
    {command}
  </Wrapper>);
};
export default Terminal;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  padding: ", " ", ";\n  font-family: ", ";\n  color: ", ";\n  border-radius: ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  background: ", ";\n  padding: ", " ", ";\n  font-family: ", ";\n  color: ", ";\n  border-radius: ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.gray500; }, space(1.5), space(3), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.white; }, function (p) { return p.theme.borderRadius; }, space(0.75));
var Prompt = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=terminal.jsx.map