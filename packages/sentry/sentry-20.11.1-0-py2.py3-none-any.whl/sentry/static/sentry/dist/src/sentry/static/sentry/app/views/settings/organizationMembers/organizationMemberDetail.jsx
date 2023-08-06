import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { inputStyles } from 'app/styles/input';
import { removeAuthenticator } from 'app/actionCreators/account';
import { resendMemberInvite, updateMember } from 'app/actionCreators/members';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import AutoSelectText from 'app/components/autoSelectText';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import DateTime from 'app/components/dateTime';
import ExternalLink from 'app/components/links/externalLink';
import Field from 'app/views/settings/components/forms/field';
import NotFound from 'app/components/errors/notFound';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TeamSelect from 'app/views/settings/components/teamSelect';
import Tooltip from 'app/components/tooltip';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import RoleSelect from './inviteMember/roleSelect';
var MULTIPLE_ORGS = t('Cannot be reset since user is in more than one organization');
var NOT_ENROLLED = t('Not enrolled in two-factor authentication');
var NO_PERMISSION = t('You do not have permission to perform this action');
var TWO_FACTOR_REQUIRED = t('Cannot be reset since two-factor is required for this organization');
var OrganizationMemberDetail = /** @class */ (function (_super) {
    __extends(OrganizationMemberDetail, _super);
    function OrganizationMemberDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSave = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, params, resp_1, errorMessage;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, params = _a.params;
                        addLoadingMessage(t('Saving...'));
                        this.setState({ busy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, updateMember(this.api, {
                                orgId: organization.slug,
                                memberId: params.memberId,
                                data: this.state.member,
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(t('Saved'));
                        this.redirectToMemberPage();
                        return [3 /*break*/, 4];
                    case 3:
                        resp_1 = _b.sent();
                        errorMessage = (resp_1 && resp_1.responseJSON && resp_1.responseJSON.detail) || t('Could not save...');
                        addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleInvite = function (regenerate) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, params, data_1, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, params = _a.params;
                        addLoadingMessage(t('Sending invite...'));
                        this.setState({ busy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, resendMemberInvite(this.api, {
                                orgId: organization.slug,
                                memberId: params.memberId,
                                regenerate: regenerate,
                            })];
                    case 2:
                        data_1 = _b.sent();
                        addSuccessMessage(t('Sent invite!'));
                        if (regenerate) {
                            this.setState(function (state) { return ({ member: __assign(__assign({}, state.member), data_1) }); });
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        addErrorMessage(t('Could not send invite'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleAddTeam = function (team) {
            var member = _this.state.member;
            if (!member.teams.includes(team.slug)) {
                member.teams.push(team.slug);
            }
            _this.setState({ member: member });
        };
        _this.handleRemoveTeam = function (removedTeam) {
            var member = _this.state.member;
            _this.setState({
                member: __assign(__assign({}, member), { teams: member.teams.filter(function (slug) { return slug !== removedTeam; }) }),
            });
        };
        _this.handle2faReset = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, router, user, requests, err_1;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, router = _a.router;
                        user = this.state.member.user;
                        requests = user.authenticators.map(function (auth) {
                            return removeAuthenticator(_this.api, user.id, auth.id);
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(requests)];
                    case 2:
                        _b.sent();
                        router.push("/settings/" + organization.slug + "/members/");
                        addSuccessMessage(t('All authenticators have been removed'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        addErrorMessage(t('Error removing authenticators'));
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.showResetButton = function () {
            var organization = _this.props.organization;
            var member = _this.state.member;
            var user = member.user;
            if (!user || !user.authenticators || organization.require2FA) {
                return false;
            }
            var hasAuth = user.authenticators.length >= 1;
            return hasAuth && user.canReset2fa;
        };
        _this.getTooltip = function () {
            var organization = _this.props.organization;
            var member = _this.state.member;
            var user = member.user;
            if (!user) {
                return '';
            }
            if (!user.authenticators) {
                return NO_PERMISSION;
            }
            if (!user.authenticators.length) {
                return NOT_ENROLLED;
            }
            if (!user.canReset2fa) {
                return MULTIPLE_ORGS;
            }
            if (organization.require2FA) {
                return TWO_FACTOR_REQUIRED;
            }
            return '';
        };
        return _this;
    }
    OrganizationMemberDetail.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { roleList: [], selectedRole: '', member: null });
    };
    OrganizationMemberDetail.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        return [
            ['member', "/organizations/" + organization.slug + "/members/" + params.memberId + "/"],
        ];
    };
    OrganizationMemberDetail.prototype.redirectToMemberPage = function () {
        var _a = this.props, location = _a.location, params = _a.params, routes = _a.routes;
        var members = recreateRoute('members/', {
            location: location,
            routes: routes,
            params: params,
            stepBack: -2,
        });
        browserHistory.push(members);
    };
    OrganizationMemberDetail.prototype.renderBody = function () {
        var _this = this;
        var organization = this.props.organization;
        var member = this.state.member;
        if (!member) {
            return <NotFound />;
        }
        var access = organization.access;
        var inviteLink = member.invite_link;
        var canEdit = access.includes('org:write');
        var email = member.email, expired = member.expired, pending = member.pending;
        var canResend = !expired;
        var showAuth = !pending;
        return (<React.Fragment>
        <SettingsPageHeader title={<React.Fragment>
              <div>{member.name}</div>
              <ExtraHeaderText>{t('Member Settings')}</ExtraHeaderText>
            </React.Fragment>}/>

        <Panel>
          <PanelHeader>{t('Basics')}</PanelHeader>

          <PanelBody>
            <PanelItem>
              <OverflowWrapper>
                <Details>
                  <div>
                    <DetailLabel>{t('Email')}</DetailLabel>
                    <div>
                      <ExternalLink href={"mailto:" + email}>{email}</ExternalLink>
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{t('Status')}</DetailLabel>
                    <div data-test-id="member-status">
                      {member.expired ? (<em>{t('Invitation Expired')}</em>) : member.pending ? (<em>{t('Invitation Pending')}</em>) : (t('Active'))}
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{t('Added')}</DetailLabel>
                    <div>
                      <DateTime dateOnly date={member.dateCreated}/>
                    </div>
                  </div>
                </Details>

                {inviteLink && (<InviteSection>
                    <div>
                      <DetailLabel>{t('Invite Link')}</DetailLabel>
                      <AutoSelectText>
                        <CodeInput>{inviteLink}</CodeInput>
                      </AutoSelectText>
                      <p className="help-block">
                        {t('This unique invite link may only be used by this member.')}
                      </p>
                    </div>
                    <InviteActions>
                      <Button onClick={function () { return _this.handleInvite(true); }}>
                        {t('Generate New Invite')}
                      </Button>
                      {canResend && (<Button data-test-id="resend-invite" onClick={function () { return _this.handleInvite(false); }}>
                          {t('Resend Invite')}
                        </Button>)}
                    </InviteActions>
                  </InviteSection>)}
              </OverflowWrapper>
            </PanelItem>
          </PanelBody>
        </Panel>

        {showAuth && (<Panel>
            <PanelHeader>{t('Authentication')}</PanelHeader>
            <PanelBody>
              <Field alignRight flexibleControlStateSize label={t('Reset two-factor authentication')} help={t('Resetting two-factor authentication will remove all two-factor authentication methods for this member.')}>
                <Tooltip data-test-id="reset-2fa-tooltip" disabled={this.showResetButton()} title={this.getTooltip()}>
                  <Confirm disabled={!this.showResetButton()} message={tct('Are you sure you want to disable all two-factor authentication methods for [name]?', { name: member.name ? member.name : 'this member' })} onConfirm={this.handle2faReset} data-test-id="reset-2fa-confirm">
                    <Button data-test-id="reset-2fa" priority="danger">
                      {t('Reset two-factor authentication')}
                    </Button>
                  </Confirm>
                </Tooltip>
              </Field>
            </PanelBody>
          </Panel>)}

        <RoleSelect enforceAllowed={false} disabled={!canEdit} roleList={member.roles} selectedRole={member.role} setRole={function (slug) { return _this.setState({ member: __assign(__assign({}, member), { role: slug }) }); }}/>

        <TeamSelect organization={organization} selectedTeams={member.teams} disabled={!canEdit} onAddTeam={this.handleAddTeam} onRemoveTeam={this.handleRemoveTeam}/>

        <Footer>
          <Button priority="primary" busy={this.state.busy} onClick={this.handleSave} disabled={!canEdit}>
            {t('Save Member')}
          </Button>
        </Footer>
      </React.Fragment>);
    };
    return OrganizationMemberDetail;
}(AsyncView));
export default withOrganization(OrganizationMemberDetail);
var ExtraHeaderText = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeLarge; });
var Details = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-template-columns: 2fr 1fr 1fr;\n  grid-gap: ", ";\n  width: 100%;\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-template-columns: auto;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-template-columns: 2fr 1fr 1fr;\n  grid-gap: ", ";\n  width: 100%;\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-template-columns: auto;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var DetailLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n  margin-bottom: ", ";\n  color: ", ";\n"], ["\n  font-weight: bold;\n  margin-bottom: ", ";\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.textColor; });
var OverflowWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  overflow: hidden;\n  flex: 1;\n"], ["\n  overflow: hidden;\n  flex: 1;\n"])));
var InviteSection = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin-top: ", ";\n  padding-top: ", ";\n"], ["\n  border-top: 1px solid ", ";\n  margin-top: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.border; }, space(2), space(2));
var CodeInput = styled('code')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", "; /* Have to do this for typescript :( */\n"], ["\n  ", "; /* Have to do this for typescript :( */\n"])), function (p) { return inputStyles(p); });
var InviteActions = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  margin-top: ", ";\n"])), space(1), space(2));
var Footer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=organizationMemberDetail.jsx.map