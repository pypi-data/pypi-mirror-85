import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { analytics } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
var DEFAULT_POLL_INTERVAL = 5000;
var recordAnalyticsFirstEvent = function (_a) {
    var key = _a.key, organization = _a.organization, project = _a.project;
    return analytics("onboarding_v2." + key, {
        org_id: parseInt(organization.id, 10),
        project: parseInt(project.id, 10),
    });
};
/**
 * This is a render prop component that can be used to wait for the first event
 * of a project to be received via polling.
 */
var EventWaiter = /** @class */ (function (_super) {
    __extends(EventWaiter, _super);
    function EventWaiter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            firstIssue: null,
        };
        _this.intervalId = null;
        _this.pollHandler = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, project, eventType, onIssueReceived, firstEvent, firstIssue, resp, resp_1, issues;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, eventType = _a.eventType, onIssueReceived = _a.onIssueReceived;
                        firstEvent = null;
                        firstIssue = null;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/")];
                    case 2:
                        resp = _c.sent();
                        firstEvent = eventType === 'error' ? resp.firstEvent : resp.firstTransactionEvent;
                        return [3 /*break*/, 4];
                    case 3:
                        resp_1 = _c.sent();
                        if (!resp_1) {
                            return [2 /*return*/];
                        }
                        // This means org or project does not exist, we need to stop polling
                        // Also stop polling on auth-related errors (403/401)
                        if ([404, 403, 401, 0].includes(resp_1.status)) {
                            // TODO: Add some UX around this... redirect? error message?
                            this.stopPolling();
                            return [2 /*return*/];
                        }
                        Sentry.setExtras({
                            status: resp_1.status,
                            detail: (_b = resp_1.responseJSON) === null || _b === void 0 ? void 0 : _b.detail,
                        });
                        Sentry.captureException(new Error("Error polling for first " + eventType + " event"));
                        return [3 /*break*/, 4];
                    case 4:
                        if (firstEvent === null || firstEvent === false) {
                            return [2 /*return*/];
                        }
                        if (!(eventType === 'error')) return [3 /*break*/, 6];
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/issues/")];
                    case 5:
                        issues = _c.sent();
                        // The event may have expired, default to true
                        firstIssue = issues.find(function (issue) { return issue.firstSeen === firstEvent; }) || true;
                        // noinspection SpellCheckingInspection
                        recordAnalyticsFirstEvent({
                            key: 'first_event_recieved',
                            organization: organization,
                            project: project,
                        });
                        return [3 /*break*/, 7];
                    case 6:
                        firstIssue = firstEvent;
                        // noinspection SpellCheckingInspection
                        recordAnalyticsFirstEvent({
                            key: 'first_transaction_recieved',
                            organization: organization,
                            project: project,
                        });
                        _c.label = 7;
                    case 7:
                        if (onIssueReceived) {
                            onIssueReceived({ firstIssue: firstIssue });
                        }
                        this.stopPolling();
                        this.setState({ firstIssue: firstIssue });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    EventWaiter.prototype.componentDidMount = function () {
        this.pollHandler();
        this.startPolling();
    };
    EventWaiter.prototype.componentDidUpdate = function () {
        this.stopPolling();
        this.startPolling();
    };
    EventWaiter.prototype.componentWillUnmount = function () {
        this.stopPolling();
    };
    EventWaiter.prototype.startPolling = function () {
        var _a = this.props, disabled = _a.disabled, organization = _a.organization, project = _a.project;
        if (disabled || !organization || !project || this.state.firstIssue) {
            return;
        }
        this.intervalId = window.setInterval(this.pollHandler, this.props.pollInterval || DEFAULT_POLL_INTERVAL);
    };
    EventWaiter.prototype.stopPolling = function () {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    };
    EventWaiter.prototype.render = function () {
        return this.props.children({ firstIssue: this.state.firstIssue });
    };
    return EventWaiter;
}(React.Component));
export default withApi(EventWaiter);
//# sourceMappingURL=eventWaiter.jsx.map