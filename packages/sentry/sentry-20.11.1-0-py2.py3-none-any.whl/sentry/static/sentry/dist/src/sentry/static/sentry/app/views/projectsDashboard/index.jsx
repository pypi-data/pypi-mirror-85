import { __extends, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import LazyLoad from 'react-lazyload';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import uniqBy from 'lodash/uniqBy';
import flatten from 'lodash/flatten';
import { withProfiler } from '@sentry/react';
import { sortProjects } from 'app/utils';
import { t } from 'app/locale';
import LoadingError from 'app/components/loadingError';
import Button from 'app/components/button';
import IdBadge from 'app/components/idBadge';
import NoProjectMessage from 'app/components/noProjectMessage';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import ProjectsStatsStore from 'app/stores/projectsStatsStore';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import LoadingIndicator from 'app/components/loadingIndicator';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withTeamsForUser from 'app/utils/withTeamsForUser';
import { IconAdd } from 'app/icons';
import Resources from './resources';
import TeamSection from './teamSection';
var Dashboard = /** @class */ (function (_super) {
    __extends(Dashboard, _super);
    function Dashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Dashboard.prototype.componentWillUnmount = function () {
        ProjectsStatsStore.reset();
    };
    Dashboard.prototype.render = function () {
        var _a = this.props, teams = _a.teams, params = _a.params, organization = _a.organization, loadingTeams = _a.loadingTeams, error = _a.error;
        if (loadingTeams) {
            return <LoadingIndicator />;
        }
        if (error) {
            return <LoadingError message="An error occurred while fetching your projects"/>;
        }
        var filteredTeams = teams.filter(function (team) { return team.projects.length; });
        filteredTeams.sort(function (team1, team2) { return team1.slug.localeCompare(team2.slug); });
        var projects = uniqBy(flatten(teams.map(function (teamObj) { return teamObj.projects; })), 'id');
        var favorites = projects.filter(function (project) { return project.isBookmarked; });
        var access = new Set(organization.access);
        var canCreateProjects = access.has('project:admin');
        var hasTeamAdminAccess = access.has('team:admin');
        var showEmptyMessage = projects.length === 0 && favorites.length === 0;
        var showResources = projects.length === 1 && !projects[0].firstEvent;
        if (showEmptyMessage) {
            return (<NoProjectMessage organization={organization} projects={projects}>
          {null}
        </NoProjectMessage>);
        }
        return (<React.Fragment>
        <SentryDocumentTitle title={t('Projects Dashboard')} objSlug={organization.slug}/>
        {projects.length > 0 && (<ProjectsHeader>
            <PageHeading>Projects</PageHeading>
            <Button size="small" disabled={!canCreateProjects} title={!canCreateProjects
            ? t('You do not have permission to create projects')
            : undefined} to={"/organizations/" + organization.slug + "/projects/new/"} icon={<IconAdd size="xs" isCircled/>} data-test-id="create-project">
              {t('Create Project')}
            </Button>
          </ProjectsHeader>)}

        {filteredTeams.map(function (team, index) {
            var showBorder = index !== teams.length - 1;
            return (<LazyLoad key={team.slug} once debounce={50} height={300} offset={300}>
              <TeamSection orgId={params.orgId} team={team} showBorder={showBorder} title={hasTeamAdminAccess ? (<TeamLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"}>
                      <IdBadge team={team} avatarSize={22}/>
                    </TeamLink>) : (<IdBadge team={team} avatarSize={22}/>)} projects={sortProjects(team.projects)} access={access}/>
            </LazyLoad>);
        })}

        {showResources && <Resources organization={organization}/>}
      </React.Fragment>);
    };
    Dashboard.propTypes = {
        teams: PropTypes.array,
        organization: SentryTypes.Organization,
        loadingTeams: PropTypes.bool,
        error: PropTypes.instanceOf(Error),
    };
    return Dashboard;
}(React.Component));
var OrganizationDashboard = function (props) { return (<OrganizationDashboardWrapper>
    <Dashboard {...props}/>
  </OrganizationDashboardWrapper>); };
var TeamLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var ProjectsHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  padding: ", " ", " 0 ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])), space(3), space(4), space(4));
var OrganizationDashboardWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
export { Dashboard };
export default withApi(withOrganization(withTeamsForUser(withProfiler(OrganizationDashboard))));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map