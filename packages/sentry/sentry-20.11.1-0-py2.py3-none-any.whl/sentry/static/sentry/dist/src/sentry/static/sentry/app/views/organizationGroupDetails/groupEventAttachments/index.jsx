import React from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import GroupEventAttachments from './groupEventAttachments';
var GroupEventAttachmentsContainer = function (_a) {
    var organization = _a.organization, group = _a.group;
    return (<Feature features={['event-attachments']} organization={organization} renderDisabled={function (props) { return <FeatureDisabled {...props}/>; }}>
    <GroupEventAttachments projectSlug={group.project.slug}/>
  </Feature>);
};
export default withOrganization(GroupEventAttachmentsContainer);
//# sourceMappingURL=index.jsx.map