import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var inlineStyle = function (p) {
    return p.inline
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        width: 50%;\n        padding-right: 10px;\n        flex-shrink: 0;\n      "], ["\n        width: 50%;\n        padding-right: 10px;\n        flex-shrink: 0;\n      "]))) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n        margin-bottom: ", ";\n      "], ["\n        margin-bottom: ", ";\n      "])), space(1));
};
var FieldDescription = styled('label')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: normal;\n  margin-bottom: 0;\n\n  ", ";\n"], ["\n  font-weight: normal;\n  margin-bottom: 0;\n\n  ", ";\n"])), inlineStyle);
export default FieldDescription;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=fieldDescription.jsx.map