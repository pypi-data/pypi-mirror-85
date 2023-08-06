import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { sortProjects } from 'app/utils';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import ProjectListItem from 'app/views/settings/components/settingsProjectItem';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import routeTitleGen from 'app/utils/routeTitle';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import { IconAdd } from 'app/icons';
import { decodeScalar } from 'app/utils/queryString';
import ProjectStatsGraph from './projectStatsGraph';
var ITEMS_PER_PAGE = 50;
var OrganizationProjects = /** @class */ (function (_super) {
    __extends(OrganizationProjects, _super);
    function OrganizationProjects() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationProjects.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        var location = this.props.location;
        var query = decodeScalar(location.query.query);
        return [
            [
                'projectList',
                "/organizations/" + orgId + "/projects/",
                {
                    query: {
                        query: query,
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
            [
                'projectStats',
                "/organizations/" + orgId + "/stats/",
                {
                    query: {
                        since: new Date().getTime() / 1000 - 3600 * 24,
                        stat: 'generated',
                        group: 'project',
                        per_page: ITEMS_PER_PAGE,
                    },
                },
            ],
        ];
    };
    OrganizationProjects.prototype.getTitle = function () {
        var organization = this.props.organization;
        return routeTitleGen(t('Projects'), organization.slug, false);
    };
    OrganizationProjects.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationProjects.prototype.renderBody = function () {
        var _a = this.state, projectList = _a.projectList, projectListPageLinks = _a.projectListPageLinks, projectStats = _a.projectStats;
        var organization = this.props.organization;
        var canCreateProjects = new Set(organization.access).has('project:admin');
        var action = (<Button priority="primary" size="small" disabled={!canCreateProjects} title={!canCreateProjects
            ? t('You do not have permission to create projects')
            : undefined} to={"/organizations/" + organization.slug + "/projects/new/"} icon={<IconAdd size="xs" isCircled/>}>
        {t('Create Project')}
      </Button>);
        return (<React.Fragment>
        <SettingsPageHeader title="Projects" action={action}/>
        <Panel>
          <PanelHeader hasButtons>
            {t('Projects')}

            {this.renderSearchInput({
            updateRoute: true,
            placeholder: t('Search Projects'),
            className: 'search',
        })}
          </PanelHeader>
          <PanelBody>
            {projectList ? (sortProjects(projectList).map(function (project) { return (<GridPanelItem key={project.id}>
                  <ProjectListItemWrapper>
                    <ProjectListItem project={project} organization={organization}/>
                  </ProjectListItemWrapper>
                  <ProjectStatsGraphWrapper>
                    {projectStats ? (<ProjectStatsGraph key={project.id} project={project} stats={projectStats[project.id]}/>) : (<Placeholder height="25px"/>)}
                  </ProjectStatsGraphWrapper>
                </GridPanelItem>); })) : (<LoadingIndicator />)}
            {projectList && projectList.length === 0 && (<EmptyMessage>{t('No projects found.')}</EmptyMessage>)}
          </PanelBody>
        </Panel>
        {projectListPageLinks && (<Pagination pageLinks={projectListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return OrganizationProjects;
}(AsyncView));
export default withOrganization(OrganizationProjects);
var GridPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: 0;\n"])));
var ProjectListItemWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n  flex: 1;\n"], ["\n  padding: ", ";\n  flex: 1;\n"])), space(2));
var ProjectStatsGraphWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n  width: 25%;\n  margin-left: ", ";\n"], ["\n  padding: ", ";\n  width: 25%;\n  margin-left: ", ";\n"])), space(2), space(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map