import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { disconnectIdentity } from 'app/actionCreators/account';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var ENDPOINT = '/users/me/social-identities/';
var AccountIdentities = /** @class */ (function (_super) {
    __extends(AccountIdentities, _super);
    function AccountIdentities() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisconnect = function (identity) {
            var identities = _this.state.identities;
            _this.setState(function (state) {
                var _a;
                var newIdentities = (_a = state.identities) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                    var id = _a.id;
                    return id !== identity.id;
                });
                return {
                    identities: newIdentities !== null && newIdentities !== void 0 ? newIdentities : [],
                };
            }, function () {
                return disconnectIdentity(identity).catch(function () {
                    _this.setState({
                        identities: identities,
                    });
                });
            });
        };
        return _this;
    }
    AccountIdentities.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { identities: [] });
    };
    AccountIdentities.prototype.getEndpoints = function () {
        return [['identities', ENDPOINT]];
    };
    AccountIdentities.prototype.getTitle = function () {
        return t('Identities');
    };
    AccountIdentities.prototype.renderBody = function () {
        var _this = this;
        var _a;
        return (<div>
        <SettingsPageHeader title="Identities"/>
        <Panel>
          <PanelHeader>{t('Identities')}</PanelHeader>
          <PanelBody>
            {!((_a = this.state.identities) === null || _a === void 0 ? void 0 : _a.length) ? (<EmptyMessage>
                {t('There are no identities associated with this account')}
              </EmptyMessage>) : (this.state.identities.map(function (identity) { return (<IdentityPanelItem key={identity.id}>
                  <div>{identity.providerLabel}</div>

                  <Button size="small" onClick={_this.handleDisconnect.bind(_this, identity)}>
                    {t('Disconnect')}
                  </Button>
                </IdentityPanelItem>); }))}
          </PanelBody>
        </Panel>
      </div>);
    };
    return AccountIdentities;
}(AsyncView));
var IdentityPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
export default AccountIdentities;
var templateObject_1;
//# sourceMappingURL=accountIdentities.jsx.map