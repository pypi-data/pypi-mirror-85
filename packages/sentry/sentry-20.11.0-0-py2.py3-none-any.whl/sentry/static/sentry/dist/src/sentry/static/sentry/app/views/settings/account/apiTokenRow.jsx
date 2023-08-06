import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconSubtract } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Button from 'app/components/button';
import DateTime from 'app/components/dateTime';
import { PanelItem } from 'app/components/panels';
import getDynamicText from 'app/utils/getDynamicText';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
function ApiTokenRow(_a) {
    var token = _a.token, onRemove = _a.onRemove;
    return (<StyledPanelItem>
      <Controls>
        <InputWrapper>
          <TextCopyInput>
            {getDynamicText({ value: token.token, fixed: 'CI_AUTH_TOKEN' })}
          </TextCopyInput>
        </InputWrapper>
        <Button size="small" onClick={function () { return onRemove(token); }} icon={<IconSubtract isCircled size="xs"/>}>
          {t('Remove')}
        </Button>
      </Controls>

      <Details>
        <ScopesWrapper>
          <Heading>{t('Scopes')}</Heading>
          <ScopeList>{token.scopes.join(', ')}</ScopeList>
        </ScopesWrapper>
        <div>
          <Heading>{t('Created')}</Heading>
          <Time>
            <DateTime date={getDynamicText({
        value: token.dateCreated,
        fixed: new Date(1508208080000),
    })}/>
          </Time>
        </div>
      </Details>
    </StyledPanelItem>);
}
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-direction: column;\n  padding: ", ";\n"], ["\n  flex-direction: column;\n  padding: ", ";\n"])), space(2));
var Controls = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(1));
var InputWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  font-size: ", ";\n  flex: 1;\n  margin-right: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, space(1));
var Details = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  margin-top: ", ";\n"])), space(1));
var ScopesWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ScopeList = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Time = styled('time')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Heading = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space(1));
export default ApiTokenRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=apiTokenRow.jsx.map