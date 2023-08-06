import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { SectionHeading } from 'app/components/charts/styles';
import DateTime from 'app/components/dateTime';
import ExternalLink from 'app/components/links/externalLink';
import FileSize from 'app/components/fileSize';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import Projects from 'app/utils/projects';
/**
 * Render metadata about the event and provide a link to the JSON blob.
 * Used in the sidebar of performance event details and discover2 event details.
 */
function EventMetadata(_a) {
    var event = _a.event, organization = _a.organization, projectId = _a.projectId;
    var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + projectId + "/events/" + event.eventID + "/json/";
    return (<MetaDataID>
      <SectionHeading>{t('Event ID')}</SectionHeading>
      <MetadataContainer data-test-id="event-id">{event.eventID}</MetadataContainer>
      <MetadataContainer>
        <DateTime date={getDynamicText({
        value: event.dateCreated || (event.endTimestamp || 0) * 1000,
        fixed: 'Dummy timestamp',
    })}/>
      </MetadataContainer>
      <Projects orgId={organization.slug} slugs={[projectId]}>
        {function (_a) {
        var projects = _a.projects;
        var project = projects.find(function (p) { return p.slug === projectId; });
        return (<StyledProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>);
    }}
      </Projects>
      <MetadataJSON href={eventJsonUrl} className="json-link">
        {t('Preview JSON')} (<FileSize bytes={event.size}/>)
      </MetadataJSON>
    </MetaDataID>);
}
var MetaDataID = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var MetadataContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var MetadataJSON = styled(ExternalLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledProjectBadge = styled(ProjectBadge)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export default EventMetadata;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventMetadata.jsx.map