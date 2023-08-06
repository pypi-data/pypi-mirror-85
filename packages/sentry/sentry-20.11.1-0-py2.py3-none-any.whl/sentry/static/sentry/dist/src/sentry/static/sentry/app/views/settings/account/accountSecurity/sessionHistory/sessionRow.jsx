import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PanelItem } from 'app/components/panels';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import { tableLayout } from './utils';
function SessionRow(_a) {
    var ipAddress = _a.ipAddress, lastSeen = _a.lastSeen, firstSeen = _a.firstSeen, countryCode = _a.countryCode, regionCode = _a.regionCode;
    return (<SessionPanelItem>
      <IpAndLocation>
        <IpAddress>{ipAddress}</IpAddress>
        {countryCode && regionCode && (<CountryCode>{countryCode + " (" + regionCode + ")"}</CountryCode>)}
      </IpAndLocation>
      <StyledTimeSince date={firstSeen}/>
      <StyledTimeSince date={lastSeen}/>
    </SessionPanelItem>);
}
export default SessionRow;
var IpAddress = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-weight: bold;\n"], ["\n  margin-bottom: ", ";\n  font-weight: bold;\n"])), space(0.5));
var CountryCode = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var StyledTimeSince = styled(TimeSince)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var IpAndLocation = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var SessionPanelItem = styled(PanelItem)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), tableLayout);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sessionRow.jsx.map