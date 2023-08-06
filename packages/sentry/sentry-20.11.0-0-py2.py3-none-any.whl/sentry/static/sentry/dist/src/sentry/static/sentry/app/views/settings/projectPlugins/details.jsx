import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { disablePlugin, enablePlugin } from 'app/actionCreators/plugins';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import PluginConfig from 'app/components/pluginConfig';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withPlugins from 'app/utils/withPlugins';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import space from 'app/styles/space';
/**
 * There are currently two sources of truths for plugin details:
 *
 * 1) PluginsStore has a list of plugins, and this is where ENABLED state lives
 * 2) We fetch "plugin details" via API and save it to local state as `pluginDetails`.
 *    This is because "details" call contains form `config` and the "list" endpoint does not.
 *    The more correct way would be to pass `config` to PluginConfig and use plugin from
 *    PluginsStore
 */
var ProjectPluginDetails = /** @class */ (function (_super) {
    __extends(ProjectPluginDetails, _super);
    function ProjectPluginDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleReset = function () {
            var _a = _this.props.params, projectId = _a.projectId, orgId = _a.orgId, pluginId = _a.pluginId;
            addLoadingMessage(t('Saving changes\u2026'));
            trackIntegrationEvent({
                eventKey: 'integrations.uninstall_clicked',
                eventName: 'Integrations: Uninstall Clicked',
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
                project_id: _this.props.project.id,
            }, _this.props.organization);
            _this.api.request("/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/", {
                method: 'POST',
                data: { reset: true },
                success: function (pluginDetails) {
                    _this.setState({ pluginDetails: pluginDetails });
                    addSuccessMessage(t('Plugin was reset'));
                    trackIntegrationEvent({
                        eventKey: 'integrations.uninstall_completed',
                        eventName: 'Integrations: Uninstall Completed',
                        integration: pluginId,
                        integration_type: 'plugin',
                        view: 'plugin_details',
                        project_id: _this.props.project.id,
                    }, _this.props.organization);
                },
                error: function () {
                    addErrorMessage(t('An error occurred'));
                },
            });
        };
        _this.handleEnable = function () {
            enablePlugin(_this.props.params);
            _this.analyticsChangeEnableStatus(true);
        };
        _this.handleDisable = function () {
            disablePlugin(_this.props.params);
            _this.analyticsChangeEnableStatus(false);
        };
        _this.analyticsChangeEnableStatus = function (enabled) {
            var pluginId = _this.props.params.pluginId;
            var eventKey = enabled ? 'integrations.enabled' : 'integrations.disabled';
            var eventName = enabled ? 'Integrations: Enabled' : 'Integrations: Disabled';
            trackIntegrationEvent({
                eventKey: eventKey,
                eventName: eventName,
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
                project_id: _this.props.project.id,
            }, _this.props.organization);
        };
        return _this;
    }
    ProjectPluginDetails.prototype.componentDidUpdate = function (prevProps, prevContext) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
        if (prevProps.params.pluginId !== this.props.params.pluginId) {
            this.recordDetailsViewed();
        }
    };
    ProjectPluginDetails.prototype.componentDidMount = function () {
        this.recordDetailsViewed();
    };
    ProjectPluginDetails.prototype.recordDetailsViewed = function () {
        var pluginId = this.props.params.pluginId;
        trackIntegrationEvent({
            eventKey: 'integrations.details_viewed',
            eventName: 'Integrations: Details Viewed',
            integration: pluginId,
            integration_type: 'plugin',
            view: 'plugin_details',
            project_id: this.props.project.id,
        }, this.props.organization);
    };
    ProjectPluginDetails.prototype.getTitle = function () {
        var plugin = this.state.plugin;
        if (plugin && plugin.name) {
            return plugin.name;
        }
        else {
            return 'Sentry';
        }
    };
    ProjectPluginDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, projectId = _a.projectId, orgId = _a.orgId, pluginId = _a.pluginId;
        return [['pluginDetails', "/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/"]];
    };
    ProjectPluginDetails.prototype.trimSchema = function (value) {
        return value.split('//')[1];
    };
    // Enabled state is handled via PluginsStore and not via plugins detail
    ProjectPluginDetails.prototype.getEnabled = function () {
        var _this = this;
        var pluginDetails = this.state.pluginDetails;
        var plugins = this.props.plugins;
        var plugin = plugins &&
            plugins.plugins &&
            plugins.plugins.find(function (_a) {
                var slug = _a.slug;
                return slug === _this.props.params.pluginId;
            });
        return plugin ? plugin.enabled : pluginDetails && pluginDetails.enabled;
    };
    ProjectPluginDetails.prototype.renderActions = function () {
        var pluginDetails = this.state.pluginDetails;
        if (!pluginDetails) {
            return null;
        }
        var enabled = this.getEnabled();
        var enable = (<StyledButton size="small" onClick={this.handleEnable}>
        {t('Enable Plugin')}
      </StyledButton>);
        var disable = (<StyledButton size="small" priority="danger" onClick={this.handleDisable}>
        {t('Disable Plugin')}
      </StyledButton>);
        var toggleEnable = enabled ? disable : enable;
        return (<div className="pull-right">
        {pluginDetails.canDisable && toggleEnable}
        <Button size="small" onClick={this.handleReset}>
          {t('Reset Configuration')}
        </Button>
      </div>);
    };
    ProjectPluginDetails.prototype.renderBody = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, project = _c.project;
        var pluginDetails = this.state.pluginDetails;
        if (!pluginDetails) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={pluginDetails.name} action={this.renderActions()}/>
        <div className="row">
          <div className="col-md-7">
            <PluginConfig organization={organization} project={project} data={pluginDetails} enabled={this.getEnabled()} onDisablePlugin={this.handleDisable}/>
          </div>
          <div className="col-md-4 col-md-offset-1">
            <div className="pluginDetails-meta">
              <h4>{t('Plugin Information')}</h4>

              <dl className="flat">
                <dt>{t('Name')}</dt>
                <dd>{pluginDetails.name}</dd>
                <dt>{t('Author')}</dt>
                <dd>{(_a = pluginDetails.author) === null || _a === void 0 ? void 0 : _a.name}</dd>
                {((_b = pluginDetails.author) === null || _b === void 0 ? void 0 : _b.url) && (<div>
                    <dt>{t('URL')}</dt>
                    <dd>
                      <ExternalLink href={pluginDetails.author.url}>
                        {this.trimSchema(pluginDetails.author.url)}
                      </ExternalLink>
                    </dd>
                  </div>)}
                <dt>{t('Version')}</dt>
                <dd>{pluginDetails.version}</dd>
              </dl>

              {pluginDetails.description && (<div>
                  <h4>{t('Description')}</h4>
                  <p className="description">{pluginDetails.description}</p>
                </div>)}

              {pluginDetails.resourceLinks && (<div>
                  <h4>{t('Resources')}</h4>
                  <dl className="flat">
                    {pluginDetails.resourceLinks.map(function (_a) {
            var title = _a.title, url = _a.url;
            return (<dd key={url}>
                        <ExternalLink href={url}>{title}</ExternalLink>
                      </dd>);
        })}
                  </dl>
                </div>)}
            </div>
          </div>
        </div>
      </div>);
    };
    return ProjectPluginDetails;
}(AsyncView));
export { ProjectPluginDetails };
export default withPlugins(ProjectPluginDetails);
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.75));
var templateObject_1;
//# sourceMappingURL=details.jsx.map