import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import QuestionTooltip from 'app/components/questionTooltip';
var ReleaseStat = function (_a) {
    var label = _a.label, children = _a.children, help = _a.help;
    return (<Wrapper>
    <Label hasHelp={!!help}>
      {label}
      {help && <StyledQuestionTooltip title={help} size="xs" position="top"/>}
    </Label>
    <Value>{children}</Value>
  </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    margin: ", " ", " ", " 0;\n  }\n"], ["\n  @media (max-width: ", ") {\n    margin: ", " ", " ", " 0;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(2), space(4), space(2));
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 600;\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  line-height: 1.3;\n  margin-bottom: ", ";\n  white-space: nowrap;\n  display: flex;\n  @media (min-width: ", ") {\n    justify-content: flex-end;\n  }\n"], ["\n  font-weight: 600;\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  line-height: 1.3;\n  margin-bottom: ", ";\n  white-space: nowrap;\n  display: flex;\n  @media (min-width: ", ") {\n    justify-content: flex-end;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space(0.25), function (p) { return p.theme.breakpoints[1]; });
var StyledQuestionTooltip = styled(QuestionTooltip)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
var Value = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return p.theme.textColor; });
export default ReleaseStat;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=releaseStat.jsx.map