import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import AsyncView from 'app/views/asyncView';
import Badge from 'app/components/badge';
import { IconMail } from 'app/icons';
import ListLink from 'app/components/links/listLink';
import AlertLink from 'app/components/alertLink';
import NavTabs from 'app/components/navTabs';
import routeTitleGen from 'app/utils/routeTitle';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withOrganization from 'app/utils/withOrganization';
var OrganizationMembersWrapper = /** @class */ (function (_super) {
    __extends(OrganizationMembersWrapper, _super);
    function OrganizationMembersWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeAccessRequest = function (id) {
            return _this.setState(function (state) { return ({
                requestList: state.requestList.filter(function (request) { return request.id !== id; }),
            }); });
        };
        _this.removeInviteRequest = function (id) {
            return _this.setState(function (state) { return ({
                inviteRequests: state.inviteRequests.filter(function (request) { return request.id !== id; }),
            }); });
        };
        _this.updateInviteRequest = function (id, data) {
            return _this.setState(function (state) {
                var inviteRequests = __spread(state.inviteRequests);
                var inviteIndex = inviteRequests.findIndex(function (request) { return request.id === id; });
                inviteRequests[inviteIndex] = __assign(__assign({}, inviteRequests[inviteIndex]), data);
                return { inviteRequests: inviteRequests };
            });
        };
        return _this;
    }
    OrganizationMembersWrapper.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['inviteRequests', "/organizations/" + orgId + "/invite-requests/"],
            ['requestList', "/organizations/" + orgId + "/access-requests/"],
        ];
    };
    OrganizationMembersWrapper.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitleGen(t('Members'), orgId, false);
    };
    Object.defineProperty(OrganizationMembersWrapper.prototype, "onRequestsTab", {
        get: function () {
            return location.pathname.includes('/requests/');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "hasWriteAccess", {
        get: function () {
            var organization = this.props.organization;
            if (!organization || !organization.access) {
                return false;
            }
            return organization.access.includes('member:write');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "showInviteRequests", {
        get: function () {
            return this.hasWriteAccess;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "showNavTabs", {
        get: function () {
            var requestList = this.state.requestList;
            // show the requests tab if there are pending team requests,
            // or if the user has access to approve or deny invite requests
            return (requestList && requestList.length > 0) || this.showInviteRequests;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "requestCount", {
        get: function () {
            var _a = this.state, requestList = _a.requestList, inviteRequests = _a.inviteRequests;
            var count = requestList.length;
            // if the user can't see the invite requests panel,
            // exclude those requests from the total count
            if (this.showInviteRequests) {
                count += inviteRequests.length;
            }
            return count ? count.toString() : null;
        },
        enumerable: false,
        configurable: true
    });
    OrganizationMembersWrapper.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, children = _a.children, organization = _a.organization, orgId = _a.params.orgId;
        var _b = this.state, requestList = _b.requestList, inviteRequests = _b.inviteRequests;
        return (<React.Fragment>
        <SettingsPageHeader title="Members"/>

        <AlertLink data-test-id="email-invite" icon={<IconMail />} priority="info" onClick={function () { return openInviteMembersModal({ source: 'members_settings' }); }}>
          {t('Invite new members by email to join your organization')}
        </AlertLink>

        {this.showNavTabs && (<NavTabs underlined>
            <ListLink to={"/settings/" + orgId + "/members/"} isActive={function () { return !_this.onRequestsTab; }} data-test-id="members-tab">
              {t('Members')}
            </ListLink>
            <ListLink to={"/settings/" + orgId + "/members/requests/"} isActive={function () { return _this.onRequestsTab; }} data-test-id="requests-tab" onClick={function () {
            _this.showInviteRequests &&
                trackAnalyticsEvent({
                    eventKey: 'invite_request.tab_clicked',
                    eventName: 'Invite Request Tab Clicked',
                    organization_id: organization.id,
                });
        }}>
              {t('Requests')}
            </ListLink>
            {this.requestCount && <StyledBadge text={this.requestCount}/>}
          </NavTabs>)}

        {children &&
            React.cloneElement(children, {
                requestList: requestList,
                inviteRequests: inviteRequests,
                onRemoveInviteRequest: this.removeInviteRequest,
                onUpdateInviteRequest: this.updateInviteRequest,
                onRemoveAccessRequest: this.removeAccessRequest,
                showInviteRequests: this.showInviteRequests,
            })}
      </React.Fragment>);
    };
    return OrganizationMembersWrapper;
}(AsyncView));
var StyledBadge = styled(Badge)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: -12px;\n\n  @media (max-width: ", ") {\n    margin-left: -6px;\n  }\n"], ["\n  margin-left: -12px;\n\n  @media (max-width: ", ") {\n    margin-left: -6px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default withOrganization(OrganizationMembersWrapper);
var templateObject_1;
//# sourceMappingURL=organizationMembersWrapper.jsx.map