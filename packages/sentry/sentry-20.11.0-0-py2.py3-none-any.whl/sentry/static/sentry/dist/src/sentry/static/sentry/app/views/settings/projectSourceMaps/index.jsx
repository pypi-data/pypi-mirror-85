import React from 'react';
import withOrganization from 'app/utils/withOrganization';
function ProjectSourceMapsContainer(props) {
    var children = props.children, organization = props.organization, project = props.project;
    return React.isValidElement(children)
        ? React.cloneElement(children, { organization: organization, project: project })
        : null;
}
export default withOrganization(ProjectSourceMapsContainer);
//# sourceMappingURL=index.jsx.map