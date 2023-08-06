import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Link from 'app/components/links/link';
import { PanelItem } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
var ROUTE_PREFIX = '/settings/account/api/';
var Row = /** @class */ (function (_super) {
    __extends(Row, _super);
    function Row() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
        };
        _this.handleRemove = function () {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props, api = _a.api, app = _a.app, onRemove = _a.onRemove;
            _this.setState({
                loading: true,
            }, function () { return __awaiter(_this, void 0, void 0, function () {
                var _err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            addLoadingMessage();
                            _a.label = 1;
                        case 1:
                            _a.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, api.requestPromise("/api-applications/" + app.id + "/", {
                                    method: 'DELETE',
                                })];
                        case 2:
                            _a.sent();
                            clearIndicators();
                            onRemove(app);
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _a.sent();
                            addErrorMessage(t('Unable to remove application. Please try again.'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            }); });
        };
        return _this;
    }
    Row.prototype.render = function () {
        var app = this.props.app;
        return (<StyledPanelItem>
        <ApplicationNameWrapper>
          <ApplicationName to={ROUTE_PREFIX + "applications/" + app.id + "/"}>
            {getDynamicText({ value: app.name, fixed: 'CI_APPLICATION_NAME' })}
          </ApplicationName>
          <ClientId>
            {getDynamicText({ value: app.clientID, fixed: 'CI_CLIENT_ID' })}
          </ClientId>
        </ApplicationNameWrapper>

        <Button aria-label="Remove" onClick={this.handleRemove} disabled={this.state.loading} icon={<IconDelete />}/>
      </StyledPanelItem>);
    };
    return Row;
}(React.Component));
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  align-items: center;\n"], ["\n  padding: ", ";\n  align-items: center;\n"])), space(2));
var ApplicationNameWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n  margin-right: ", ";\n"])), space(1));
var ApplicationName = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space(0.5));
var ClientId = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.fontSizeMedium; });
export default Row;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=row.jsx.map