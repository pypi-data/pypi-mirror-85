import { __assign, __awaiter, __extends, __generator } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { MEMBER_ROLES } from 'app/constants';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t, tct } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import withOrganization from 'app/utils/withOrganization';
import withTeams from 'app/utils/withTeams';
import AsyncView from 'app/views/asyncView';
import InviteRequestRow from './inviteRequestRow';
import OrganizationAccessRequests from './organizationAccessRequests';
var OrganizationRequestsView = /** @class */ (function (_super) {
    __extends(OrganizationRequestsView, _super);
    function OrganizationRequestsView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAction = function (_a) {
            var inviteRequest = _a.inviteRequest, method = _a.method, data = _a.data, successMessage = _a.successMessage, errorMessage = _a.errorMessage, eventKey = _a.eventKey, eventName = _a.eventName;
            return __awaiter(_this, void 0, void 0, function () {
                var _b, params, organization, onRemoveInviteRequest, _c;
                return __generator(this, function (_d) {
                    switch (_d.label) {
                        case 0:
                            _b = this.props, params = _b.params, organization = _b.organization, onRemoveInviteRequest = _b.onRemoveInviteRequest;
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: __assign(__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = true, _a)),
                                });
                            });
                            _d.label = 1;
                        case 1:
                            _d.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.api.requestPromise("/organizations/" + params.orgId + "/invite-requests/" + inviteRequest.id + "/", {
                                    method: method,
                                    data: data,
                                })];
                        case 2:
                            _d.sent();
                            onRemoveInviteRequest(inviteRequest.id);
                            addSuccessMessage(successMessage);
                            trackAnalyticsEvent({
                                eventKey: eventKey,
                                eventName: eventName,
                                organization_id: organization.id,
                                member_id: parseInt(inviteRequest.id, 10),
                                invite_status: inviteRequest.inviteStatus,
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            _c = _d.sent();
                            addErrorMessage(errorMessage);
                            return [3 /*break*/, 4];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: __assign(__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = false, _a)),
                                });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleApprove = function (inviteRequest) {
            _this.handleAction({
                inviteRequest: inviteRequest,
                method: 'PUT',
                data: {
                    role: inviteRequest.role,
                    teams: inviteRequest.teams,
                    approve: 1,
                },
                successMessage: tct('[email] has been invited', { email: inviteRequest.email }),
                errorMessage: tct('Error inviting [email]', { email: inviteRequest.email }),
                eventKey: 'invite_request.approved',
                eventName: 'Invite Request Approved',
            });
        };
        _this.handleDeny = function (inviteRequest) {
            _this.handleAction({
                inviteRequest: inviteRequest,
                method: 'DELETE',
                data: {},
                successMessage: tct('Invite request for [email] denied', {
                    email: inviteRequest.email,
                }),
                errorMessage: tct('Error denying invite request for [email]', {
                    email: inviteRequest.email,
                }),
                eventKey: 'invite_request.denied',
                eventName: 'Invite Request Denied',
            });
        };
        return _this;
    }
    OrganizationRequestsView.prototype.getDefaultState = function () {
        var state = _super.prototype.getDefaultState.call(this);
        return __assign(__assign({}, state), { inviteRequestBusy: {} });
    };
    OrganizationRequestsView.prototype.UNSAFE_componentWillMount = function () {
        _super.prototype.UNSAFE_componentWillMount.call(this);
        this.handleRedirect();
    };
    OrganizationRequestsView.prototype.componentDidUpdate = function () {
        this.handleRedirect();
    };
    OrganizationRequestsView.prototype.getEndpoints = function () {
        var orgId = this.props.organization.slug;
        return [['member', "/organizations/" + orgId + "/members/me/"]];
    };
    OrganizationRequestsView.prototype.handleRedirect = function () {
        var _a = this.props, router = _a.router, params = _a.params, requestList = _a.requestList, showInviteRequests = _a.showInviteRequests;
        // redirect to the members view if the user cannot see
        // the invite requests panel and all of the team requests
        // have been approved or denied
        if (showInviteRequests || requestList.length) {
            return null;
        }
        return router.push("/settings/" + params.orgId + "/members/");
    };
    OrganizationRequestsView.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, requestList = _a.requestList, showInviteRequests = _a.showInviteRequests, inviteRequests = _a.inviteRequests, onRemoveAccessRequest = _a.onRemoveAccessRequest, onUpdateInviteRequest = _a.onUpdateInviteRequest, organization = _a.organization, teams = _a.teams;
        var _b = this.state, inviteRequestBusy = _b.inviteRequestBusy, member = _b.member;
        return (<React.Fragment>
        {showInviteRequests && (<Panel>
            <PanelHeader>{t('Pending Invite Requests')}</PanelHeader>
            <PanelBody>
              {inviteRequests.map(function (inviteRequest) { return (<InviteRequestRow key={inviteRequest.id} organization={organization} inviteRequest={inviteRequest} inviteRequestBusy={inviteRequestBusy} allTeams={teams} allRoles={member ? member.roles : MEMBER_ROLES} onApprove={_this.handleApprove} onDeny={_this.handleDeny} onUpdate={function (data) { return onUpdateInviteRequest(inviteRequest.id, data); }}/>); })}
              {inviteRequests.length === 0 && (<EmptyMessage>{t('No requests found.')}</EmptyMessage>)}
            </PanelBody>
          </Panel>)}

        <OrganizationAccessRequests orgId={params.orgId} requestList={requestList} onRemoveAccessRequest={onRemoveAccessRequest}/>
      </React.Fragment>);
    };
    OrganizationRequestsView.propTypes = {
        requestList: PropTypes.array.isRequired,
        inviteRequests: PropTypes.array.isRequired,
        onRemoveInviteRequest: PropTypes.func.isRequired,
        onRemoveAccessRequest: PropTypes.func.isRequired,
        showInviteRequests: PropTypes.bool.isRequired,
    };
    OrganizationRequestsView.defaultProps = {
        inviteRequests: [],
    };
    return OrganizationRequestsView;
}(AsyncView));
export default withTeams(withOrganization(OrganizationRequestsView));
//# sourceMappingURL=organizationRequestsView.jsx.map