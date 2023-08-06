import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import React from 'react';
import * as Sentry from '@sentry/react';
import styled from '@emotion/styled';
import { metric } from 'app/utils/analytics';
import { fetchSentryAppComponents } from 'app/actionCreators/sentryAppComponents';
import { withMeta } from 'app/components/events/meta/metaProxy';
import EventEntries from 'app/components/events/eventEntries';
import GroupEventDetailsLoadingError from 'app/components/errors/groupEventDetailsLoadingError';
import GroupSidebar from 'app/components/group/sidebar';
import LoadingIndicator from 'app/components/loadingIndicator';
import MutedBox from 'app/components/mutedBox';
import ResolutionBox from 'app/components/resolutionBox';
import SentryTypes from 'app/sentryTypes';
import fetchSentryAppInstallations from 'app/utils/fetchSentryAppInstallations';
import { fetchGroupEventAndMarkSeen, getEventEnvironment } from '../utils';
import GroupEventToolbar from '../eventToolbar';
var GroupEventDetails = /** @class */ (function (_super) {
    __extends(GroupEventDetails, _super);
    function GroupEventDetails(props) {
        var _this = _super.call(this, props) || this;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, group, project, organization, params, environments, eventId, groupId, orgSlug, projSlug, projectId, envNames, releasesCompletionPromise, fetchGroupEventPromise, releasesCompletion, event_1, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group, project = _a.project, organization = _a.organization, params = _a.params, environments = _a.environments;
                        eventId = params.eventId || 'latest';
                        groupId = group.id;
                        orgSlug = organization.slug;
                        projSlug = project.slug;
                        projectId = project.id;
                        this.setState({
                            loading: true,
                            error: false,
                        });
                        envNames = environments.map(function (e) { return e.name; });
                        releasesCompletionPromise = api.requestPromise("/projects/" + orgSlug + "/" + projSlug + "/releases/completion/");
                        fetchGroupEventPromise = fetchGroupEventAndMarkSeen(api, orgSlug, projSlug, groupId, eventId, envNames);
                        fetchSentryAppInstallations(api, orgSlug);
                        fetchSentryAppComponents(api, orgSlug, projectId);
                        return [4 /*yield*/, releasesCompletionPromise];
                    case 1:
                        releasesCompletion = _b.sent();
                        this.setState({
                            releasesCompletion: releasesCompletion,
                        });
                        _b.label = 2;
                    case 2:
                        _b.trys.push([2, 4, , 5]);
                        return [4 /*yield*/, fetchGroupEventPromise];
                    case 3:
                        event_1 = _b.sent();
                        this.setState({
                            event: event_1,
                            error: false,
                            loading: false,
                        });
                        return [3 /*break*/, 5];
                    case 4:
                        err_1 = _b.sent();
                        // This is an expected error, capture to Sentry so that it is not considered as an unhandled error
                        Sentry.captureException(err_1);
                        this.setState({
                            event: null,
                            error: true,
                            loading: false,
                        });
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        _this.state = {
            loading: true,
            error: false,
            event: null,
            eventNavLinks: '',
            releasesCompletion: null,
        };
        return _this;
    }
    GroupEventDetails.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupEventDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, environments = _a.environments, params = _a.params, location = _a.location;
        var eventHasChanged = prevProps.params.eventId !== params.eventId;
        var environmentsHaveChanged = !isEqual(prevProps.environments, environments);
        // If environments are being actively changed and will no longer contain the
        // current event's environment, redirect to latest
        if (environmentsHaveChanged &&
            prevState.event &&
            params.eventId &&
            !['latest', 'oldest'].includes(params.eventId)) {
            var shouldRedirect = environments.length > 0 &&
                !environments.find(function (env) { return env.name === getEventEnvironment(prevState.event); });
            if (shouldRedirect) {
                browserHistory.replace({
                    pathname: "/organizations/" + params.orgId + "/issues/" + params.groupId + "/",
                    query: location.query,
                });
                return;
            }
        }
        if (eventHasChanged || environmentsHaveChanged) {
            this.fetchData();
        }
        // First Meaningful Paint for /organizations/:orgId/issues/:groupId/
        if (prevState.loading && !this.state.loading && prevState.event === null) {
            metric.measure({
                name: 'app.page.perf.issue-details',
                start: 'page-issue-details-start',
                data: {
                    // start_type is set on 'page-issue-details-start'
                    org_id: parseInt(this.props.organization.id, 10),
                    group: this.props.organization.features.includes('enterprise-perf')
                        ? 'enterprise-perf'
                        : 'control',
                    milestone: 'first-meaningful-paint',
                    is_enterprise: this.props.organization.features
                        .includes('enterprise-orgs')
                        .toString(),
                    is_outlier: this.props.organization.features
                        .includes('enterprise-orgs-outliers')
                        .toString(),
                },
            });
        }
    };
    GroupEventDetails.prototype.componentWillUnmount = function () {
        var api = this.props.api;
        api.clear();
    };
    Object.defineProperty(GroupEventDetails.prototype, "showExampleCommit", {
        get: function () {
            var project = this.props.project;
            var releasesCompletion = this.state.releasesCompletion;
            return ((project === null || project === void 0 ? void 0 : project.isMember) && (project === null || project === void 0 ? void 0 : project.firstEvent) && (releasesCompletion === null || releasesCompletion === void 0 ? void 0 : releasesCompletion.some(function (_a) {
                var step = _a.step, complete = _a.complete;
                return step === 'commit' && !complete;
            })));
        },
        enumerable: false,
        configurable: true
    });
    GroupEventDetails.prototype.render = function () {
        var _a = this.props, className = _a.className, group = _a.group, project = _a.project, organization = _a.organization, environments = _a.environments, location = _a.location;
        var evt = withMeta(this.state.event);
        return (<div className={className}>
        <div className="event-details-container">
          <div className="primary">
            {evt && (<GroupEventToolbar organization={organization} group={group} event={evt} orgId={organization.slug} projectId={project.slug} location={location}/>)}
            {group.status === 'ignored' && (<MutedBox statusDetails={group.statusDetails}/>)}
            {group.status === 'resolved' && (<ResolutionBox statusDetails={group.statusDetails} projectId={project.id}/>)}
            {this.state.loading ? (<LoadingIndicator />) : this.state.error ? (<GroupEventDetailsLoadingError environments={environments} onRetry={this.fetchData}/>) : (<EventEntries group={group} event={evt} organization={organization} project={project} location={location} showExampleCommit={this.showExampleCommit}/>)}
          </div>
          <div className="secondary">
            <GroupSidebar organization={organization} project={project} group={group} event={evt} environments={environments}/>
          </div>
        </div>
      </div>);
    };
    GroupEventDetails.propTypes = {
        api: PropTypes.object.isRequired,
        group: SentryTypes.Group.isRequired,
        project: SentryTypes.Project.isRequired,
        organization: SentryTypes.Organization.isRequired,
        environments: PropTypes.arrayOf(SentryTypes.Environment).isRequired,
    };
    return GroupEventDetails;
}(React.Component));
export default styled(GroupEventDetails)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
var templateObject_1;
//# sourceMappingURL=groupEventDetails.jsx.map