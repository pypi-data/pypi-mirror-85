import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { IconSliders } from 'app/icons';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ConfigStore from 'app/stores/configStore';
import Pagination from 'app/components/pagination';
import routeTitleGen from 'app/utils/routeTitle';
import SentryTypes from 'app/sentryTypes';
import { redirectToRemainingOrganization } from 'app/actionCreators/organizations';
import { resendMemberInvite } from 'app/actionCreators/members';
import withOrganization from 'app/utils/withOrganization';
import Button from 'app/components/button';
import DropdownMenu from 'app/components/dropdownMenu';
import space from 'app/styles/space';
import { MEMBER_ROLES } from 'app/constants';
import theme from 'app/utils/theme';
import OrganizationMemberRow from './organizationMemberRow';
import MembersFilter from './components/membersFilter';
var OrganizationMembersList = /** @class */ (function (_super) {
    __extends(OrganizationMembersList, _super);
    function OrganizationMembersList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeMember = function (id) { return __awaiter(_this, void 0, void 0, function () {
            var orgId;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        orgId = this.props.params.orgId;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + orgId + "/members/" + id + "/", {
                                method: 'DELETE',
                                data: {},
                            })];
                    case 1:
                        _a.sent();
                        this.setState(function (state) { return ({
                            members: state.members.filter(function (_a) {
                                var existingId = _a.id;
                                return existingId !== id;
                            }),
                        }); });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleRemove = function (_a) {
            var id = _a.id, name = _a.name;
            return __awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            addErrorMessage(tct('Error removing [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            addSuccessMessage(tct('Removed [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleLeave = function (_a) {
            var id = _a.id;
            return __awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            addErrorMessage(tct('Error leaving [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            redirectToRemainingOrganization({ orgId: orgName, removeOrg: true });
                            addSuccessMessage(tct('You left [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleSendInvite = function (_a) {
            var id = _a.id, expired = _a.expired;
            return __awaiter(_this, void 0, void 0, function () {
                var _b;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    invited: __assign(__assign({}, state.invited), (_a = {}, _a[id] = 'loading', _a)),
                                });
                            });
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, resendMemberInvite(this.api, {
                                    orgId: this.props.params.orgId,
                                    memberId: id,
                                    regenerate: expired,
                                })];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: __assign(__assign({}, state.invited), (_a = {}, _a[id] = null, _a)) });
                            });
                            addErrorMessage(t('Error sending invite'));
                            return [2 /*return*/];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: __assign(__assign({}, state.invited), (_a = {}, _a[id] = 'success', _a)) });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    OrganizationMembersList.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { members: [], invited: {} });
    };
    OrganizationMembersList.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['members', "/organizations/" + orgId + "/members/", {}, { paginate: true }],
            [
                'member',
                "/organizations/" + orgId + "/members/me/",
                {},
                { allowError: function (error) { return error.status === 404; } },
            ],
            [
                'authProvider',
                "/organizations/" + orgId + "/auth-provider/",
                {},
                { allowError: function (error) { return error.status === 403; } },
            ],
        ];
    };
    OrganizationMembersList.prototype.getTitle = function () {
        var orgId = this.props.organization.slug;
        return routeTitleGen(t('Members'), orgId, false);
    };
    OrganizationMembersList.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, params = _a.params, organization = _a.organization, routes = _a.routes;
        var _b = this.state, membersPageLinks = _b.membersPageLinks, members = _b.members, currentMember = _b.member;
        var orgName = organization.name, access = organization.access;
        var canAddMembers = access.includes('member:write');
        var canRemove = access.includes('member:admin');
        var currentUser = ConfigStore.get('user');
        // Find out if current user is the only owner
        var isOnlyOwner = !members.find(function (_a) {
            var role = _a.role, email = _a.email, pending = _a.pending;
            return role === 'owner' && email !== currentUser.email && !pending;
        });
        // Only admins/owners can remove members
        var requireLink = !!this.state.authProvider && this.state.authProvider.require_link;
        // eslint-disable-next-line react/prop-types
        var renderSearch = function (_a) {
            var defaultSearchBar = _a.defaultSearchBar, value = _a.value, handleChange = _a.handleChange;
            return (<SearchWrapper>
        {defaultSearchBar}
        <DropdownMenu closeOnEscape>
          {function (_a) {
                var _b;
                var getActorProps = _a.getActorProps, isOpen = _a.isOpen;
                return (<FilterWrapper>
              <Button size="small" icon={<IconSliders size="xs"/>} {...getActorProps({})}>
                {t('Search Filters')}
              </Button>
              {isOpen && (<StyledMembersFilter roles={(_b = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _b !== void 0 ? _b : MEMBER_ROLES} query={value} onChange={function (query) { return handleChange(query); }}/>)}
            </FilterWrapper>);
            }}
        </DropdownMenu>
      </SearchWrapper>);
        };
        return (<React.Fragment>
        <ClassNames>
          {function (_a) {
            var css = _a.css;
            return _this.renderSearchInput({
                updateRoute: true,
                placeholder: t('Search Members'),
                children: renderSearch,
                className: css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                font-size: ", ";\n                padding: ", ";\n              "], ["\n                font-size: ", ";\n                padding: ", ";\n              "])), theme.fontSizeMedium, space(0.75)),
            });
        }}
        </ClassNames>
        <Panel data-test-id="org-member-list">
          <PanelHeader>{t('Members')}</PanelHeader>

          <PanelBody>
            {members.map(function (member) { return (<OrganizationMemberRow routes={routes} params={params} key={member.id} member={member} status={_this.state.invited[member.id]} orgId={params.orgId} orgName={orgName} memberCanLeave={!isOnlyOwner} currentUser={currentUser} canRemoveMembers={canRemove} canAddMembers={canAddMembers} requireLink={requireLink} onSendInvite={_this.handleSendInvite} onRemove={_this.handleRemove} onLeave={_this.handleLeave}/>); })}
            {members.length === 0 && (<EmptyMessage>{t('No members found.')}</EmptyMessage>)}
          </PanelBody>
        </Panel>

        <Pagination pageLinks={membersPageLinks}/>
      </React.Fragment>);
    };
    OrganizationMembersList.propTypes = {
        organization: SentryTypes.Organization,
    };
    return OrganizationMembersList;
}(AsyncView));
var SearchWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"])), space(1.5), space(3));
var FilterWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledMembersFilter = styled(MembersFilter)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"], ["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
export default withOrganization(OrganizationMembersList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=organizationMembersList.jsx.map