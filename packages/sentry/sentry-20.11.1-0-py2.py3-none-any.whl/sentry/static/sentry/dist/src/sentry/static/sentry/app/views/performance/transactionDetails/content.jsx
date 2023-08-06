import { __assign, __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import SentryTypes from 'app/sentryTypes';
import EventMetadata from 'app/components/events/eventMetadata';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import * as SpanEntryContext from 'app/components/events/interfaces/spans/context';
import Button from 'app/components/button';
import LoadingError from 'app/components/loadingError';
import NotFound from 'app/components/errors/notFound';
import AsyncComponent from 'app/components/asyncComponent';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import RootSpanStatus from 'app/components/events/rootSpanStatus';
import OpsBreakdown from 'app/components/events/opsBreakdown';
import RealUserMonitoring from 'app/components/events/realUserMonitoring';
import TagsTable from 'app/components/tagsTable';
import Projects from 'app/utils/projects';
import * as Layout from 'app/components/layouts/thirds';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { decodeScalar, appendTagCondition } from 'app/utils/queryString';
import { transactionSummaryRouteWithQuery } from '../transactionSummary/utils';
import { getTransactionDetailsUrl } from '../utils';
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
        _this.generateTagUrl = function (tag) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var query = decodeScalar(location.query.query) || '';
            var newQuery = __assign(__assign({}, location.query), { query: appendTagCondition(query, tag.key, tag.value) });
            return transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: event.title,
                projectID: decodeScalar(location.query.project),
                query: newQuery,
            });
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var eventSlug = params.eventSlug;
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        return [['event', url]];
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
        var _a = this.props, organization = _a.organization, location = _a.location, eventSlug = _a.eventSlug;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'performance.event_details',
            eventName: 'Performance: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var isSidebarVisible = this.state.isSidebarVisible;
        var transactionName = event.title;
        var query = decodeScalar(location.query.query) || '';
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} transactionName={transactionName} eventSlug={eventSlug}/>
            <Layout.Title data-test-id="event-header">{event.title}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <Button onClick={this.toggleSidebar}>
              {isSidebarVisible ? 'Hide Details' : 'Show Details'}
            </Button>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth={!isSidebarVisible}>
            <Projects orgId={organization.slug} slugs={[this.projectId]}>
              {function (_a) {
            var projects = _a.projects;
            return (<SpanEntryContext.Provider value={{
                getViewChildTransactionTarget: function (childTransactionProps) {
                    return getTransactionDetailsUrl(organization, childTransactionProps.eventSlug, childTransactionProps.transaction, location.query);
                },
            }}>
                  <BorderlessEventEntries organization={organization} event={event} project={projects[0]} showExampleCommit={false} showTagSummary={false} location={location}/>
                </SpanEntryContext.Provider>);
        }}
            </Projects>
          </Layout.Main>
          {isSidebarVisible && (<Layout.Side>
              <EventMetadata event={event} organization={organization} projectId={this.projectId}/>
              <RootSpanStatus event={event}/>
              <OpsBreakdown event={event}/>
              <RealUserMonitoring event={event}/>
              <TagsTable event={event} query={query} generateUrl={this.generateTagUrl}/>
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
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={t('Performance - Event Details')} objSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </SentryDocumentTitle>);
    };
    EventDetailsContent.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        eventSlug: PropTypes.string.isRequired,
        location: PropTypes.object.isRequired,
    };
    return EventDetailsContent;
}(AsyncComponent));
export default EventDetailsContent;
//# sourceMappingURL=content.jsx.map