import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PageContent, PageHeader } from 'app/styles/organization';
import { t } from 'app/locale';
import space from 'app/styles/space';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import IncidentRulesDetails from 'app/views/settings/incidentRules/details';
import IssueEditor from 'app/views/settings/projectAlerts/issueEditor';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
function ProjectAlertsEditor(props) {
    var hasMetricAlerts = props.hasMetricAlerts, location = props.location, params = props.params, organization = props.organization, project = props.project;
    var projectId = params.projectId;
    var alertType = location.pathname.includes('/alerts/metric-rules/')
        ? 'metric'
        : 'issue';
    var title = t('Edit Alert Rule');
    return (<React.Fragment>
      <SentryDocumentTitle title={title} objSlug={projectId}/>
      <PageContent>
        <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} title={title}/>
        <StyledPageHeader>
          <PageHeading>{title}</PageHeading>
        </StyledPageHeader>
        {(!hasMetricAlerts || alertType === 'issue') && (<IssueEditor {...props} project={project}/>)}

        {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesDetails {...props} project={project}/>)}
      </PageContent>
    </React.Fragment>);
}
var StyledPageHeader = styled(PageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
export default ProjectAlertsEditor;
var templateObject_1;
//# sourceMappingURL=edit.jsx.map