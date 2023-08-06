import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconDelete, IconStats, IconUpgrade } from 'app/icons';
import ConfirmDelete from 'app/components/confirmDelete';
import { t } from 'app/locale';
import space from 'app/styles/space';
var ActionButtons = function (_a) {
    var org = _a.org, app = _a.app, showPublish = _a.showPublish, showDelete = _a.showDelete, onPublish = _a.onPublish, onDelete = _a.onDelete, disablePublishReason = _a.disablePublishReason, disableDeleteReason = _a.disableDeleteReason;
    var appDashboardButton = (<StyledButton size="small" icon={<IconStats />} to={"/settings/" + org.slug + "/developer-settings/" + app.slug + "/dashboard/"}>
      {t('Dashboard')}
    </StyledButton>);
    var publishRequestButton = showPublish ? (<StyledButton disabled={!!disablePublishReason} title={disablePublishReason} icon={<IconUpgrade />} size="small" onClick={onPublish}>
      {t('Publish')}
    </StyledButton>) : null;
    var deleteConfirmMessage = t("Deleting " + app.slug + " will also delete any and all of its installations.          This is a permanent action. Do you wish to continue?");
    var deleteButton = showDelete ? (disableDeleteReason ? (<StyledButton disabled title={disableDeleteReason} size="small" icon={<IconDelete />} label="Delete"/>) : (onDelete && (<ConfirmDelete message={deleteConfirmMessage} confirmInput={app.slug} priority="danger" onConfirm={function () { return onDelete(app); }}>
          <StyledButton size="small" icon={<IconDelete />} label="Delete"/>
        </ConfirmDelete>))) : null;
    return (<ButtonHolder>
      {appDashboardButton}
      {publishRequestButton}
      {deleteButton}
    </ButtonHolder>);
};
var ButtonHolder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-direction: row;\n  display: flex;\n  & > * {\n    margin-left: ", ";\n  }\n"], ["\n  flex-direction: row;\n  display: flex;\n  & > * {\n    margin-left: ", ";\n  }\n"])), space(0.5));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export default ActionButtons;
var templateObject_1, templateObject_2;
//# sourceMappingURL=actionButtons.jsx.map