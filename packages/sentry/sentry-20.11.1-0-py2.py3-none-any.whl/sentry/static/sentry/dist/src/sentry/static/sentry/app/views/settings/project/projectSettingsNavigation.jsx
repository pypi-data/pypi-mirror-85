import React from 'react';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
import getConfiguration from 'app/views/settings/project/navigationConfiguration';
import withProject from 'app/utils/withProject';
var ProjectSettingsNavigation = function (_a) {
    var organization = _a.organization, project = _a.project;
    return (<SettingsNavigation navigationObjects={getConfiguration({ project: project, organization: organization })} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} project={project}/>);
};
export default withProject(ProjectSettingsNavigation);
//# sourceMappingURL=projectSettingsNavigation.jsx.map