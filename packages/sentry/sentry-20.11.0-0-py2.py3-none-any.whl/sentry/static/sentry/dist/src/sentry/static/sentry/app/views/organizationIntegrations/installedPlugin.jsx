import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Alert from 'app/components/alert';
import { IconDelete, IconFlag, IconSettings } from 'app/icons';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import withApi from 'app/utils/withApi';
import { addErrorMessage, addSuccessMessage, addLoadingMessage, } from 'app/actionCreators/indicator';
import space from 'app/styles/space';
import Switch from 'app/components/switch';
var InstalledPlugin = /** @class */ (function (_super) {
    __extends(InstalledPlugin, _super);
    function InstalledPlugin() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pluginUpdate = function (data, method) {
            if (method === void 0) { method = 'POST'; }
            return __awaiter(_this, void 0, void 0, function () {
                var _a, organization, projectItem, plugin;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.props, organization = _a.organization, projectItem = _a.projectItem, plugin = _a.plugin;
                            // no try/catch so the caller will have to have it
                            return [4 /*yield*/, this.props.api.requestPromise("/projects/" + organization.slug + "/" + projectItem.projectSlug + "/plugins/" + plugin.id + "/", {
                                    method: method,
                                    data: data,
                                })];
                        case 1:
                            // no try/catch so the caller will have to have it
                            _b.sent();
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.updatePluginEnableStatus = function (enabled) { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!enabled) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.pluginUpdate({ enabled: enabled })];
                    case 1:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, this.pluginUpdate({}, 'DELETE')];
                    case 3:
                        _a.sent();
                        _a.label = 4;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleReset = function () { return __awaiter(_this, void 0, void 0, function () {
            var _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        addLoadingMessage(t('Removing...'));
                        return [4 /*yield*/, this.pluginUpdate({ reset: true })];
                    case 1:
                        _a.sent();
                        addSuccessMessage(t('Configuration was removed'));
                        this.props.onResetConfiguration(this.projectId);
                        this.props.trackIntegrationEvent({
                            eventKey: 'integrations.uninstall_completed',
                            eventName: 'Integrations: Uninstall Completed',
                            project_id: this.projectId,
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Unable to remove configuration'));
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.handleUninstallClick = function () {
            _this.props.trackIntegrationEvent({
                eventKey: 'integrations.uninstall_clicked',
                eventName: 'Integrations: Uninstall Clicked',
                project_id: _this.projectId,
            });
        };
        _this.toggleEnablePlugin = function (projectId, status) {
            if (status === void 0) { status = true; }
            return __awaiter(_this, void 0, void 0, function () {
                var _err_2;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            addLoadingMessage(t('Enabling...'));
                            return [4 /*yield*/, this.updatePluginEnableStatus(status)];
                        case 1:
                            _a.sent();
                            addSuccessMessage(status ? t('Configuration was enabled.') : t('Configuration was disabled.'));
                            this.props.onPluginEnableStatusChange(projectId, status);
                            this.props.trackIntegrationEvent({
                                eventKey: status ? 'integrations.enabled' : 'integrations.disabled',
                                eventName: status ? 'Integrations: Enabled' : 'Integrations: Disabled',
                                project_id: projectId,
                            });
                            return [3 /*break*/, 3];
                        case 2:
                            _err_2 = _a.sent();
                            addErrorMessage(status
                                ? t('Unable to enable configuration.')
                                : t('Unable to disable configuration.'));
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    Object.defineProperty(InstalledPlugin.prototype, "projectId", {
        get: function () {
            return this.props.projectItem.projectId;
        },
        enumerable: false,
        configurable: true
    });
    InstalledPlugin.prototype.getConfirmMessage = function () {
        return (<React.Fragment>
        <Alert type="error" icon={<IconFlag size="md"/>}>
          {t('Deleting this installation will disable the integration for this project and remove any configurations.')}
        </Alert>
      </React.Fragment>);
    };
    Object.defineProperty(InstalledPlugin.prototype, "projectForBadge", {
        get: function () {
            //this function returns the project as needed for the ProjectBadge component
            var projectItem = this.props.projectItem;
            return {
                slug: projectItem.projectSlug,
                platform: projectItem.projectPlatform ? projectItem.projectPlatform : undefined,
            };
        },
        enumerable: false,
        configurable: true
    });
    InstalledPlugin.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, plugin = _a.plugin, organization = _a.organization, projectItem = _a.projectItem;
        return (<Container>
        <Access access={['org:integrations']}>
          {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<IntegrationFlex className={className}>
              <IntegrationItemBox>
                <ProjectBadge project={_this.projectForBadge}/>
              </IntegrationItemBox>
              <div>
                {<StyledButton borderless icon={<IconSettings />} disabled={!hasAccess} to={"/settings/" + organization.slug + "/projects/" + projectItem.projectSlug + "/plugins/" + plugin.id + "/"} data-test-id="integration-configure-button">
                    {t('Configure')}
                  </StyledButton>}
              </div>
              <div>
                <Confirm priority="danger" onConfirming={_this.handleUninstallClick} disabled={!hasAccess} confirmText="Delete Installation" onConfirm={function () { return _this.handleReset(); }} message={_this.getConfirmMessage()}>
                  <StyledButton disabled={!hasAccess} borderless icon={<IconDelete />} data-test-id="integration-remove-button">
                    {t('Uninstall')}
                  </StyledButton>
                </Confirm>
              </div>
              <Switch isActive={projectItem.enabled} toggle={function () {
                return _this.toggleEnablePlugin(projectItem.projectId, !projectItem.enabled);
            }} isDisabled={!hasAccess}/>
            </IntegrationFlex>);
        }}
        </Access>
      </Container>);
    };
    return InstalledPlugin;
}(React.Component));
export { InstalledPlugin };
export default withApi(InstalledPlugin);
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; });
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var IntegrationFlex = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationItemBox = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: row;\n  min-width: 0;\n"], ["\n  flex: 1;\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: row;\n  min-width: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=installedPlugin.jsx.map