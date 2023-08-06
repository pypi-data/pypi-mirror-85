import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import TextOverflow from 'app/components/textOverflow';
import space from 'app/styles/space';
import { tct, t } from 'app/locale';
var SelectedOption = function (_a) {
    var id = _a.id, details = _a.details;
    return (<Wrapper>
    <ThreadId>{tct('Thread #[id]:', { id: id })}</ThreadId>
    <Label>{(details === null || details === void 0 ? void 0 : details.label) || "<" + t('unknown') + ">"}</Label>
  </Wrapper>);
};
export default SelectedOption;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: auto 1fr;\n  display: grid;\n"], ["\n  grid-template-columns: auto 1fr;\n  display: grid;\n"])));
var ThreadId = styled(TextOverflow)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: ", ";\n  max-width: 100%;\n  text-align: left;\n"], ["\n  padding-right: ", ";\n  max-width: 100%;\n  text-align: left;\n"])), space(1));
var Label = styled(ThreadId)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.blue300; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=selectedOption.jsx.map