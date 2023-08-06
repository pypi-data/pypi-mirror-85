import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import ConfirmDelete from 'app/components/confirmDelete';
import ButtonBar from 'app/components/buttonBar';
import QuestionTooltip from 'app/components/questionTooltip';
import DateTime from 'app/components/dateTime';
import { IconEdit, IconDelete, IconCopy } from 'app/icons';
import space from 'app/styles/space';
import Clipboard from 'app/components/clipboard';
var CardHeader = function (_a) {
    var publicKey = _a.publicKey, name = _a.name, description = _a.description, created = _a.created, onEdit = _a.onEdit, onDelete = _a.onDelete;
    return (<Header>
    <MainInfo>
      <Name>
        <div>{name}</div>
        {description && <QuestionTooltip position="top" size="sm" title={description}/>}
      </Name>
      <Date>
        {tct('Created on [date]', { date: <DateTime date={created} timeAndDate/> })}
      </Date>
    </MainInfo>
    <ButtonBar gap={1}>
      <Clipboard value={publicKey}>
        <Button size="small" icon={<IconCopy />}>
          {t('Copy Key')}
        </Button>
      </Clipboard>
      <Button size="small" onClick={onEdit(publicKey)} icon={<IconEdit />} label={t('Edit Key')}/>
      <ConfirmDelete message={t('After removing this Public Key, your Relay will no longer be able to communicate with Sentry and events will be dropped.')} onConfirm={onDelete(publicKey)} confirmInput={name}>
        <Button size="small" icon={<IconDelete />} label={t('Delete Key')}/>
      </ConfirmDelete>
    </ButtonBar>
  </Header>);
};
export default CardHeader;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; });
var Name = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), space(0.5));
var MainInfo = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.textColor; }, space(1));
var Date = styled('small')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=cardHeader.jsx.map