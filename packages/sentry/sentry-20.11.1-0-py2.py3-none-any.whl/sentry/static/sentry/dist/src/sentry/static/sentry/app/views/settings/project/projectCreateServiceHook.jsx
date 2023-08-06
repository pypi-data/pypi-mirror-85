import React from 'react';
import DocumentTitle from 'react-document-title';
import { t } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ServiceHookSettingsForm from 'app/views/settings/project/serviceHookSettingsForm';
function ProjectCreateServiceHook(_a) {
    var params = _a.params;
    var orgId = params.orgId, projectId = params.projectId;
    var title = t('Create Service Hook');
    return (<DocumentTitle title={title + " - Sentry"}>
      <React.Fragment>
        <SettingsPageHeader title={title}/>
        <ServiceHookSettingsForm orgId={orgId} projectId={projectId} initialData={{ events: [], isActive: true }}/>
      </React.Fragment>
    </DocumentTitle>);
}
export default ProjectCreateServiceHook;
//# sourceMappingURL=projectCreateServiceHook.jsx.map