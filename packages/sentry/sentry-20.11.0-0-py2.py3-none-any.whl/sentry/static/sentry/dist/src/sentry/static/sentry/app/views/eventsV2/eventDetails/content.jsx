import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import * as SpanEntryContext from 'app/components/events/interfaces/spans/context';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getMessage, getTitle } from 'app/utils/events';
import SentryTypes from 'app/sentryTypes';
import Button from 'app/components/button';
import Feature from 'app/components/acl/feature';
import RootSpanStatus from 'app/components/events/rootSpanStatus';
import OpsBreakdown from 'app/components/events/opsBreakdown';
import RealUserMonitoring from 'app/components/events/realUserMonitoring';
import EventMetadata from 'app/components/events/eventMetadata';
import LoadingError from 'app/components/loadingError';
import NotFound from 'app/components/errors/notFound';
import TagsTable from 'app/components/tagsTable';
import AsyncComponent from 'app/components/asyncComponent';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import Projects from 'app/utils/projects';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { eventDetailsRoute } from 'app/utils/discover/urls';
import * as Layout from 'app/components/layouts/thirds';
import ButtonBar from 'app/components/buttonBar';
import { FIELD_TAGS } from 'app/utils/discover/fields';
import LoadingIndicator from 'app/components/loadingIndicator';
import { generateTitle, getExpandedResults } from '../utils';
import LinkedIssue from './linkedIssue';
import DiscoverBreadcrumb from '../breadcrumb';
var slugValidator = function (props, propName, componentName) {
    var value = props[propName];
    // Accept slugs that look like:
    // * project-slug:deadbeef
    if (value && typeof value === 'string' && !/^(?:[^:]+):(?:[a-f0-9-]+)$/.test(value)) {
        return new Error("Invalid value for " + propName + " provided to " + componentName + ".");
    }
    return null;
};
var EventDetailsContent = /** @class */ (function (_super) {
    __extends(EventDetailsContent, _super);
    function EventDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            event: undefined,
            // local state
            isSidebarVisible: true,
        };
        _this.toggleSidebar = function () {
            _this.setState({ isSidebarVisible: !_this.state.isSidebarVisible });
        };
        _this.generateTagKey = function (tag) {
            // Some tags may be normalized from context, but not all of them are.
            // This supports a user making a custom tag with the same name as one
            // that comes from context as all of these are also tags.
            if (tag.key in FIELD_TAGS) {
                return "tags[" + tag.key + "]";
            }
            return tag.key;
        };
        _this.generateTagUrl = function (tag) {
            var _a;
            var _b = _this.props, eventView = _b.eventView, organization = _b.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var eventReference = __assign({}, event);
            if (eventReference.id) {
                delete eventReference.id;
            }
            var tagKey = _this.generateTagKey(tag);
            var nextView = getExpandedResults(eventView, (_a = {}, _a[tagKey] = tag.value, _a), eventReference);
            return nextView.getResultsViewUrlTarget(organization.slug);
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, eventView = _a.eventView;
        var eventSlug = params.eventSlug;
        var query = eventView.getEventsAPIPayload(location);
        // Fields aren't used, reduce complexity by omitting from query entirely
        query.field = [];
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        // Get a specific event. This could be coming from
        // a paginated group or standalone event.
        return [['event', url, { query: query }]];
    };
    Object.defineProperty(EventDetailsContent.prototype, "projectId", {
        get: function () {
            return this.props.eventSlug.split(':')[0];
        },
        enumerable: false,
        configurable: true
    });
    EventDetailsContent.prototype.renderBody = function () {
        var event = this.state.event;
        if (!event) {
            return <NotFound />;
        }
        return this.renderContent(event);
    };
    EventDetailsContent.prototype.renderContent = function (event) {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, eventView = _b.eventView;
        var isSidebarVisible = this.state.isSidebarVisible;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'discover_v2.event_details',
            eventName: 'Discoverv2: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var transactionName = (_a = event.tags.find(function (tag) { return tag.key === 'transaction'; })) === null || _a === void 0 ? void 0 : _a.value;
        var transactionSummaryTarget = event.type === 'transaction' && transactionName
            ? transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: location.query,
            })
            : null;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <DiscoverBreadcrumb eventView={eventView} event={event} organization={organization} location={location}/>
            <EventHeader event={event} organization={organization}/>
          </Layout.HeaderContent>
          <StyledHeaderActions>
            <ButtonBar gap={1}>
              <Button onClick={this.toggleSidebar}>
                {isSidebarVisible ? 'Hide Details' : 'Show Details'}
              </Button>
              {transactionSummaryTarget && (<Feature organization={organization} features={['performance-view']}>
                  {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<Button disabled={!hasFeature} priority="primary" to={transactionSummaryTarget}>
                      {t('Go to Summary')}
                    </Button>);
        }}
                </Feature>)}
            </ButtonBar>
          </StyledHeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth={!isSidebarVisible}>
            <Projects orgId={organization.slug} slugs={[this.projectId]}>
              {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded;
            return initiallyLoaded ? (<SpanEntryContext.Provider value={{
                getViewChildTransactionTarget: function (childTransactionProps) {
                    var childTransactionLink = eventDetailsRoute({
                        eventSlug: childTransactionProps.eventSlug,
                        orgSlug: organization.slug,
                    });
                    return {
                        pathname: childTransactionLink,
                        query: eventView.generateQueryStringObject(),
                    };
                },
            }}>
                    <BorderlessEventEntries organization={organization} event={event} project={projects[0]} location={location} showExampleCommit={false} showTagSummary={false}/>
                  </SpanEntryContext.Provider>) : (<LoadingIndicator />);
        }}
            </Projects>
          </Layout.Main>
          {isSidebarVisible && (<Layout.Side>
              <EventMetadata event={event} organization={organization} projectId={this.projectId}/>
              <RootSpanStatus event={event}/>
              <OpsBreakdown event={event}/>
              <RealUserMonitoring event={event}/>
              {event.groupID && (<LinkedIssue groupId={event.groupID} eventId={event.eventID}/>)}
              <TagsTable generateUrl={this.generateTagUrl} event={event} query={eventView.query}/>
            </Layout.Side>)}
        </Layout.Body>
      </React.Fragment>);
    };
    EventDetailsContent.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        var permissionDenied = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 403; });
        if (notFound) {
            return <NotFound />;
        }
        if (permissionDenied) {
            return (<LoadingError message={t('You do not have permission to view that event.')}/>);
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    EventDetailsContent.prototype.renderComponent = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        var event = this.state.event;
        var title = generateTitle({ eventView: eventView, event: event, organization: organization });
        return (<SentryDocumentTitle title={title} objSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </SentryDocumentTitle>);
    };
    EventDetailsContent.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        eventSlug: slugValidator,
        location: PropTypes.object.isRequired,
    };
    return EventDetailsContent;
}(AsyncComponent));
var EventHeader = function (_a) {
    var event = _a.event, organization = _a.organization;
    var title = getTitle(event, organization).title;
    var message = getMessage(event);
    return (<Layout.Title data-test-id="event-header">
      <span>
        {title}
        {message && message.length > 0 ? ':' : null}
      </span>
      <EventSubheading>{getMessage(event)}</EventSubheading>
    </Layout.Title>);
};
var StyledHeaderActions = styled(Layout.HeaderActions)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var EventSubheading = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
export default EventDetailsContent;
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map