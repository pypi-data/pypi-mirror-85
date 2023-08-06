import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import OrganizationAvatar from 'app/components/avatar/organizationAvatar';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { tn } from 'app/locale';
var SidebarOrgSummary = function (_a) {
    var organization = _a.organization;
    var fullOrg = organization;
    var projects = fullOrg.projects && fullOrg.projects.length;
    var extra = [];
    if (projects) {
        extra.push(tn('%s project', '%s projects', projects));
    }
    return (<OrgSummary>
      <OrganizationAvatar organization={organization} size={36}/>

      <Details>
        <SummaryOrgName>{organization.name}</SummaryOrgName>
        {!!extra.length && <SummaryOrgDetails>{extra.join(', ')}</SummaryOrgDetails>}
      </Details>
    </OrgSummary>);
};
var OrgSummary = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  padding: 10px 15px;\n  overflow: hidden;\n"], ["\n  display: flex;\n  padding: 10px 15px;\n  overflow: hidden;\n"])));
var SummaryOrgName = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 16px;\n  line-height: 1.1;\n  font-weight: bold;\n  margin-bottom: 4px;\n  ", ";\n"], ["\n  color: ", ";\n  font-size: 16px;\n  line-height: 1.1;\n  font-weight: bold;\n  margin-bottom: 4px;\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis);
var SummaryOrgDetails = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 14px;\n  line-height: 1;\n  ", ";\n"], ["\n  color: ", ";\n  font-size: 14px;\n  line-height: 1;\n  ", ";\n"])), function (p) { return p.theme.subText; }, overflowEllipsis);
var Details = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  padding-left: 10px;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  padding-left: 10px;\n  overflow: hidden;\n"])));
// Needed for styling in SidebarMenuItem
export { OrgSummary };
export default SidebarOrgSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sidebarOrgSummary.jsx.map