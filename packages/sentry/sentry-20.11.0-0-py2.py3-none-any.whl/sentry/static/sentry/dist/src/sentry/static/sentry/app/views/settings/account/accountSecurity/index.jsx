import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import CircleIndicator from 'app/components/circleIndicator';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Field from 'app/views/settings/components/forms/field';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import { IconDelete } from 'app/icons';
import PasswordForm from 'app/views/settings/account/passwordForm';
import RemoveConfirm from 'app/views/settings/account/accountSecurity/components/removeConfirm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import Tooltip from 'app/components/tooltip';
import TwoFactorRequired from 'app/views/settings/account/accountSecurity/components/twoFactorRequired';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
/**
 * Lists 2fa devices + password change form
 */
var AccountSecurity = /** @class */ (function (_super) {
    __extends(AccountSecurity, _super);
    function AccountSecurity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSessionClose = function () { return __awaiter(_this, void 0, void 0, function () {
            var err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.api.requestPromise('/auth/', {
                                method: 'DELETE',
                                data: { all: true },
                            })];
                    case 1:
                        _a.sent();
                        window.location.assign('/auth/login/');
                        return [3 /*break*/, 3];
                    case 2:
                        err_1 = _a.sent();
                        addErrorMessage(t('There was a problem closing all sessions'));
                        throw err_1;
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.formatOrgSlugs = function () {
            var orgsRequire2fa = _this.props.orgsRequire2fa;
            var slugs = orgsRequire2fa.map(function (_a) {
                var slug = _a.slug;
                return slug;
            });
            return [slugs.slice(0, -1).join(', '), slugs.slice(-1)[0]].join(slugs.length > 1 ? ' and ' : '');
        };
        return _this;
    }
    AccountSecurity.prototype.getTitle = function () {
        return t('Security');
    };
    AccountSecurity.prototype.getEndpoints = function () {
        return [];
    };
    AccountSecurity.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, authenticators = _a.authenticators, countEnrolled = _a.countEnrolled, deleteDisabled = _a.deleteDisabled, onDisable = _a.onDisable;
        var isEmpty = !(authenticators === null || authenticators === void 0 ? void 0 : authenticators.length);
        return (<div>
        <SettingsPageHeader title={t('Security')} tabs={<NavTabs underlined>
              <ListLink to={recreateRoute('', this.props)} index>
                {t('Settings')}
              </ListLink>
              <ListLink to={recreateRoute('session-history/', this.props)}>
                {t('Session History')}
              </ListLink>
            </NavTabs>}/>

        {!isEmpty && countEnrolled === 0 && <TwoFactorRequired />}

        <PasswordForm />

        <Panel>
          <PanelHeader>{t('Sessions')}</PanelHeader>
          <PanelBody>
            <Field alignRight flexibleControlStateSize label={t('Sign out of all devices')} help={t('Signing out of all devices will sign you out of this device as well.')}>
              <Button data-test-id="signoutAll" onClick={this.handleSessionClose}>
                {t('Sign out of all devices')}
              </Button>
            </Field>
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader>{t('Two-Factor Authentication')}</PanelHeader>

          {isEmpty && (<EmptyMessage>{t('No available authenticators to add')}</EmptyMessage>)}

          <PanelBody>
            {!isEmpty && (authenticators === null || authenticators === void 0 ? void 0 : authenticators.map(function (auth) {
            var id = auth.id, authId = auth.authId, description = auth.description, isBackupInterface = auth.isBackupInterface, isEnrolled = auth.isEnrolled, configureButton = auth.configureButton, name = auth.name;
            return (<AuthenticatorPanelItem key={id}>
                    <AuthenticatorHeader>
                      <AuthenticatorTitle>
                        <AuthenticatorStatus enabled={isEnrolled}/>
                        <AuthenticatorName>{name}</AuthenticatorName>
                      </AuthenticatorTitle>

                      <Actions>
                        {!isBackupInterface && !isEnrolled && (<Button to={"/settings/account/security/mfa/" + id + "/enroll/"} size="small" priority="primary" className="enroll-button">
                            {t('Add')}
                          </Button>)}

                        {isEnrolled && authId && (<Button to={"/settings/account/security/mfa/" + authId + "/"} size="small" className="details-button">
                            {configureButton}
                          </Button>)}

                        {!isBackupInterface && isEnrolled && (<Tooltip title={t("Two-factor authentication is required for organization(s): " + _this.formatOrgSlugs() + ".")} disabled={!deleteDisabled}>
                            <RemoveConfirm onConfirm={function () { return onDisable(auth); }} disabled={deleteDisabled}>
                              <Button size="small" label={t('delete')} icon={<IconDelete />}/>
                            </RemoveConfirm>
                          </Tooltip>)}
                      </Actions>

                      {isBackupInterface && !isEnrolled ? t('requires 2FA') : null}
                    </AuthenticatorHeader>

                    <Description>{description}</Description>
                  </AuthenticatorPanelItem>);
        }))}
          </PanelBody>
        </Panel>
      </div>);
    };
    return AccountSecurity;
}(AsyncView));
var AuthenticatorName = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
var AuthenticatorPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var AuthenticatorHeader = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var AuthenticatorTitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Actions = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space(1));
var AuthenticatorStatus = styled(CircleIndicator)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Description = styled(TextBlock)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: 0;\n"], ["\n  margin-top: ", ";\n  margin-bottom: 0;\n"])), space(2));
export default AccountSecurity;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map