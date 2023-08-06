import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ControlState from 'app/views/settings/components/forms/field/controlState';
import { t } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import { IconClose, IconCheckmark } from 'app/icons';
import { EventIdStatus } from '../../types';
var EventIdFieldStatusIcon = function (_a) {
    var status = _a.status, onClickIconClose = _a.onClickIconClose;
    switch (status) {
        case EventIdStatus.ERROR:
        case EventIdStatus.INVALID:
        case EventIdStatus.NOT_FOUND:
            return (<CloseIcon onClick={onClickIconClose}>
          <Tooltip title={t('Clear event ID')}>
            <StyledIconClose size="xs"/>
          </Tooltip>
        </CloseIcon>);
        case EventIdStatus.LOADING:
            return <ControlState isSaving/>;
        case EventIdStatus.LOADED:
            return <IconCheckmark color="green300"/>;
        default:
            return null;
    }
};
export default EventIdFieldStatusIcon;
var CloseIcon = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  :first-child {\n    line-height: 0;\n  }\n"], ["\n  :first-child {\n    line-height: 0;\n  }\n"])));
var StyledIconClose = styled(IconClose)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: pointer;\n"], ["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: pointer;\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventIdFieldStatusIcon.jsx.map