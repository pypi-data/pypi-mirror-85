import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as modal from 'app/actionCreators/modal';
import Button from 'app/components/button';
import ContextPickerModal from 'app/components/contextPickerModal';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import AbstractIntegrationDetailedView from './abstractIntegrationDetailedView';
import InstalledPlugin from './installedPlugin';
var PluginDetailedView = /** @class */ (function (_super) {
    __extends(PluginDetailedView, _super);
    function PluginDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleResetConfiguration = function (projectId) {
            //make a copy of our project list
            var projectList = _this.plugin.projectList.slice();
            //find the index of the project
            var index = projectList.findIndex(function (item) { return item.projectId === projectId; });
            //should match but quit if it doesn't
            if (index < 0) {
                return;
            }
            //remove from array
            projectList.splice(index, 1);
            //update state
            _this.setState({
                plugins: [__assign(__assign({}, _this.state.plugins[0]), { projectList: projectList })],
            });
        };
        _this.handlePluginEnableStatus = function (projectId, enable) {
            if (enable === void 0) { enable = true; }
            //make a copy of our project list
            var projectList = _this.plugin.projectList.slice();
            //find the index of the project
            var index = projectList.findIndex(function (item) { return item.projectId === projectId; });
            //should match but quit if it doesn't
            if (index < 0) {
                return;
            }
            //update item in array
            projectList[index] = __assign(__assign({}, projectList[index]), { enabled: enable });
            //update state
            _this.setState({
                plugins: [__assign(__assign({}, _this.state.plugins[0]), { projectList: projectList })],
            });
        };
        _this.handleAddToProject = function () {
            var plugin = _this.plugin;
            var _a = _this.props, organization = _a.organization, router = _a.router;
            _this.trackIntegrationEvent({
                eventKey: 'integrations.plugin_add_to_project_clicked',
                eventName: 'Integrations: Plugin Add to Project Clicked',
            });
            modal.openModal(function (modalProps) { return (<ContextPickerModal {...modalProps} nextPath={"/settings/" + organization.slug + "/projects/:projectId/plugins/" + plugin.id + "/"} needProject needOrg={false} onFinish={function (path) {
                modalProps.closeModal();
                router.push(path);
            }}/>); }, {});
        };
        return _this;
    }
    PluginDetailedView.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, integrationSlug = _a.integrationSlug;
        return [
            ['plugins', "/organizations/" + orgId + "/plugins/configs/?plugins=" + integrationSlug],
        ];
    };
    Object.defineProperty(PluginDetailedView.prototype, "integrationType", {
        get: function () {
            return 'plugin';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "plugin", {
        get: function () {
            return this.state.plugins[0];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "description", {
        get: function () {
            return this.plugin.description || '';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "author", {
        get: function () {
            var _a;
            return (_a = this.plugin.author) === null || _a === void 0 ? void 0 : _a.name;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "resourceLinks", {
        get: function () {
            return this.plugin.resourceLinks || [];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "installationStatus", {
        get: function () {
            return this.plugin.projectList.length > 0 ? 'Installed' : 'Not Installed';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "integrationName", {
        get: function () {
            return "" + this.plugin.name + (this.plugin.isHidden ? ' (Legacy)' : '');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(PluginDetailedView.prototype, "featureData", {
        get: function () {
            return this.plugin.featureDescriptions;
        },
        enumerable: false,
        configurable: true
    });
    PluginDetailedView.prototype.getTabDisplay = function (tab) {
        //we want to show project configurations to make it more clear
        if (tab === 'configurations') {
            return 'project configurations';
        }
        return 'overview';
    };
    PluginDetailedView.prototype.renderTopButton = function (disabledFromFeatures, userHasAccess) {
        if (userHasAccess) {
            return (<AddButton data-test-id="install-button" disabled={disabledFromFeatures} onClick={this.handleAddToProject} size="small" priority="primary">
          {t('Add to Project')}
        </AddButton>);
        }
        return this.renderRequestIntegrationButton();
    };
    PluginDetailedView.prototype.renderConfigurations = function () {
        var _this = this;
        var plugin = this.plugin;
        var organization = this.props.organization;
        if (plugin.projectList.length) {
            return (<div>
          {plugin.projectList.map(function (projectItem) { return (<InstalledPlugin key={projectItem.projectId} organization={organization} plugin={plugin} projectItem={projectItem} onResetConfiguration={_this.handleResetConfiguration} onPluginEnableStatusChange={_this.handlePluginEnableStatus} trackIntegrationEvent={_this.trackIntegrationEvent}/>); })}
        </div>);
        }
        return this.renderEmptyConfigurations();
    };
    return PluginDetailedView;
}(AbstractIntegrationDetailedView));
var AddButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default withOrganization(PluginDetailedView);
var templateObject_1;
//# sourceMappingURL=pluginDetailedView.jsx.map