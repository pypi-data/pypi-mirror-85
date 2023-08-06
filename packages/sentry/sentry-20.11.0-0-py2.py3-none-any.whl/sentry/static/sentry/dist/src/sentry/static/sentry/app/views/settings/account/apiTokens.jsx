import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import AlertLink from 'app/components/alertLink';
import ApiTokenRow from 'app/views/settings/account/apiTokenRow';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import withOrganization from 'app/utils/withOrganization';
var ApiTokens = /** @class */ (function (_super) {
    __extends(ApiTokens, _super);
    function ApiTokens() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemoveToken = function (token) {
            addLoadingMessage();
            var oldTokenList = _this.state.tokenList;
            _this.setState(function (state) {
                var _a, _b;
                return ({
                    tokenList: (_b = (_a = state.tokenList) === null || _a === void 0 ? void 0 : _a.filter(function (tk) { return tk.token !== token.token; })) !== null && _b !== void 0 ? _b : [],
                });
            }, function () { return __awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            return [4 /*yield*/, this.api.requestPromise('/api-tokens/', {
                                    method: 'DELETE',
                                    data: { token: token.token },
                                })];
                        case 1:
                            _a.sent();
                            addSuccessMessage(t('Removed token'));
                            return [3 /*break*/, 3];
                        case 2:
                            _err_1 = _a.sent();
                            addErrorMessage(t('Unable to remove token. Please try again.'));
                            this.setState({
                                tokenList: oldTokenList,
                            });
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    ApiTokens.prototype.getTitle = function () {
        return t('API Tokens');
    };
    ApiTokens.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { tokenList: [] });
    };
    ApiTokens.prototype.getEndpoints = function () {
        return [['tokenList', '/api-tokens/']];
    };
    ApiTokens.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var tokenList = this.state.tokenList;
        var isEmpty = !Array.isArray(tokenList) || tokenList.length === 0;
        var action = (<Button priority="primary" size="small" to="/settings/account/api/auth-tokens/new-token/" data-test-id="create-token">
        {t('Create New Token')}
      </Button>);
        return (<div>
        <SettingsPageHeader title="Auth Tokens" action={action}/>
        <AlertLink to={"/settings/" + ((_a = organization === null || organization === void 0 ? void 0 : organization.slug) !== null && _a !== void 0 ? _a : '') + "/developer-settings/new-internal"}>
          {t("Auth Tokens are tied to the logged in user, meaning they'll stop working if the user leaves the organization! We suggest using internal integrations to create/manage tokens tied to the organization instead.")}
        </AlertLink>
        <TextBlock>
          {t("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
        </TextBlock>
        <TextBlock>
          {tct('For more information on how to use the web API, see our [link:documentation].', {
            link: <a href="https://docs.sentry.io/api/"/>,
        })}
        </TextBlock>
        <TextBlock>
          <small>
            psst. Looking for the <strong>DSN</strong> for an SDK? You'll find that under{' '}
            <strong>[Project] » Settings » Client Keys</strong>.
          </small>
        </TextBlock>
        <Panel>
          <PanelHeader>{t('Auth Token')}</PanelHeader>

          <PanelBody>
            {isEmpty && (<EmptyMessage>
                {t("You haven't created any authentication tokens yet.")}
              </EmptyMessage>)}

            {tokenList === null || tokenList === void 0 ? void 0 : tokenList.map(function (token) { return (<ApiTokenRow key={token.token} token={token} onRemove={_this.handleRemoveToken}/>); })}
          </PanelBody>
        </Panel>
      </div>);
    };
    return ApiTokens;
}(AsyncView));
export { ApiTokens };
export default withOrganization(ApiTokens);
//# sourceMappingURL=apiTokens.jsx.map