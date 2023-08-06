import { __awaiter, __extends, __generator, __rest } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import * as Sentry from '@sentry/react';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import { trackAdhocEvent, trackAnalyticsEvent } from 'app/utils/analytics';
import Button from 'app/components/button';
import SentryTypes from 'app/sentryTypes';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var EVENT_POLL_RETRIES = 6;
var EVENT_POLL_INTERVAL = 800;
function latestEventAvailable(api, groupID) {
    return __awaiter(this, void 0, void 0, function () {
        var retries, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    retries = 0;
                    _b.label = 1;
                case 1:
                    if (!true) return [3 /*break*/, 7];
                    if (retries > EVENT_POLL_RETRIES) {
                        return [2 /*return*/, { eventCreated: false, retries: retries - 1 }];
                    }
                    return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve, EVENT_POLL_INTERVAL); })];
                case 2:
                    _b.sent();
                    _b.label = 3;
                case 3:
                    _b.trys.push([3, 5, , 6]);
                    return [4 /*yield*/, api.requestPromise("/issues/" + groupID + "/events/latest/")];
                case 4:
                    _b.sent();
                    return [2 /*return*/, { eventCreated: true, retries: retries }];
                case 5:
                    _a = _b.sent();
                    ++retries;
                    return [3 /*break*/, 6];
                case 6: return [3 /*break*/, 1];
                case 7: return [2 /*return*/];
            }
        });
    });
}
var CreateSampleEventButton = /** @class */ (function (_super) {
    __extends(CreateSampleEventButton, _super);
    function CreateSampleEventButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            creating: false,
        };
        _this.createSampleGroup = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, project, eventData, url, error_1, t0, _b, eventCreated, retries, t1, duration;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project;
                        if (!project) {
                            return [2 /*return*/];
                        }
                        addLoadingMessage(t('Processing sample event...'));
                        this.setState({ creating: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        url = "/projects/" + organization.slug + "/" + project.slug + "/create-sample/";
                        return [4 /*yield*/, api.requestPromise(url, { method: 'POST' })];
                    case 2:
                        eventData = _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _c.sent();
                        Sentry.withScope(function (scope) {
                            scope.setExtra('error', error_1);
                            Sentry.captureException(new Error('Failed to create sample event'));
                        });
                        this.setState({ creating: false });
                        addErrorMessage(t('Failed to create a new sample event'));
                        return [2 /*return*/];
                    case 4:
                        t0 = performance.now();
                        return [4 /*yield*/, latestEventAvailable(api, eventData.groupID)];
                    case 5:
                        _b = _c.sent(), eventCreated = _b.eventCreated, retries = _b.retries;
                        t1 = performance.now();
                        clearIndicators();
                        this.setState({ creating: false });
                        duration = Math.ceil(t1 - t0);
                        this.recordAnalytics({ eventCreated: eventCreated, retries: retries, duration: duration });
                        if (!eventCreated) {
                            addErrorMessage(t('Failed to load sample event'));
                            Sentry.withScope(function (scope) {
                                scope.setTag('groupID', eventData.groupID);
                                scope.setTag('platform', project.platform || '');
                                scope.setTag('interval', EVENT_POLL_INTERVAL.toString());
                                scope.setTag('retries', retries.toString());
                                scope.setTag('duration', duration.toString());
                                scope.setLevel(Sentry.Severity.Warning);
                                Sentry.captureMessage('Failed to load sample event');
                            });
                            return [2 /*return*/];
                        }
                        browserHistory.push("/organizations/" + organization.slug + "/issues/" + eventData.groupID + "/");
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CreateSampleEventButton.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, source = _a.source;
        if (!project) {
            return;
        }
        trackAdhocEvent({
            eventKey: 'sample_event.button_viewed',
            org_id: organization.id,
            project_id: project.id,
            source: source,
        });
    };
    CreateSampleEventButton.prototype.recordAnalytics = function (_a) {
        var eventCreated = _a.eventCreated, retries = _a.retries, duration = _a.duration;
        var _b = this.props, organization = _b.organization, project = _b.project, source = _b.source;
        if (!project) {
            return;
        }
        var eventKey = "sample_event." + (eventCreated ? 'created' : 'failed');
        var eventName = "Sample Event " + (eventCreated ? 'Created' : 'Failed');
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: organization.id,
            project_id: project.id,
            platform: project.platform || '',
            interval: EVENT_POLL_INTERVAL,
            retries: retries,
            duration: duration,
            source: source,
        });
    };
    CreateSampleEventButton.prototype.render = function () {
        var _a = this.props, _api = _a.api, _organization = _a.organization, _project = _a.project, _source = _a.source, props = __rest(_a, ["api", "organization", "project", "source"]);
        var creating = this.state.creating;
        return (<Button {...props} data-test-id="create-sample-event" disabled={props.disabled || creating} onClick={this.createSampleGroup}/>);
    };
    CreateSampleEventButton.propTypes = {
        api: PropTypes.object,
        organization: SentryTypes.Organization.isRequired,
        project: SentryTypes.Project,
        source: PropTypes.string.isRequired,
        disabled: PropTypes.bool,
    };
    return CreateSampleEventButton;
}(React.Component));
export default withApi(withOrganization(CreateSampleEventButton));
//# sourceMappingURL=createSampleEventButton.jsx.map