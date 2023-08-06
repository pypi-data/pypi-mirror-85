import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import PageHeading from 'app/components/pageHeading';
import TeamMembers from './teamMembers';
import ProjectCard from './projectCard';
var TeamSection = function (_a) {
    var team = _a.team, projects = _a.projects, title = _a.title, showBorder = _a.showBorder, orgId = _a.orgId, access = _a.access;
    var hasTeamAccess = access.has('team:read');
    var hasProjectAccess = access.has('project:read');
    return (<TeamSectionWrapper data-test-id="team" showBorder={showBorder}>
      <TeamTitleBar>
        <TeamName>{title}</TeamName>
        {hasTeamAccess && team && <TeamMembers teamId={team.slug} orgId={orgId}/>}
      </TeamTitleBar>
      <ProjectCards>
        {projects.map(function (project) { return (<ProjectCard data-test-id={project.slug} key={project.slug} project={project} hasProjectAccess={hasProjectAccess}/>); })}
      </ProjectCards>
    </TeamSectionWrapper>);
};
TeamSection.propTypes = {
    team: SentryTypes.Team,
    orgId: PropTypes.string,
    showBorder: PropTypes.bool,
    access: PropTypes.object,
    title: PropTypes.node,
    projects: PropTypes.array,
};
var ProjectCards = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(100px, 1fr));\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[3]; });
var TeamSectionWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: ", ";\n  padding: 0 ", " ", ";\n"], ["\n  border-bottom: ", ";\n  padding: 0 ", " ", ";\n"])), function (p) { return (p.showBorder ? '1px solid ' + p.theme.border : 0); }, space(4), space(4));
var TeamTitleBar = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " 0 ", ";\n"])), space(3), space(2));
var TeamName = styled(PageHeading)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 20px;\n  line-height: 24px; /* We need this so that header doesn't flicker when lazy loading because avatarList height > this */\n"], ["\n  font-size: 20px;\n  line-height: 24px; /* We need this so that header doesn't flicker when lazy loading because avatarList height > this */\n"])));
export default TeamSection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=teamSection.jsx.map