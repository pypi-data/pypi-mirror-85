/**
 * Create a slug that can be used with discover details views
 * or as a reference event for event-stats requests
 */
export function generateEventSlug(eventData) {
    var id = eventData.id || eventData.latest_event;
    var projectSlug = eventData.project || eventData['project.name'];
    return projectSlug + ":" + id;
}
/**
 * Create a URL to an event details view.
 */
export function eventDetailsRoute(_a) {
    var eventSlug = _a.eventSlug, orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/discover/" + eventSlug + "/";
}
/**
 * Create a URL target to event details with an event view in the query string.
 */
export function eventDetailsRouteWithEventView(_a) {
    var orgSlug = _a.orgSlug, eventSlug = _a.eventSlug, eventView = _a.eventView;
    var pathname = eventDetailsRoute({
        orgSlug: orgSlug,
        eventSlug: eventSlug,
    });
    return {
        pathname: pathname,
        query: eventView.generateQueryStringObject(),
    };
}
/**
 * Get the URL for the discover entry page which changes based on organization
 * feature flags.
 */
export function getDiscoverLandingUrl(organization) {
    if (organization.features.includes('discover-query')) {
        return "/organizations/" + organization.slug + "/discover/queries/";
    }
    return "/organizations/" + organization.slug + "/discover/results/";
}
//# sourceMappingURL=urls.jsx.map