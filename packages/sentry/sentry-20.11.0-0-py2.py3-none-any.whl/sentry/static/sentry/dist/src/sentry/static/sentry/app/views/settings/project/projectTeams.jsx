import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { addTeamToProject, removeTeamFromProject } from 'app/actionCreators/projects';
import { openCreateTeamModal } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Link from 'app/components/links/link';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TeamSelect from 'app/views/settings/components/teamSelect';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import routeTitleGen from 'app/utils/routeTitle';
var ProjectTeams = /** @class */ (function (_super) {
    __extends(ProjectTeams, _super);
    function ProjectTeams() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.canCreateTeam = function () {
            var organization = _this.props.organization;
            var access = new Set(organization.access);
            return (access.has('org:write') && access.has('team:write') && access.has('project:write'));
        };
        _this.handleRemove = function (teamSlug) {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            removeTeamFromProject(_this.api, orgId, projectId, teamSlug)
                .then(function () { return _this.handleRemovedTeam(teamSlug); })
                .catch(function () {
                addErrorMessage(t('Could not remove the %s team', teamSlug));
                _this.setState({ loading: false });
            });
        };
        _this.handleRemovedTeam = function (teamSlug) {
            _this.setState(function (prevState) { return ({
                projectTeams: __spread((prevState.projectTeams || []).filter(function (team) { return team.slug !== teamSlug; })),
            }); });
        };
        _this.handleAddedTeam = function (team) {
            _this.setState(function (prevState) { return ({
                projectTeams: __spread(prevState.projectTeams, [team]),
            }); });
        };
        _this.handleAdd = function (team) {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            addTeamToProject(_this.api, orgId, projectId, team).then(function () {
                _this.handleAddedTeam(team);
            }, function () {
                _this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
        _this.handleCreateTeam = function (e) {
            var _a = _this.props, project = _a.project, organization = _a.organization;
            if (!_this.canCreateTeam()) {
                return;
            }
            e.stopPropagation();
            e.preventDefault();
            openCreateTeamModal({
                project: project,
                organization: organization,
                onClose: function (data) {
                    addTeamToProject(_this.api, organization.slug, project.slug, data).then(_this.remountComponent, _this.remountComponent);
                },
            });
        };
        return _this;
    }
    ProjectTeams.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['projectTeams', "/projects/" + orgId + "/" + projectId + "/teams/"]];
    };
    ProjectTeams.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Project Teams'), projectId, false);
    };
    ProjectTeams.prototype.renderBody = function () {
        var _a;
        var _b = this.props, params = _b.params, organization = _b.organization;
        var canCreateTeam = this.canCreateTeam();
        var hasAccess = organization.access.includes('project:write');
        var confirmRemove = t('This is the last team with access to this project. Removing it will mean ' +
            'only organization owners and managers will be able to access the project pages. Are ' +
            'you sure you want to remove this team from the project %s?', params.projectId);
        var projectTeams = this.state.projectTeams;
        var selectedTeams = (_a = projectTeams === null || projectTeams === void 0 ? void 0 : projectTeams.map(function (_a) {
            var slug = _a.slug;
            return slug;
        })) !== null && _a !== void 0 ? _a : [];
        var menuHeader = (<StyledTeamsLabel>
        {t('Teams')}
        <Tooltip disabled={canCreateTeam} title={t('You must be a project admin to create teams')} position="top">
          <StyledCreateTeamLink to="" disabled={!canCreateTeam} onClick={this.handleCreateTeam}>
            {t('Create Team')}
          </StyledCreateTeamLink>
        </Tooltip>
      </StyledTeamsLabel>);
        return (<div>
        <SettingsPageHeader title={t('%s Teams', params.projectId)}/>
        <TeamSelect organization={organization} selectedTeams={selectedTeams} onAddTeam={this.handleAdd} onRemoveTeam={this.handleRemove} menuHeader={menuHeader} confirmLastTeamRemoveMessage={confirmRemove} disabled={!hasAccess}/>
      </div>);
    };
    return ProjectTeams;
}(AsyncView));
var StyledTeamsLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 0.875em;\n  padding: ", " 0px;\n  text-transform: uppercase;\n"], ["\n  font-size: 0.875em;\n  padding: ", " 0px;\n  text-transform: uppercase;\n"])), space(0.5));
var StyledCreateTeamLink = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  float: right;\n  text-transform: none;\n  ", ";\n"], ["\n  float: right;\n  text-transform: none;\n  ",
    ";\n"])), function (p) {
    return p.disabled && css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n      cursor: not-allowed;\n      color: ", ";\n      opacity: 0.6;\n    "], ["\n      cursor: not-allowed;\n      color: ", ";\n      opacity: 0.6;\n    "])), p.theme.gray300);
});
export default ProjectTeams;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTeams.jsx.map