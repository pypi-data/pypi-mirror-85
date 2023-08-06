import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Clipboard from 'app/components/clipboard';
import { IconCopy } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getShortEventId } from 'app/utils/events';
var Header = function (_a) {
    var traceID = _a.traceID;
    return (<Wrapper>
    <h4>{t('Issues with the same trace ID')}</h4>
    {traceID ? (<Clipboard value={traceID}>
        <ClipboardWrapper>
          <span>{getShortEventId(traceID)}</span>
          <IconCopy />
        </ClipboardWrapper>
      </Clipboard>) : (<span>{'-'}</span>)}
  </Wrapper>);
};
export default Header;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  h4 {\n    font-size: ", ";\n    color: ", ";\n    font-weight: normal;\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  h4 {\n    font-size: ", ";\n    color: ", ";\n    font-weight: normal;\n    margin-bottom: 0;\n  }\n"])), space(1), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; });
var ClipboardWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  &:hover {\n    cursor: pointer;\n  }\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=header.jsx.map