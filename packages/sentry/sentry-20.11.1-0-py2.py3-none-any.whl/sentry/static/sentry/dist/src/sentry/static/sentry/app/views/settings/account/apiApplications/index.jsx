import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Row from 'app/views/settings/account/apiApplications/row';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import { IconAdd } from 'app/icons';
var ROUTE_PREFIX = '/settings/account/api/';
var ApiApplications = /** @class */ (function (_super) {
    __extends(ApiApplications, _super);
    function ApiApplications() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCreateApplication = function () { return __awaiter(_this, void 0, void 0, function () {
            var app, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        addLoadingMessage();
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/api-applications/', {
                                method: 'POST',
                            })];
                    case 2:
                        app = _a.sent();
                        addSuccessMessage(t('Created a new API Application'));
                        this.props.router.push(ROUTE_PREFIX + "applications/" + app.id + "/");
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Unable to remove application. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRemoveApplication = function (app) {
            _this.setState({
                appList: _this.state.appList.filter(function (a) { return a.id !== app.id; }),
            });
        };
        return _this;
    }
    ApiApplications.prototype.getEndpoints = function () {
        return [['appList', '/api-applications/']];
    };
    ApiApplications.prototype.getTitle = function () {
        return t('API Applications');
    };
    ApiApplications.prototype.renderBody = function () {
        var _this = this;
        var action = (<Button priority="primary" size="small" onClick={this.handleCreateApplication} icon={<IconAdd size="xs" isCircled/>}>
        {t('Create New Application')}
      </Button>);
        var isEmpty = this.state.appList.length === 0;
        return (<div>
        <SettingsPageHeader title="API Applications" action={action}/>

        <Panel>
          <PanelHeader>{t('Application Name')}</PanelHeader>

          <PanelBody>
            {!isEmpty ? (this.state.appList.map(function (app) { return (<Row api={_this.api} key={app.id} app={app} onRemove={_this.handleRemoveApplication}/>); })) : (<EmptyMessage>
                {t("You haven't created any applications yet.")}
              </EmptyMessage>)}
          </PanelBody>
        </Panel>
      </div>);
    };
    return ApiApplications;
}(AsyncView));
export default ApiApplications;
//# sourceMappingURL=index.jsx.map