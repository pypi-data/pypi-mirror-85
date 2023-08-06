import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import { urlEncode } from '@sentry/utils';
import React from 'react';
import styled from '@emotion/styled';
import { logout } from 'app/actionCreators/account';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import ConfigStore from 'app/stores/configStore';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import NarrowLayout from 'app/components/narrowLayout';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import space from 'app/styles/space';
var AcceptOrganizationInvite = /** @class */ (function (_super) {
    __extends(AcceptOrganizationInvite, _super);
    function AcceptOrganizationInvite() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLogout = function (e) { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        e.preventDefault();
                        return [4 /*yield*/, logout(this.api)];
                    case 1:
                        _a.sent();
                        window.location.replace(this.makeNextUrl('/auth/login/'));
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleAcceptInvite = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, memberId, token, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props.params, memberId = _a.memberId, token = _a.token;
                        this.setState({ accepting: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/accept-invite/" + memberId + "/" + token + "/", {
                                method: 'POST',
                            })];
                    case 2:
                        _c.sent();
                        browserHistory.replace("/" + this.state.inviteDetails.orgSlug + "/");
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ acceptError: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ accepting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AcceptOrganizationInvite.prototype.getEndpoints = function () {
        var _a = this.props.params, memberId = _a.memberId, token = _a.token;
        return [['inviteDetails', "/accept-invite/" + memberId + "/" + token + "/"]];
    };
    AcceptOrganizationInvite.prototype.getTitle = function () {
        return t('Accept Organization Invite');
    };
    AcceptOrganizationInvite.prototype.makeNextUrl = function (path) {
        return path + "?" + urlEncode({ next: window.location.pathname });
    };
    Object.defineProperty(AcceptOrganizationInvite.prototype, "existingMemberAlert", {
        get: function () {
            var user = ConfigStore.get('user');
            return (<Alert type="warning" data-test-id="existing-member">
        {tct('Your account ([email]) is already a member of this organization. [switchLink:Switch accounts]?', {
                email: user.email,
                switchLink: (<Link to="" data-test-id="existing-member-link" onClick={this.handleLogout}/>),
            })}
      </Alert>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "authenticationActions", {
        get: function () {
            var inviteDetails = this.state.inviteDetails;
            return (<React.Fragment>
        {!inviteDetails.requireSso && (<p data-test-id="action-info-general">
            {t("To continue, you must either create a new account, or login to an\n              existing Sentry account.")}
          </p>)}

        {inviteDetails.needsSso && (<p data-test-id="action-info-sso">
            {inviteDetails.requireSso
                ? tct("Note that [orgSlug] has required Single Sign-On (SSO) using\n               [authProvider]. You may create an account by authenticating with\n               the organization's SSO provider.", {
                    orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                    authProvider: inviteDetails.ssoProvider,
                })
                : tct("Note that [orgSlug] has enabled Single Sign-On (SSO) using\n               [authProvider]. You may create an account by authenticating with\n               the organization's SSO provider.", {
                    orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                    authProvider: inviteDetails.ssoProvider,
                })}
          </p>)}

        <Actions>
          <ActionsLeft>
            {inviteDetails.needsSso && (<Button label="sso-login" priority="primary" href={this.makeNextUrl("/auth/login/" + inviteDetails.orgSlug + "/")}>
                {t('Join with %s', inviteDetails.ssoProvider)}
              </Button>)}
            {!inviteDetails.requireSso && (<Button label="create-account" priority="primary" href={this.makeNextUrl('/auth/register/')}>
                {t('Create a new account')}
              </Button>)}
          </ActionsLeft>
          {!inviteDetails.requireSso && (<ExternalLink href={this.makeNextUrl('/auth/login/')} openInNewTab={false} data-test-id="link-with-existing">
              {t('Login using an existing account')}
            </ExternalLink>)}
        </Actions>
      </React.Fragment>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "warning2fa", {
        get: function () {
            var inviteDetails = this.state.inviteDetails;
            return (<React.Fragment>
        <p data-test-id="2fa-warning">
          {tct('To continue, [orgSlug] requires all members to configure two-factor authentication.', { orgSlug: inviteDetails.orgSlug })}
        </p>
        <Actions>
          <Button priority="primary" to="/settings/account/security/">
            {t('Configure Two-Factor Auth')}
          </Button>
        </Actions>
      </React.Fragment>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "acceptActions", {
        get: function () {
            var _a = this.state, inviteDetails = _a.inviteDetails, accepting = _a.accepting;
            return (<Actions>
        <Button label="join-organization" priority="primary" disabled={accepting} onClick={this.handleAcceptInvite}>
          {t('Join the %s organization', inviteDetails.orgSlug)}
        </Button>
      </Actions>);
        },
        enumerable: false,
        configurable: true
    });
    AcceptOrganizationInvite.prototype.renderError = function () {
        return (<NarrowLayout>
        <Alert type="warning">
          {t('This organization invite link is no longer valid.')}
        </Alert>
      </NarrowLayout>);
    };
    AcceptOrganizationInvite.prototype.renderBody = function () {
        var _a = this.state, inviteDetails = _a.inviteDetails, acceptError = _a.acceptError;
        return (<NarrowLayout>
        <SettingsPageHeader title={t('Accept organization invite')}/>
        {acceptError && (<Alert type="error">
            {t('Failed to join this organization. Please try again')}
          </Alert>)}
        <InviteDescription data-test-id="accept-invite">
          {tct('[orgSlug] is using Sentry to track and debug errors.', {
            orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
        })}
        </InviteDescription>
        {inviteDetails.needsAuthentication
            ? this.authenticationActions
            : inviteDetails.existingMember
                ? this.existingMemberAlert
                : inviteDetails.needs2fa
                    ? this.warning2fa
                    : this.acceptActions}
      </NarrowLayout>);
    };
    return AcceptOrganizationInvite;
}(AsyncView));
var Actions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(3));
var ActionsLeft = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  > a {\n    margin-right: ", ";\n  }\n"], ["\n  > a {\n    margin-right: ", ";\n  }\n"])), space(1));
var InviteDescription = styled('p')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
export default AcceptOrganizationInvite;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=acceptOrganizationInvite.jsx.map