import { __rest } from "tslib";
import React from 'react';
import ProjectContext from 'app/views/projects/projectContext';
import ProjectSettingsNavigation from 'app/views/settings/project/projectSettingsNavigation';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
import withOrganization from 'app/utils/withOrganization';
function ProjectSettingsLayout(_a) {
    var params = _a.params, organization = _a.organization, children = _a.children, props = __rest(_a, ["params", "organization", "children"]);
    var orgId = params.orgId, projectId = params.projectId;
    return (<ProjectContext orgId={orgId} projectId={projectId}>
      <SettingsLayout params={params} {...props} renderNavigation={function () { return <ProjectSettingsNavigation organization={organization}/>; }}>
        {children && React.isValidElement(children)
        ? React.cloneElement(children, {
            organization: organization,
        })
        : children}
      </SettingsLayout>
    </ProjectContext>);
}
export default withOrganization(ProjectSettingsLayout);
//# sourceMappingURL=projectSettingsLayout.jsx.map