import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import { ProjectTableLayout, ProjectTableDataElement, } from 'app/views/organizationStats/projectTableLayout';
import Count from 'app/components/count';
import { formatPercentage } from 'app/utils/formatters';
import space from 'app/styles/space';
var ProjectTable = function (_a) {
    var projectMap = _a.projectMap, projectTotals = _a.projectTotals, orgTotal = _a.orgTotal, organization = _a.organization;
    var getPercent = function (item, total) {
        if (total === 0) {
            return '';
        }
        return formatPercentage(item / total, 0);
    };
    if (!projectTotals) {
        return null;
    }
    var elements = projectTotals
        .sort(function (a, b) { return b.received - a.received; })
        .map(function (item, index) {
        var project = projectMap[item.id];
        if (!project) {
            return null;
        }
        var projectLink = "/settings/" + organization.slug + "/projects/" + project.slug + "/";
        return (<StyledProjectTableLayout key={index}>
          <StyledProjectTitle>
            <Link to={projectLink}>{project.slug}</Link>
          </StyledProjectTitle>
          <ProjectTableDataElement>
            <Count value={item.accepted}/>
            <Percentage>{getPercent(item.accepted, orgTotal.accepted)}</Percentage>
          </ProjectTableDataElement>
          <ProjectTableDataElement>
            <Count value={item.rejected}/>
            <Percentage>{getPercent(item.rejected, orgTotal.rejected)}</Percentage>
          </ProjectTableDataElement>
          <ProjectTableDataElement>
            <Count value={item.blacklisted}/>
            <Percentage>{getPercent(item.blacklisted, orgTotal.blacklisted)}</Percentage>
          </ProjectTableDataElement>
          <ProjectTableDataElement>
            <Count value={item.received}/>
            <Percentage>{getPercent(item.received, orgTotal.received)}</Percentage>
          </ProjectTableDataElement>
        </StyledProjectTableLayout>);
    });
    return <React.Fragment>{elements}</React.Fragment>;
};
var StyledProjectTitle = styled(ProjectTableDataElement)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"], ["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"])));
var StyledProjectTableLayout = styled(ProjectTableLayout)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(2), function (p) { return p.theme.innerBorder; });
var Percentage = styled(function (_a) {
    var children = _a.children, props = __rest(_a, ["children"]);
    if (children === '') {
        return null;
    }
    return <div {...props}>{children}</div>;
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n  color: ", ";\n  font-size: 12px;\n  line-height: 1.2;\n"], ["\n  margin-top: ", ";\n  color: ", ";\n  font-size: 12px;\n  line-height: 1.2;\n"])), space(0.25), function (p) { return p.theme.gray300; });
export default ProjectTable;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTable.jsx.map