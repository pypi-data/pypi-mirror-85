import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { analytics } from 'app/utils/analytics';
import { logException } from 'app/utils/logging';
import { objectIsEmpty } from 'app/utils';
import { t } from 'app/locale';
import CspInterface from 'app/components/events/interfaces/csp';
import DebugMetaInterface from 'app/components/events/interfaces/debugMeta';
import EventAttachments from 'app/components/events/eventAttachments';
import EventCause from 'app/components/events/eventCause';
import EventCauseEmpty from 'app/components/events/eventCauseEmpty';
import EventContextSummary from 'app/components/events/contextSummary/contextSummary';
import EventContexts from 'app/components/events/contexts';
import EventDataSection from 'app/components/events/eventDataSection';
import EventDevice from 'app/components/events/device';
import EventErrors from 'app/components/events/errors';
import EventExtraData from 'app/components/events/eventExtraData/eventExtraData';
import EventGroupingInfo from 'app/components/events/groupingInfo';
import EventPackageData from 'app/components/events/packageData';
import EventSdk from 'app/components/events/eventSdk';
import EventSdkUpdates from 'app/components/events/sdkUpdates';
import EventTags from 'app/components/events/eventTags/eventTags';
import EventUserFeedback from 'app/components/events/userFeedback';
import ExceptionInterface from 'app/components/events/interfaces/exception';
import GenericInterface from 'app/components/events/interfaces/generic';
import MessageInterface from 'app/components/events/interfaces/message';
import RequestInterface from 'app/components/events/interfaces/request';
import RRWebIntegration from 'app/components/events/rrwebIntegration';
import SentryTypes from 'app/sentryTypes';
import BreadcrumbsInterface from 'app/components/events/interfaces/breadcrumbs';
import SpansInterface from 'app/components/events/interfaces/spans';
import StacktraceInterface from 'app/components/events/interfaces/stacktrace';
import TemplateInterface from 'app/components/events/interfaces/template';
import ThreadsInterface from 'app/components/events/interfaces/threads/threads';
import { DataSection } from 'app/components/events/styles';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
export var INTERFACES = {
    exception: ExceptionInterface,
    message: MessageInterface,
    request: RequestInterface,
    stacktrace: StacktraceInterface,
    template: TemplateInterface,
    csp: CspInterface,
    expectct: GenericInterface,
    expectstaple: GenericInterface,
    hpkp: GenericInterface,
    breadcrumbs: BreadcrumbsInterface,
    threads: ThreadsInterface,
    debugmeta: DebugMetaInterface,
    spans: SpansInterface,
};
var defaultProps = {
    isShare: false,
    showExampleCommit: false,
    showTagSummary: true,
};
var EventEntries = /** @class */ (function (_super) {
    __extends(EventEntries, _super);
    function EventEntries() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventEntries.prototype.componentDidMount = function () {
        var event = this.props.event;
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        var errors = event.errors;
        var errorTypes = errors.map(function (errorEntries) { return errorEntries.type; });
        var errorMessages = errors.map(function (errorEntries) { return errorEntries.message; });
        this.recordIssueError(errorTypes, errorMessages);
    };
    EventEntries.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, event = _a.event, showExampleCommit = _a.showExampleCommit;
        return ((event && nextProps.event && event.id !== nextProps.event.id) ||
            showExampleCommit !== nextProps.showExampleCommit);
    };
    EventEntries.prototype.recordIssueError = function (errorTypes, errorMessages) {
        var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
        var orgId = organization.id;
        var platform = project.platform;
        analytics('issue_error_banner.viewed', __assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform: platform })));
    };
    EventEntries.prototype.renderEntries = function () {
        var _a = this.props, event = _a.event, project = _a.project, organization = _a.organization, isShare = _a.isShare;
        var entries = event && event.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map(function (entry, entryIdx) {
            try {
                var Component = INTERFACES[entry.type];
                if (!Component) {
                    /*eslint no-console:0*/
                    window.console &&
                        console.error &&
                        console.error('Unregistered interface: ' + entry.type);
                    return null;
                }
                return (<Component key={'entry-' + entryIdx} projectId={project ? project.slug : null} orgId={organization ? organization.slug : null} event={event} type={entry.type} data={entry.data} isShare={isShare}/>);
            }
            catch (ex) {
                logException(ex);
                return (<EventDataSection type={entry.type} title={entry.type}>
            <p>{t('There was an error rendering this data.')}</p>
          </EventDataSection>);
            }
        });
    };
    EventEntries.prototype.render = function () {
        var _a = this.props, className = _a.className, organization = _a.organization, group = _a.group, isShare = _a.isShare, project = _a.project, event = _a.event, showExampleCommit = _a.showExampleCommit, showTagSummary = _a.showTagSummary, location = _a.location;
        var features = organization && organization.features ? new Set(organization.features) : new Set();
        var hasQueryFeature = features.has('discover-query');
        if (!event) {
            return (<div style={{ padding: '15px 30px' }}>
          <h3>{t('Latest Event Not Available')}</h3>
        </div>);
        }
        var hasContext = !objectIsEmpty(event.user) || !objectIsEmpty(event.contexts);
        var hasErrors = !objectIsEmpty(event.errors);
        return (<div className={className} data-test-id="event-entries">
        {hasErrors && (<ErrorContainer>
            <EventErrors event={event}/>
          </ErrorContainer>)}
        {!isShare &&
            (showExampleCommit ? (<EventCauseEmpty organization={organization} project={project}/>) : (<EventCause organization={organization} project={project} event={event} group={group}/>))}
        {(event === null || event === void 0 ? void 0 : event.userReport) && group && (<StyledEventUserFeedback report={event.userReport} orgId={organization.slug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {hasContext && showTagSummary && <EventContextSummary event={event}/>}
        {showTagSummary && (<EventTags event={event} orgId={organization.slug} projectId={project.slug} location={location} hasQueryFeature={hasQueryFeature}/>)}
        {this.renderEntries()}
        {hasContext && <EventContexts group={group} event={event}/>}
        {event && !objectIsEmpty(event.context) && <EventExtraData event={event}/>}
        {event && !objectIsEmpty(event.packages) && <EventPackageData event={event}/>}
        {event && !objectIsEmpty(event.device) && <EventDevice event={event}/>}
        {!isShare && features.has('event-attachments') && (<EventAttachments event={event} orgId={organization.slug} projectId={project.slug} location={location}/>)}
        {(event === null || event === void 0 ? void 0 : event.sdk) && !objectIsEmpty(event.sdk) && <EventSdk sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<EventSdkUpdates event={__assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && (event === null || event === void 0 ? void 0 : event.groupID) && (<EventGroupingInfo projectId={project.slug} event={event} showGroupingConfig={features.has('set-grouping-config')}/>)}
        {!isShare && features.has('event-attachments') && (<RRWebIntegration event={event} orgId={organization.slug} projectId={project.slug}/>)}
      </div>);
    };
    EventEntries.propTypes = {
        // Custom shape because shared view doesn't get id.
        organization: PropTypes.shape({
            id: PropTypes.string,
            slug: PropTypes.string.isRequired,
            features: PropTypes.arrayOf(PropTypes.string),
        }).isRequired,
        event: SentryTypes.Event.isRequired,
        group: SentryTypes.Group,
        project: PropTypes.object.isRequired,
        // TODO(dcramer): ideally isShare would be replaced with simple permission
        // checks
        isShare: PropTypes.bool,
        showExampleCommit: PropTypes.bool,
        showTagSummary: PropTypes.bool,
    };
    EventEntries.defaultProps = defaultProps;
    return EventEntries;
}(React.Component));
var ErrorContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"], ["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"])));
var BorderlessEventEntries = styled(EventEntries)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & ", " {\n    padding: ", " 0 0 0;\n  }\n  & ", ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & ", " {\n    margin-bottom: ", ";\n  }\n"], ["\n  & " /* sc-selector */, " {\n    padding: ", " 0 0 0;\n  }\n  & " /* sc-selector */, ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & " /* sc-selector */, " {\n    margin-bottom: ", ";\n  }\n"])), /* sc-selector */ DataSection, space(3), /* sc-selector */ DataSection, /* sc-selector */ ErrorContainer, space(2));
var StyledEventUserFeedback = styled(EventUserFeedback)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"], ["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"])), function (p) { return (p.includeBorder ? "border-top: 1px solid " + p.theme.innerBorder + ";" : ''); });
// TODO(ts): any required due to our use of SharedViewOrganization
export default withOrganization(EventEntries);
export { BorderlessEventEntries };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventEntries.jsx.map