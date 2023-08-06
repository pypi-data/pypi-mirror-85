import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import debounce from 'lodash/debounce';
import styled from '@emotion/styled';
import { Panel, PanelItem, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { joinTeam, leaveTeam } from 'app/actionCreators/teams';
import { openInviteMembersModal, openTeamAccessRequestModal, } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import UserAvatar from 'app/components/avatar/userAvatar';
import Button from 'app/components/button';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import IdBadge from 'app/components/idBadge';
import { IconSubtract, IconUser } from 'app/icons';
import Link from 'app/components/links/link';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import withOrganization from 'app/utils/withOrganization';
var TeamMembers = /** @class */ (function (_super) {
    __extends(TeamMembers, _super);
    function TeamMembers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            dropdownBusy: false,
            teamMemberList: [],
            orgMemberList: [],
        };
        _this.debouncedFetchMembersRequest = debounce(function (query) {
            return _this.setState({ dropdownBusy: true }, function () { return _this.fetchMembersRequest(query); });
        }, 200);
        _this.fetchMembersRequest = function (query) { return __awaiter(_this, void 0, void 0, function () {
            var _a, params, api, orgId, data, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, params = _a.params, api = _a.api;
                        orgId = params.orgId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/members/", {
                                query: { query: query },
                            })];
                    case 2:
                        data = _b.sent();
                        this.setState({
                            orgMemberList: data,
                            dropdownBusy: false,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        addErrorMessage(t('Unable to load organization members.'), {
                            duration: 2000,
                        });
                        this.setState({
                            dropdownBusy: false,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, params, data, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/teams/" + params.orgId + "/" + params.teamId + "/members/")];
                    case 2:
                        data = _b.sent();
                        this.setState({
                            teamMemberList: data,
                            loading: false,
                            error: false,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: true,
                        });
                        return [3 /*break*/, 4];
                    case 4:
                        this.fetchMembersRequest('');
                        return [2 /*return*/];
                }
            });
        }); };
        _this.addTeamMember = function (selection) {
            var params = _this.props.params;
            _this.setState({ loading: true });
            // Reset members list after adding member to team
            _this.debouncedFetchMembersRequest('');
            joinTeam(_this.props.api, {
                orgId: params.orgId,
                teamId: params.teamId,
                memberId: selection.value,
            }, {
                success: function () {
                    var orgMember = _this.state.orgMemberList.find(function (member) { return member.id === selection.value; });
                    if (orgMember === undefined) {
                        return;
                    }
                    _this.setState({
                        loading: false,
                        error: false,
                        teamMemberList: _this.state.teamMemberList.concat([orgMember]),
                    });
                    addSuccessMessage(t('Successfully added member to team.'));
                },
                error: function () {
                    _this.setState({
                        loading: false,
                    });
                    addErrorMessage(t('Unable to add team member.'));
                },
            });
        };
        /**
         * We perform an API request to support orgs with > 100 members (since that's the max API returns)
         *
         * @param {Event} e React Event when member filter input changes
         */
        _this.handleMemberFilterChange = function (e) {
            _this.setState({ dropdownBusy: true });
            _this.debouncedFetchMembersRequest(e.target.value);
        };
        return _this;
    }
    TeamMembers.prototype.componentDidMount = function () {
        this.fetchData();
    };
    TeamMembers.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        var params = this.props.params;
        if (nextProps.params.teamId !== params.teamId ||
            nextProps.params.orgId !== params.orgId) {
            this.setState({
                loading: true,
                error: false,
            }, this.fetchData);
        }
    };
    TeamMembers.prototype.removeMember = function (member) {
        var _this = this;
        var params = this.props.params;
        leaveTeam(this.props.api, {
            orgId: params.orgId,
            teamId: params.teamId,
            memberId: member.id,
        }, {
            success: function () {
                _this.setState({
                    teamMemberList: _this.state.teamMemberList.filter(function (m) { return m.id !== member.id; }),
                });
                addSuccessMessage(t('Successfully removed member from team.'));
            },
            error: function () {
                return addErrorMessage(t('There was an error while trying to remove a member from the team.'));
            },
        });
    };
    TeamMembers.prototype.renderDropdown = function (hasWriteAccess) {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params;
        var existingMembers = new Set(this.state.teamMemberList.map(function (member) { return member.id; }));
        // members can add other members to a team if the `Open Membership` setting is enabled
        // otherwise, `org:write` or `team:admin` permissions are required
        var hasOpenMembership = !!(organization === null || organization === void 0 ? void 0 : organization.openMembership);
        var canAddMembers = hasOpenMembership || hasWriteAccess;
        var items = (this.state.orgMemberList || [])
            .filter(function (m) { return !existingMembers.has(m.id); })
            .map(function (m) { return ({
            searchKey: m.name + " " + m.email,
            value: m.id,
            label: (<StyledUserListElement>
            <StyledAvatar user={m} size={24} className="avatar"/>
            <StyledNameOrEmail>{m.name || m.email}</StyledNameOrEmail>
          </StyledUserListElement>),
        }); });
        var menuHeader = (<StyledMembersLabel>
        {t('Members')}
        <StyledCreateMemberLink to="" onClick={function () { return openInviteMembersModal({ source: 'teams' }); }} data-test-id="invite-member">
          {t('Invite Member')}
        </StyledCreateMemberLink>
      </StyledMembersLabel>);
        return (<DropdownAutoComplete items={items} alignMenu="right" onSelect={canAddMembers
            ? this.addTeamMember
            : function (selection) {
                return openTeamAccessRequestModal({
                    teamId: params.teamId,
                    orgId: params.orgId,
                    memberId: selection.value,
                });
            }} menuHeader={menuHeader} emptyMessage={t('No members')} onChange={this.handleMemberFilterChange} busy={this.state.dropdownBusy} onClose={function () { return _this.debouncedFetchMembersRequest(''); }}>
        {function (_a) {
            var isOpen = _a.isOpen;
            return (<DropdownButton isOpen={isOpen} size="xsmall" data-test-id="add-member">
            {t('Add Member')}
          </DropdownButton>);
        }}
      </DropdownAutoComplete>);
    };
    TeamMembers.prototype.removeButton = function (member) {
        var _this = this;
        return (<Button size="small" icon={<IconSubtract size="xs" isCircled/>} onClick={function () { return _this.removeMember(member); }} label={t('Remove')}>
        {t('Remove')}
      </Button>);
    };
    TeamMembers.prototype.render = function () {
        var _this = this;
        if (this.state.loading) {
            return <LoadingIndicator />;
        }
        if (this.state.error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        var _a = this.props, params = _a.params, organization = _a.organization, config = _a.config;
        var access = organization.access;
        var hasWriteAccess = access.includes('org:write') || access.includes('team:admin');
        return (<Panel>
        <PanelHeader hasButtons>
          <div>{t('Members')}</div>
          <div style={{ textTransform: 'none' }}>{this.renderDropdown(hasWriteAccess)}</div>
        </PanelHeader>
        {this.state.teamMemberList.length ? (this.state.teamMemberList.map(function (member) {
            var isSelf = member.email === config.user.email;
            var canRemoveMember = hasWriteAccess || isSelf;
            return (<StyledMemberContainer key={member.id}>
                <IdBadge avatarSize={36} member={member} useLink orgId={params.orgId}/>
                {canRemoveMember && _this.removeButton(member)}
              </StyledMemberContainer>);
        })) : (<EmptyMessage icon={<IconUser size="xl"/>} size="large">
            {t('This team has no members')}
          </EmptyMessage>)}
      </Panel>);
    };
    return TeamMembers;
}(React.Component));
var StyledMemberContainer = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  justify-content: space-between;\n  align-items: center;\n"])));
var StyledUserListElement = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(0.5));
var StyledNameOrEmail = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, overflowEllipsis);
var StyledAvatar = styled(function (props) { return <UserAvatar {...props}/>; })(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  min-width: 1.75em;\n  min-height: 1.75em;\n  width: 1.5em;\n  height: 1.5em;\n"], ["\n  min-width: 1.75em;\n  min-height: 1.75em;\n  width: 1.5em;\n  height: 1.5em;\n"])));
var StyledMembersLabel = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  padding: ", " 0;\n  font-size: ", ";\n  text-transform: uppercase;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  padding: ", " 0;\n  font-size: ", ";\n  text-transform: uppercase;\n"])), space(1), function (p) { return p.theme.fontSizeExtraSmall; });
var StyledCreateMemberLink = styled(Link)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-transform: none;\n"], ["\n  text-transform: none;\n"])));
export default withConfig(withApi(withOrganization(TeamMembers)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=teamMembers.jsx.map