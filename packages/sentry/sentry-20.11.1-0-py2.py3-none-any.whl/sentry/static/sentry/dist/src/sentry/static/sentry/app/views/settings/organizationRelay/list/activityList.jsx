import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { PanelTable } from 'app/components/panels';
import DateTime from 'app/components/dateTime';
var ActivityList = function (_a) {
    var activities = _a.activities;
    return (<StyledPanelTable headers={[t('Version'), t('First Used'), t('Last Used')]}>
    {activities.map(function (_a) {
        var relayId = _a.relayId, version = _a.version, firstSeen = _a.firstSeen, lastSeen = _a.lastSeen;
        return (<React.Fragment key={relayId}>
          <div>{version}</div>
          <DateTime date={firstSeen} seconds={false}/>
          <DateTime date={lastSeen} seconds={false}/>
        </React.Fragment>);
    })}
  </StyledPanelTable>);
};
export default ActivityList;
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(3, 2fr);\n\n  @media (min-width: ", ") {\n    grid-template-columns: 2fr repeat(2, 1fr);\n  }\n"], ["\n  grid-template-columns: repeat(3, 2fr);\n\n  @media (min-width: ", ") {\n    grid-template-columns: 2fr repeat(2, 1fr);\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=activityList.jsx.map