import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ActivityAuthor from 'app/components/activity/author';
import ConfigStore from 'app/stores/configStore';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import Tooltip from 'app/components/tooltip';
import EditorTools from './editorTools';
var NoteHeader = function (_a) {
    var authorName = _a.authorName, user = _a.user, onEdit = _a.onEdit, onDelete = _a.onDelete;
    var activeUser = ConfigStore.get('user');
    var canEdit = activeUser && (activeUser.isSuperuser || user.id === activeUser.id);
    return (<div>
      <ActivityAuthor>{authorName}</ActivityAuthor>
      {canEdit && (<EditorTools>
          <Tooltip title={t('You can edit this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <Edit onClick={onEdit}>{t('Edit')}</Edit>
          </Tooltip>
          <Tooltip title={t('You can delete this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <LinkWithConfirmation title={t('Remove')} message={t('Are you sure you wish to delete this comment?')} onConfirm={onDelete}>
              <Remove>{t('Remove')}</Remove>
            </LinkWithConfirmation>
          </Tooltip>
        </EditorTools>)}
    </div>);
};
var getActionStyle = function (p) { return "\n  padding: 0 7px;\n  color: " + p.theme.gray200 + ";\n  font-weight: normal;\n"; };
var Edit = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  margin-left: 7px;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  ", ";\n  margin-left: 7px;\n\n  &:hover {\n    color: ", ";\n  }\n"])), getActionStyle, function (p) { return p.theme.gray300; });
var Remove = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  border-left: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  ", ";\n  border-left: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), getActionStyle, function (p) { return p.theme.border; }, function (p) { return p.theme.error; });
export default NoteHeader;
var templateObject_1, templateObject_2;
//# sourceMappingURL=header.jsx.map