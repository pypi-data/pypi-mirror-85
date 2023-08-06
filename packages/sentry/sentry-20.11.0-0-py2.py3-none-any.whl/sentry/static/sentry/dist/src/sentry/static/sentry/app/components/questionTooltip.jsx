import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { IconQuestion } from 'app/icons';
var QuestionIconContainer = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n\n  & svg {\n    transition: 120ms color;\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n\n  & svg {\n    transition: 120ms color;\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
function QuestionTooltip(_a) {
    var title = _a.title, size = _a.size, className = _a.className, tooltipProps = __rest(_a, ["title", "size", "className"]);
    return (<QuestionIconContainer size={size} className={className}>
      <Tooltip title={title} {...tooltipProps}>
        <IconQuestion size={size}/>
      </Tooltip>
    </QuestionIconContainer>);
}
export default QuestionTooltip;
var templateObject_1;
//# sourceMappingURL=questionTooltip.jsx.map