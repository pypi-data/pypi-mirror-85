import React from 'react';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
var ProjectName = function (_a) {
    var orgSlug = _a.orgSlug, releaseVersion = _a.releaseVersion, project = _a.project;
    return (<GlobalSelectionLink to={{
        pathname: "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/",
        query: { project: project.id },
    }}>
    <ProjectBadge project={project} avatarSize={16}/>
  </GlobalSelectionLink>);
};
export default ProjectName;
//# sourceMappingURL=projectName.jsx.map