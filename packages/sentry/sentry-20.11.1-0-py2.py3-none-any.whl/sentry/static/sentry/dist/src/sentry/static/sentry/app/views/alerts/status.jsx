import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { IconCheckmark, IconWarning, IconFire } from 'app/icons';
import { IncidentStatus } from './types';
var Status = function (_a) {
    var className = _a.className, incident = _a.incident, disableIconColor = _a.disableIconColor;
    var status = incident.status;
    var isResolved = status === IncidentStatus.CLOSED;
    var isWarning = status === IncidentStatus.WARNING;
    var icon = isResolved ? (<IconCheckmark color={disableIconColor ? undefined : 'green300'}/>) : isWarning ? (<IconWarning color={disableIconColor ? undefined : 'orange400'}/>) : (<IconFire color={disableIconColor ? undefined : 'red300'}/>);
    var text = isResolved ? t('Resolved') : isWarning ? t('Warning') : t('Critical');
    return (<Wrapper className={className}>
      <Icon>{icon}</Icon>
      {text}
    </Wrapper>);
};
export default Status;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n"])), space(0.75));
var Icon = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: -3px;\n"], ["\n  margin-bottom: -3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=status.jsx.map