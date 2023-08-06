import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import space from 'app/styles/space';
var AccountAuthorizations = /** @class */ (function (_super) {
    __extends(AccountAuthorizations, _super);
    function AccountAuthorizations() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRevoke = function (authorization) {
            var oldData = _this.state.data;
            _this.setState(function (state) { return ({
                data: state.data.filter(function (_a) {
                    var id = _a.id;
                    return id !== authorization.id;
                }),
            }); }, function () { return __awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            return [4 /*yield*/, this.api.requestPromise('/api-authorizations/', {
                                    method: 'DELETE',
                                    data: { authorization: authorization.id },
                                })];
                        case 1:
                            _a.sent();
                            addSuccessMessage(t('Saved changes'));
                            return [3 /*break*/, 3];
                        case 2:
                            _err_1 = _a.sent();
                            this.setState({
                                data: oldData,
                            });
                            addErrorMessage(t('Unable to save changes, please try again'));
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    AccountAuthorizations.prototype.getEndpoints = function () {
        return [['data', '/api-authorizations/']];
    };
    AccountAuthorizations.prototype.getTitle = function () {
        return 'Approved Applications';
    };
    AccountAuthorizations.prototype.renderBody = function () {
        var _this = this;
        var data = this.state.data;
        var isEmpty = data.length === 0;
        return (<div>
        <SettingsPageHeader title="Authorized Applications"/>
        <Description>
          {tct('You can manage your own applications via the [link:API dashboard].', {
            link: <Link to="/settings/account/api/"/>,
        })}
        </Description>

        <Panel>
          <PanelHeader>{t('Approved Applications')}</PanelHeader>

          <PanelBody>
            {isEmpty && (<EmptyMessage>
                {t("You haven't approved any third party applications.")}
              </EmptyMessage>)}

            {!isEmpty && (<div>
                {data.map(function (authorization) { return (<PanelItemCenter key={authorization.id}>
                    <ApplicationDetails>
                      <ApplicationName>{authorization.application.name}</ApplicationName>
                      {authorization.homepageUrl && (<Url>
                          <a href={authorization.homepageUrl}>
                            {authorization.homepageUrl}
                          </a>
                        </Url>)}
                      <Scopes>{authorization.scopes.join(', ')}</Scopes>
                    </ApplicationDetails>
                    <Button size="small" onClick={function () { return _this.handleRevoke(authorization); }} icon={<IconDelete />}/>
                  </PanelItemCenter>); })}
              </div>)}
          </PanelBody>
        </Panel>
      </div>);
    };
    return AccountAuthorizations;
}(AsyncView));
export default AccountAuthorizations;
var Description = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, space(4));
var PanelItemCenter = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var ApplicationDetails = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
var ApplicationName = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: bold;\n  margin-bottom: ", ";\n"], ["\n  font-weight: bold;\n  margin-bottom: ", ";\n"])), space(0.5));
/**
 * Intentionally wrap <a> so that it does not take up full width and cause
 * hit box issues
 */
var Url = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeRelativeSmall; });
var Scopes = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeRelativeSmall; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=accountAuthorizations.jsx.map