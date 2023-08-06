import React from 'react';
import { getMeta } from 'app/components/events/meta/metaProxy';
import withProjects from 'app/utils/withProjects';
import { generateEventSlug, eventDetailsRoute } from 'app/utils/discover/urls';
import Link from 'app/components/links/link';
import Highlight from 'app/components/highlight';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import Summary from './summary';
var Default = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm;
    return (<Summary kvData={breadcrumb.data} searchTerm={searchTerm}>
    {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) && (<AnnotatedText value={<FormatMessage searchTerm={searchTerm} event={event} orgId={orgId} breadcrumb={breadcrumb} message={breadcrumb.message}/>} meta={getMeta(breadcrumb, 'message')}/>)}
  </Summary>);
};
function isEventId(maybeEventId) {
    // maybeEventId is an event id if it's a hex string of 32 characters long
    return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
var FormatMessage = withProjects(function FormatMessageInner(_a) {
    var searchTerm = _a.searchTerm, event = _a.event, message = _a.message, breadcrumb = _a.breadcrumb, projects = _a.projects, loadingProjects = _a.loadingProjects, orgId = _a.orgId;
    var content = <Highlight text={searchTerm}>{message}</Highlight>;
    if (!loadingProjects &&
        typeof orgId === 'string' &&
        breadcrumb.category === 'sentry.transaction' &&
        isEventId(message)) {
        var maybeProject = projects.find(function (project) {
            return project.id === event.projectID;
        });
        if (!maybeProject) {
            return content;
        }
        var projectSlug = maybeProject.slug;
        var eventSlug = generateEventSlug({ project: projectSlug, id: message });
        return <Link to={eventDetailsRoute({ orgSlug: orgId, eventSlug: eventSlug })}>{content}</Link>;
    }
    return content;
});
export default Default;
//# sourceMappingURL=default.jsx.map