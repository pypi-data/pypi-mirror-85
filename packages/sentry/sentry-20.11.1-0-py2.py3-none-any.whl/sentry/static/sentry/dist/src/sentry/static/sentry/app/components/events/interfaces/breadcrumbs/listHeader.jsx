import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { IconSwitch } from 'app/icons';
import { GridCell } from './styles';
var getTimeTooltipTitle = function (displayRelativeTime) {
    if (displayRelativeTime) {
        return t('Switch to absolute');
    }
    return t('Switch to relative');
};
var ListHeader = React.memo(function (_a) {
    var onSwitchTimeFormat = _a.onSwitchTimeFormat, displayRelativeTime = _a.displayRelativeTime;
    return (<React.Fragment>
    <StyledGridCell>{t('Type')}</StyledGridCell>
    <Category>{t('Category')}</Category>
    <StyledGridCell>{t('Description')}</StyledGridCell>
    <StyledGridCell>{t('Level')}</StyledGridCell>
    <Time onClick={onSwitchTimeFormat}>
      <Tooltip title={getTimeTooltipTitle(displayRelativeTime)}>
        <StyledIconSwitch size="xs"/>
      </Tooltip>
      <span> {t('Time')}</span>
    </Time>
  </React.Fragment>);
});
export default ListHeader;
var StyledGridCell = styled(GridCell)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: sticky;\n  z-index: ", ";\n  top: 0;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  line-height: 1;\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n    font-size: ", ";\n  }\n"], ["\n  position: sticky;\n  z-index: ", ";\n  top: 0;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  line-height: 1;\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.zIndex.breadcrumbs.header; }, function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.breakpoints[0]; }, space(2), space(2), function (p) { return p.theme.fontSizeSmall; });
var Category = styled(StyledGridCell)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var Time = styled(StyledGridCell)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: pointer;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: pointer;\n"])), space(1));
var StyledIconSwitch = styled(IconSwitch)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  transition: 0.15s color;\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.15s color;\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=listHeader.jsx.map