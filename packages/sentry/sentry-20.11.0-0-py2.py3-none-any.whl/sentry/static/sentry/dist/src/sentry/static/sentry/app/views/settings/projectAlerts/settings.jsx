import { __assign, __extends } from "tslib";
import React from 'react';
import { IconMail } from 'app/icons';
import { PanelAlert } from 'app/components/panels';
import { fields } from 'app/data/forms/projectAlerts';
import { t } from 'app/locale';
import AlertLink from 'app/components/alertLink';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import PluginList from 'app/components/pluginList';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import routeTitleGen from 'app/utils/routeTitle';
var Settings = /** @class */ (function (_super) {
    __extends(Settings, _super);
    function Settings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleEnablePlugin = function (plugin) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(function (p) {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return __assign(__assign({}, plugin), { enabled: true });
                    }),
                });
            });
        };
        _this.handleDisablePlugin = function (plugin) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    pluginList: ((_a = prevState.pluginList) !== null && _a !== void 0 ? _a : []).map(function (p) {
                        if (p.id !== plugin.id) {
                            return p;
                        }
                        return __assign(__assign({}, plugin), { enabled: false });
                    }),
                });
            });
        };
        return _this;
    }
    Settings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { project: null, pluginList: [] });
    };
    Settings.prototype.getProjectEndpoint = function (_a) {
        var orgId = _a.orgId, projectId = _a.projectId;
        return "/projects/" + orgId + "/" + projectId + "/";
    };
    Settings.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var projectEndpoint = this.getProjectEndpoint(params);
        return [
            ['project', projectEndpoint],
            ['pluginList', "/projects/" + orgId + "/" + projectId + "/plugins/"],
        ];
    };
    Settings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Alerts Settings'), projectId, false);
    };
    Settings.prototype.renderBody = function () {
        var _a = this.props, canEditRule = _a.canEditRule, organization = _a.organization, params = _a.params;
        var orgId = params.orgId;
        var _b = this.state, project = _b.project, pluginList = _b.pluginList;
        if (!project) {
            return null;
        }
        var projectEndpoint = this.getProjectEndpoint(params);
        return (<React.Fragment>
        <SettingsPageHeader title={t('Alerts Settings')} action={<Button to={{
            pathname: "/organizations/" + orgId + "/alerts/rules/",
            query: { project: project.id },
        }} size="small">
              {t('View Alert Rules')}
            </Button>}/>
        <PermissionAlert />
        <AlertLink to="/settings/account/notifications/" icon={<IconMail />}>
          {t('Looking to fine-tune your personal notification preferences? Visit your Account Settings')}
        </AlertLink>

        <Form saveOnBlur allowUndo initialData={{
            subjectTemplate: project.subjectTemplate,
            digestsMinDelay: project.digestsMinDelay,
            digestsMaxDelay: project.digestsMaxDelay,
        }} apiMethod="PUT" apiEndpoint={projectEndpoint}>
          <JsonForm disabled={!canEditRule} title={t('Email Settings')} fields={[fields.subjectTemplate]}/>

          <JsonForm title={t('Digests')} disabled={!canEditRule} fields={[fields.digestsMinDelay, fields.digestsMaxDelay]} renderHeader={function () { return (<PanelAlert type="info">
                {t('Sentry will automatically digest alerts sent by some services to avoid flooding your inbox with individual issue notifications. To control how frequently notifications are delivered, use the sliders below.')}
              </PanelAlert>); }}/>
        </Form>

        {canEditRule && (<PluginList organization={organization} project={project} pluginList={(pluginList !== null && pluginList !== void 0 ? pluginList : []).filter(function (p) { return p.type === 'notification' && p.hasConfiguration; })} onEnablePlugin={this.handleEnablePlugin} onDisablePlugin={this.handleDisablePlugin}/>)}
      </React.Fragment>);
    };
    return Settings;
}(AsyncView));
export default Settings;
//# sourceMappingURL=settings.jsx.map