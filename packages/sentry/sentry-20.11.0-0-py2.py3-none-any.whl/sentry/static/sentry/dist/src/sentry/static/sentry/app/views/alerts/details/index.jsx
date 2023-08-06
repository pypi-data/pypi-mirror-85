import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { fetchOrgMembers } from 'app/actionCreators/members';
import { markIncidentAsSeen } from 'app/actionCreators/incident';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import { IncidentStatus } from '../types';
import { fetchIncident, fetchIncidentStats, updateSubscription, updateStatus, isOpen, } from '../utils';
import DetailsBody from './body';
import DetailsHeader from './header';
var IncidentDetails = /** @class */ (function (_super) {
    __extends(IncidentDetails, _super);
    function IncidentDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, alertId, incidentPromise, statsPromise, _err_1;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        this.setState({ isLoading: true, hasError: false });
                        _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        incidentPromise = fetchIncident(api, orgId, alertId).then(function (incident) {
                            _this.setState({ incident: incident });
                            markIncidentAsSeen(api, orgId, incident);
                        });
                        statsPromise = fetchIncidentStats(api, orgId, alertId).then(function (stats) {
                            return _this.setState({ stats: stats });
                        });
                        // State not set after promise.all because stats *usually* takes
                        // more time than the incident api
                        return [4 /*yield*/, Promise.all([incidentPromise, statsPromise])];
                    case 2:
                        // State not set after promise.all because stats *usually* takes
                        // more time than the incident api
                        _c.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _c.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubscriptionChange = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, alertId, isSubscribed, newIsSubscribed;
            return __generator(this, function (_c) {
                _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                if (!this.state.incident) {
                    return [2 /*return*/];
                }
                isSubscribed = this.state.incident.isSubscribed;
                newIsSubscribed = !isSubscribed;
                this.setState(function (state) { return ({
                    incident: __assign(__assign({}, state.incident), { isSubscribed: newIsSubscribed }),
                }); });
                try {
                    updateSubscription(api, orgId, alertId, newIsSubscribed);
                }
                catch (_err) {
                    this.setState(function (state) { return ({
                        incident: __assign(__assign({}, state.incident), { isSubscribed: isSubscribed }),
                    }); });
                    addErrorMessage(t('An error occurred, your subscription status was not changed.'));
                }
                return [2 /*return*/];
            });
        }); };
        _this.handleStatusChange = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, alertId, status, newStatus, incident, _err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                        if (!this.state.incident) {
                            return [2 /*return*/];
                        }
                        status = this.state.incident.status;
                        newStatus = isOpen(this.state.incident) ? IncidentStatus.CLOSED : status;
                        this.setState(function (state) { return ({
                            incident: __assign(__assign({}, state.incident), { status: newStatus }),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, updateStatus(api, orgId, alertId, newStatus)];
                    case 2:
                        incident = _c.sent();
                        // Update entire incident object because updating status can cause other parts
                        // of the model to change (e.g close date)
                        this.setState({ incident: incident });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _c.sent();
                        this.setState(function (state) { return ({
                            incident: __assign(__assign({}, state.incident), { status: status }),
                        }); });
                        addErrorMessage(t('An error occurred, your incident status was not changed.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    IncidentDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, params = _a.params;
        trackAnalyticsEvent({
            eventKey: 'alert_details.viewed',
            eventName: 'Alert Details: Viewed',
            organization_id: parseInt(organization.id, 10),
            alert_id: parseInt(params.alertId, 10),
        });
        fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    IncidentDetails.prototype.render = function () {
        var _a = this.state, incident = _a.incident, stats = _a.stats, hasError = _a.hasError;
        var params = this.props.params;
        return (<React.Fragment>
        <DetailsHeader hasIncidentDetailsError={hasError} params={params} incident={incident} stats={stats} onSubscriptionChange={this.handleSubscriptionChange} onStatusChange={this.handleStatusChange}/>

        <DetailsBody {...this.props} incident={incident} stats={stats}/>
      </React.Fragment>);
    };
    return IncidentDetails;
}(React.Component));
export default withApi(IncidentDetails);
//# sourceMappingURL=index.jsx.map