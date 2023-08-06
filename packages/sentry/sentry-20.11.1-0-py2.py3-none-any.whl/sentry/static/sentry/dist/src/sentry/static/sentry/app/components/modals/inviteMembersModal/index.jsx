import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { t, tn, tct } from 'app/locale';
import { MEMBER_ROLES } from 'app/constants';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { uniqueId } from 'app/utils/guid';
import { IconCheckmark, IconWarning, IconAdd } from 'app/icons';
import Button from 'app/components/button';
import HookOrDefault from 'app/components/hookOrDefault';
import QuestionTooltip from 'app/components/questionTooltip';
import space from 'app/styles/space';
import AsyncComponent from 'app/components/asyncComponent';
import withLatestContext from 'app/utils/withLatestContext';
import withTeams from 'app/utils/withTeams';
import LoadingIndicator from 'app/components/loadingIndicator';
import InviteRowControl from './inviteRowControl';
var DEFAULT_ROLE = 'member';
var InviteModalHook = HookOrDefault({
    hookName: 'member-invite-modal:customization',
    defaultComponent: function (_a) {
        var onSendInvites = _a.onSendInvites, children = _a.children;
        return children({ sendInvites: onSendInvites, canSend: true });
    },
});
var InviteMembersModal = /** @class */ (function (_super) {
    __extends(InviteMembersModal, _super);
    function InviteMembersModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Used for analytics tracking of the modals usage.
         */
        _this.sessionId = '';
        _this.reset = function () {
            _this.setState({
                pendingInvites: [_this.inviteTemplate],
                inviteStatus: {},
                complete: false,
                sendingInvites: false,
            });
            trackAnalyticsEvent({
                eventKey: 'invite_modal.add_more',
                eventName: 'Invite Modal: Add More',
                organization_id: _this.props.organization.id,
                modal_session: _this.sessionId,
            });
        };
        _this.sendInvite = function (invite) { return __awaiter(_this, void 0, void 0, function () {
            var slug, data, endpoint, err_1, errorResponse, emailError, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        slug = this.props.organization.slug;
                        data = {
                            email: invite.email,
                            teams: __spread(invite.teams),
                            role: invite.role,
                        };
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: __assign(__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: false }, _a)),
                            });
                        });
                        endpoint = this.willInvite
                            ? "/organizations/" + slug + "/members/"
                            : "/organizations/" + slug + "/invite-requests/";
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, { method: 'POST', data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        errorResponse = err_1.responseJSON;
                        emailError = !errorResponse || !errorResponse.email
                            ? false
                            : Array.isArray(errorResponse.email)
                                ? errorResponse.email[0]
                                : errorResponse.email;
                        error_1 = emailError || t('Could not invite user');
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: __assign(__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: false, error: error_1 }, _a)),
                            });
                        });
                        return [2 /*return*/];
                    case 4:
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: __assign(__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: true }, _a)),
                            });
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.sendInvites = function () { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ sendingInvites: true });
                        return [4 /*yield*/, Promise.all(this.invites.map(this.sendInvite))];
                    case 1:
                        _a.sent();
                        this.setState({ sendingInvites: false, complete: true });
                        trackAnalyticsEvent({
                            eventKey: this.willInvite
                                ? 'invite_modal.invites_sent'
                                : 'invite_modal.requests_sent',
                            eventName: this.willInvite
                                ? 'Invite Modal: Invites Sent'
                                : 'Invite Modal: Requests Sent',
                            organization_id: this.props.organization.id,
                            modal_session: this.sessionId,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.addInviteRow = function () {
            return _this.setState(function (state) { return ({
                pendingInvites: __spread(state.pendingInvites, [_this.inviteTemplate]),
            }); });
        };
        return _this;
    }
    Object.defineProperty(InviteMembersModal.prototype, "inviteTemplate", {
        get: function () {
            return {
                emails: new Set(),
                teams: new Set(),
                role: DEFAULT_ROLE,
            };
        },
        enumerable: false,
        configurable: true
    });
    InviteMembersModal.prototype.componentDidMount = function () {
        this.sessionId = uniqueId();
        var _a = this.props, organization = _a.organization, source = _a.source;
        trackAnalyticsEvent({
            eventKey: 'invite_modal.opened',
            eventName: 'Invite Modal: Opened',
            organization_id: organization.id,
            modal_session: this.sessionId,
            can_invite: this.willInvite,
            source: source,
        });
    };
    InviteMembersModal.prototype.getEndpoints = function () {
        var orgId = this.props.organization.slug;
        return [['member', "/organizations/" + orgId + "/members/me/"]];
    };
    InviteMembersModal.prototype.getDefaultState = function () {
        var _this = this;
        var state = _super.prototype.getDefaultState.call(this);
        var initialData = this.props.initialData;
        var pendingInvites = initialData
            ? initialData.map(function (initial) { return (__assign(__assign({}, _this.inviteTemplate), initial)); })
            : [this.inviteTemplate];
        return __assign(__assign({}, state), { pendingInvites: pendingInvites, inviteStatus: {}, complete: false, sendingInvites: false });
    };
    InviteMembersModal.prototype.setEmails = function (emails, index) {
        this.setState(function (state) {
            var pendingInvites = __spread(state.pendingInvites);
            pendingInvites[index] = __assign(__assign({}, pendingInvites[index]), { emails: new Set(emails) });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.setTeams = function (teams, index) {
        this.setState(function (state) {
            var pendingInvites = __spread(state.pendingInvites);
            pendingInvites[index] = __assign(__assign({}, pendingInvites[index]), { teams: new Set(teams) });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.setRole = function (role, index) {
        this.setState(function (state) {
            var pendingInvites = __spread(state.pendingInvites);
            pendingInvites[index] = __assign(__assign({}, pendingInvites[index]), { role: role });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.removeInviteRow = function (index) {
        this.setState(function (state) {
            var pendingInvites = __spread(state.pendingInvites);
            pendingInvites.splice(index, 1);
            return { pendingInvites: pendingInvites };
        });
    };
    Object.defineProperty(InviteMembersModal.prototype, "invites", {
        get: function () {
            return this.state.pendingInvites.reduce(function (acc, row) { return __spread(acc, __spread(row.emails).map(function (email) { return ({ email: email, teams: row.teams, role: row.role }); })); }, []);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "hasDuplicateEmails", {
        get: function () {
            var emails = this.invites.map(function (inv) { return inv.email; });
            return emails.length !== new Set(emails).size;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "isValidInvites", {
        get: function () {
            return this.invites.length > 0 && !this.hasDuplicateEmails;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "statusMessage", {
        get: function () {
            var _a = this.state, sendingInvites = _a.sendingInvites, complete = _a.complete, inviteStatus = _a.inviteStatus;
            if (sendingInvites) {
                return (<StatusMessage>
          <LoadingIndicator mini relative hideMessage size={16}/>
          {this.willInvite
                    ? t('Sending organization invitations...')
                    : t('Sending invite requests...')}
        </StatusMessage>);
            }
            if (complete) {
                var statuses = Object.values(inviteStatus);
                var sentCount = statuses.filter(function (i) { return i.sent; }).length;
                var errorCount = statuses.filter(function (i) { return i.error; }).length;
                var invites = <strong>{tn('%s invite', '%s invites', sentCount)}</strong>;
                var tctComponents = {
                    invites: invites,
                    failed: errorCount,
                };
                return (<StatusMessage status="success">
          <IconCheckmark size="sm"/>
          {errorCount > 0
                    ? tct('Sent [invites], [failed] failed to send.', tctComponents)
                    : tct('Sent [invites]', tctComponents)}
        </StatusMessage>);
            }
            if (this.hasDuplicateEmails) {
                return (<StatusMessage status="error">
          <IconWarning size="sm"/>
          {t('Duplicate emails between invite rows.')}
        </StatusMessage>);
            }
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "willInvite", {
        get: function () {
            var _a;
            return (_a = this.props.organization.access) === null || _a === void 0 ? void 0 : _a.includes('member:write');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "inviteButtonLabel", {
        get: function () {
            if (this.invites.length > 0) {
                var numberInvites = this.invites.length;
                // Note we use `t()` here because `tn()` expects the same # of string formatters
                var inviteText = numberInvites === 1 ? t('Send invite') : t('Send invites (%s)', numberInvites);
                var requestText = numberInvites === 1
                    ? t('Send invite request')
                    : t('Send invite requests (%s)', numberInvites);
                return this.willInvite ? inviteText : requestText;
            }
            return this.willInvite ? t('Send invite') : t('Send invite request');
        },
        enumerable: false,
        configurable: true
    });
    InviteMembersModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Footer = _a.Footer, closeModal = _a.closeModal, organization = _a.organization, allTeams = _a.teams;
        var _b = this.state, pendingInvites = _b.pendingInvites, sendingInvites = _b.sendingInvites, complete = _b.complete, inviteStatus = _b.inviteStatus, member = _b.member;
        var disableInputs = sendingInvites || complete;
        // eslint-disable-next-line react/prop-types
        var hookRenderer = function (_a) {
            var sendInvites = _a.sendInvites, canSend = _a.canSend, headerInfo = _a.headerInfo;
            return (<React.Fragment>
        <Heading>
          {t('Invite New Members')}
          {!_this.willInvite && (<QuestionTooltip title={t("You do not have permission to directly invite members. Email\n                 addresses entered here will be forwarded to organization\n                 managers and owners; they will be prompted to approve the\n                 invitation.")} size="sm" position="bottom"/>)}
        </Heading>
        <Subtext>
          {_this.willInvite
                ? t('Invite new members by email to join your organization.')
                : t("You don\u2019t have permission to directly invite users, but we\u2019ll\n                 send a request on your behalf.")}
        </Subtext>

        {headerInfo}

        <InviteeHeadings>
          <div>{t('Email addresses')}</div>
          <div>{t('Role')}</div>
          <div>{t('Add to team')}</div>
        </InviteeHeadings>

        {pendingInvites.map(function (_a, i) {
                var emails = _a.emails, role = _a.role, teams = _a.teams;
                return (<StyledInviteRow key={i} disabled={disableInputs} emails={__spread(emails)} role={role} teams={__spread(teams)} roleOptions={member ? member.roles : MEMBER_ROLES} roleDisabledUnallowed={_this.willInvite} teamOptions={allTeams} inviteStatus={inviteStatus} onRemove={function () { return _this.removeInviteRow(i); }} onChangeEmails={function (opts) {
                    return _this.setEmails(opts.map(function (v) { return v.value; }), i);
                }} onChangeRole={function (_a) {
                    var value = _a.value;
                    return _this.setRole(value, i);
                }} onChangeTeams={function (opts) {
                    return _this.setTeams(opts.map(function (v) { return v.value; }), i);
                }} disableRemove={disableInputs || pendingInvites.length === 1}/>);
            })}

        <AddButton disabled={disableInputs} priority="link" onClick={_this.addInviteRow} icon={<IconAdd size="xs" isCircled/>}>
          {t('Add another')}
        </AddButton>

        <Footer>
          <FooterContent>
            <div>{_this.statusMessage}</div>

            {complete ? (<React.Fragment>
                <Button data-test-id="send-more" size="small" onClick={_this.reset}>
                  {t('Send more invites')}
                </Button>
                <Button data-test-id="close" priority="primary" size="small" onClick={function () {
                trackAnalyticsEvent({
                    eventKey: 'invite_modal.closed',
                    eventName: 'Invite Modal: Closed',
                    organization_id: _this.props.organization.id,
                    modal_session: _this.sessionId,
                });
                closeModal();
            }}>
                  {t('Close')}
                </Button>
              </React.Fragment>) : (<React.Fragment>
                <Button data-test-id="cancel" size="small" onClick={closeModal} disabled={disableInputs}>
                  {t('Cancel')}
                </Button>
                <Button size="small" data-test-id="send-invites" priority="primary" disabled={!canSend || !_this.isValidInvites || disableInputs} onClick={sendInvites}>
                  {_this.inviteButtonLabel}
                </Button>
              </React.Fragment>)}
          </FooterContent>
        </Footer>
      </React.Fragment>);
        };
        return (<InviteModalHook organization={organization} willInvite={this.willInvite} onSendInvites={this.sendInvites}>
        {hookRenderer}
      </InviteModalHook>);
    };
    return InviteMembersModal;
}(AsyncComponent));
var Heading = styled('h1')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  align-items: center;\n  font-weight: 400;\n  font-size: ", ";\n  margin-top: 0;\n  margin-bottom: ", ";\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  align-items: center;\n  font-weight: 400;\n  font-size: ", ";\n  margin-top: 0;\n  margin-bottom: ", ";\n"])), space(1.5), function (p) { return p.theme.headerFontSize; }, space(0.75));
var Subtext = styled('p')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space(3));
var inviteRowGrid = css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 3fr 180px 2fr max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 3fr 180px 2fr max-content;\n"])), space(1.5));
var InviteeHeadings = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n\n  margin-bottom: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  font-size: ", ";\n"], ["\n  ", ";\n\n  margin-bottom: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  font-size: ", ";\n"])), inviteRowGrid, space(1), function (p) { return p.theme.fontSizeSmall; });
var StyledInviteRow = styled(InviteRowControl)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n  margin-bottom: ", ";\n"], ["\n  ", ";\n  margin-bottom: ", ";\n"])), inviteRowGrid, space(1.5));
var AddButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(3));
var FooterContent = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: 100%;\n  display: grid;\n  grid-template-columns: 1fr max-content max-content;\n  grid-gap: ", ";\n"], ["\n  width: 100%;\n  display: grid;\n  grid-template-columns: 1fr max-content max-content;\n  grid-gap: ", ";\n"])), space(1));
var StatusMessage = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n\n  > :first-child {\n    ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n\n  > :first-child {\n    ", ";\n  }\n"])), space(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return (p.status === 'error' ? p.theme.red300 : p.theme.gray400); }, function (p) { return p.status === 'success' && "color: " + p.theme.green300; });
export var modalCss = css(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding: 50px;\n\n  .modal-dialog {\n    position: unset;\n    width: 100%;\n    max-width: 800px;\n    margin: 50px auto;\n  }\n"], ["\n  padding: 50px;\n\n  .modal-dialog {\n    position: unset;\n    width: 100%;\n    max-width: 800px;\n    margin: 50px auto;\n  }\n"])));
export default withLatestContext(withTeams(InviteMembersModal));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=index.jsx.map