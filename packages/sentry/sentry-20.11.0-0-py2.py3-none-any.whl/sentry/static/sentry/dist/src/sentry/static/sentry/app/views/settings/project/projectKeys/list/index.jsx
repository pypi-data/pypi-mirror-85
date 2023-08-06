import { __assign, __awaiter, __extends, __generator, __read, __spread } from "tslib";
import React from 'react';
import { addLoadingMessage, addErrorMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { Panel } from 'app/components/panels';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ExternalLink from 'app/components/links/externalLink';
import Pagination from 'app/components/pagination';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import { IconAdd, IconFlag } from 'app/icons';
import KeyRow from './keyRow';
var ProjectKeys = /** @class */ (function (_super) {
    __extends(ProjectKeys, _super);
    function ProjectKeys() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Optimistically remove key
         */
        _this.handleRemoveKey = function (data) { return __awaiter(_this, void 0, void 0, function () {
            var oldKeyList, _a, orgId, projectId, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeyList = __spread(this.state.keyList);
                        addLoadingMessage(t('Revoking key\u2026'));
                        this.setState(function (state) { return ({
                            keyList: state.keyList.filter(function (key) { return key.id !== data.id; }),
                        }); });
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + data.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(t('Revoked key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({
                            keyList: oldKeyList,
                        });
                        addErrorMessage(t('Unable to revoke key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleToggleKey = function (isActive, data) { return __awaiter(_this, void 0, void 0, function () {
            var oldKeyList, _a, orgId, projectId, _err_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeyList = __spread(this.state.keyList);
                        addLoadingMessage(t('Saving changes\u2026'));
                        this.setState(function (state) {
                            var keyList = state.keyList.map(function (key) {
                                if (key.id === data.id) {
                                    return __assign(__assign({}, key), { isActive: !data.isActive });
                                }
                                return key;
                            });
                            return { keyList: keyList };
                        });
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + data.id + "/", {
                                method: 'PUT',
                                data: { isActive: isActive },
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(isActive ? t('Enabled key') : t('Disabled key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _b.sent();
                        addErrorMessage(isActive ? t('Error enabling key') : t('Error disabling key'));
                        this.setState({ keyList: oldKeyList });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCreateKey = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectId, data_1, _err_3;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/", {
                                method: 'POST',
                            })];
                    case 2:
                        data_1 = _b.sent();
                        this.setState(function (state) { return ({
                            keyList: __spread(state.keyList, [data_1]),
                        }); });
                        addSuccessMessage(t('Created a new key.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_3 = _b.sent();
                        addErrorMessage(t('Unable to create new key. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectKeys.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Client Keys'), projectId, false);
    };
    ProjectKeys.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectKeys.prototype.renderEmpty = function () {
        return (<Panel>
        <EmptyMessage icon={<IconFlag size="xl"/>} description={t('There are no keys active for this project.')}/>
      </Panel>);
    };
    ProjectKeys.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, routes = _a.routes, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var access = new Set(organization.access);
        return (<React.Fragment>
        {this.state.keyList.map(function (key) { return (<KeyRow api={_this.api} access={access} key={key.id} orgId={orgId} projectId={"" + projectId} data={key} onToggle={_this.handleToggleKey} onRemove={_this.handleRemoveKey} routes={routes} location={location} params={params}/>); })}
        <Pagination pageLinks={this.state.keyListPageLinks}/>
      </React.Fragment>);
    };
    ProjectKeys.prototype.renderBody = function () {
        var access = new Set(this.props.organization.access);
        var isEmpty = !this.state.keyList.length;
        return (<div data-test-id="project-keys">
        <SettingsPageHeader title={t('Client Keys')} action={access.has('project:write') ? (<Button onClick={this.handleCreateKey} size="small" priority="primary" icon={<IconAdd size="xs" isCircled/>}>
                {t('Generate New Key')}
              </Button>) : null}/>
        <TextBlock>
          {tct("To send data to Sentry you will need to configure an SDK with a client key\n          (usually referred to as the [code:SENTRY_DSN] value). For more\n          information on integrating Sentry with your application take a look at our\n          [link:documentation].", {
            link: <ExternalLink href="https://docs.sentry.io/"/>,
            code: <code />,
        })}
        </TextBlock>

        {isEmpty ? this.renderEmpty() : this.renderResults()}
      </div>);
    };
    return ProjectKeys;
}(AsyncView));
export default withOrganization(withProject(ProjectKeys));
//# sourceMappingURL=index.jsx.map