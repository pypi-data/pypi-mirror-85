import React from 'react';
import { openCreateTeamModal } from 'app/actionCreators/modal';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import recreateRoute from 'app/utils/recreateRoute';
import { IconAdd } from 'app/icons';
import AllTeamsList from './allTeamsList';
function OrganizationTeams(_a) {
    var allTeams = _a.allTeams, activeTeams = _a.activeTeams, organization = _a.organization, access = _a.access, features = _a.features, routes = _a.routes, params = _a.params;
    if (!organization) {
        return null;
    }
    var canCreateTeams = access.has('project:admin');
    var action = (<Button priority="primary" size="small" disabled={!canCreateTeams} title={!canCreateTeams ? t('You do not have permission to create teams') : undefined} onClick={function () {
        return openCreateTeamModal({
            organization: organization,
        });
    }} icon={<IconAdd size="xs" isCircled/>}>
      {t('Create Team')}
    </Button>);
    var teamRoute = routes.find(function (_a) {
        var path = _a.path;
        return path === 'teams/';
    });
    var urlPrefix = teamRoute
        ? recreateRoute(teamRoute, { routes: routes, params: params, stepBack: -2 })
        : '';
    var activeTeamIds = new Set(activeTeams.map(function (team) { return team.id; }));
    var otherTeams = allTeams.filter(function (team) { return !activeTeamIds.has(team.id); });
    var title = t('Teams');
    return (<div data-test-id="team-list">
      <SentryDocumentTitle title={title} objSlug={organization.slug}/>
      <SettingsPageHeader title={title} action={action}/>
      <Panel>
        <PanelHeader>{t('Your Teams')}</PanelHeader>
        <PanelBody>
          <AllTeamsList urlPrefix={urlPrefix} organization={organization} teamList={activeTeams} access={access} openMembership={false}/>
        </PanelBody>
      </Panel>
      <Panel>
        <PanelHeader>{t('Other Teams')}</PanelHeader>
        <PanelBody>
          <AllTeamsList urlPrefix={urlPrefix} organization={organization} teamList={otherTeams} access={access} openMembership={!!(features.has('open-membership') || access.has('org:write'))}/>
        </PanelBody>
      </Panel>
    </div>);
}
export default OrganizationTeams;
//# sourceMappingURL=organizationTeams.jsx.map