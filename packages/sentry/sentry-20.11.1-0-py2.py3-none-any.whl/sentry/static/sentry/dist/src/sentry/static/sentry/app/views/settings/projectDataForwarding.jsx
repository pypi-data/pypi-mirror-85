import { __assign, __extends, __read } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ExternalLink from 'app/components/links/externalLink';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { IconInfo } from 'app/icons';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import PluginList from 'app/components/pluginList';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import MiniBarChart from 'app/components/charts/miniBarChart';
import TextBlock from 'app/views/settings/components/text/textBlock';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
var DataForwardingStats = /** @class */ (function (_super) {
    __extends(DataForwardingStats, _super);
    function DataForwardingStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DataForwardingStats.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var options = {
            query: {
                since: since,
                until: until,
                resolution: '1d',
                stat: 'forwarded',
            },
        };
        return [['stats', "/projects/" + orgId + "/" + projectId + "/stats/", options]];
    };
    DataForwardingStats.prototype.renderBody = function () {
        var projectId = this.props.params.projectId;
        var stats = this.state.stats;
        var series = {
            seriesName: t('Forwarded'),
            data: stats.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
                return ({ name: timestamp * 1000, value: value });
            }),
        };
        var forwardedAny = series.data.some(function (_a) {
            var value = _a.value;
            return value > 0;
        });
        return (<Panel>
        <SentryDocumentTitle title={t('Data Forwarding')} objSlug={projectId}/>
        <PanelHeader>{t('Forwarded events in the last 30 days (by day)')}</PanelHeader>
        <PanelBody withPadding>
          {forwardedAny ? (<MiniBarChart isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<EmptyMessage title={t('Nothing forwarded in the last 30 days.')} description={t('Total events forwarded to third party integrations.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return DataForwardingStats;
}(AsyncComponent));
var ProjectDataForwarding = /** @class */ (function (_super) {
    __extends(ProjectDataForwarding, _super);
    function ProjectDataForwarding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onEnablePlugin = function (plugin) { return _this.updatePlugin(plugin, true); };
        _this.onDisablePlugin = function (plugin) { return _this.updatePlugin(plugin, false); };
        return _this;
    }
    ProjectDataForwarding.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['plugins', "/projects/" + orgId + "/" + projectId + "/plugins/"]];
    };
    Object.defineProperty(ProjectDataForwarding.prototype, "forwardingPlugins", {
        get: function () {
            return this.state.plugins.filter(function (p) { return p.type === 'data-forwarding' && p.hasConfiguration; });
        },
        enumerable: false,
        configurable: true
    });
    ProjectDataForwarding.prototype.updatePlugin = function (plugin, enabled) {
        var plugins = this.state.plugins.map(function (p) { return (__assign(__assign({}, p), { enabled: p.id === plugin.id ? enabled : p.enabled })); });
        this.setState({ plugins: plugins });
    };
    ProjectDataForwarding.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, project = _a.project;
        var plugins = this.forwardingPlugins;
        var hasAccess = organization.access.includes('project:write');
        var pluginsPanel = plugins.length > 0 ? (<PluginList organization={organization} project={project} pluginList={plugins} onEnablePlugin={this.onEnablePlugin} onDisablePlugin={this.onDisablePlugin}/>) : (<Panel>
          <EmptyMessage title={t('There are no integrations available for data forwarding')}/>
        </Panel>);
        return (<div data-test-id="data-forwarding-settings">
        <Feature features={['projects:data-forwarding']} hookName="feature-disabled:data-forwarding">
          {function (_a) {
            var hasFeature = _a.hasFeature, features = _a.features;
            return (<React.Fragment>
              <SettingsPageHeader title={t('Data Forwarding')}/>
              <TextBlock>
                {tct("Data Forwarding allows processed events to be sent to your\n                favorite business intelligence tools. The exact payload and\n                types of data depend on the integration you're using. Learn\n                more about this functionality in our [link:documentation].", {
                link: (<ExternalLink href="https://docs.sentry.io/learn/data-forwarding/"/>),
            })}
              </TextBlock>
              <PermissionAlert />

              <Alert icon={<IconInfo size="md"/>}>
                {tct("Sentry forwards [em:all applicable events] to the provider, in\n                some cases this may be a significant volume of data.", {
                em: <strong />,
            })}
              </Alert>

              {!hasFeature && (<FeatureDisabled alert featureName="Data Forwarding" features={features}/>)}

              <DataForwardingStats params={params}/>
              {hasAccess && hasFeature && pluginsPanel}
            </React.Fragment>);
        }}
        </Feature>
      </div>);
    };
    return ProjectDataForwarding;
}(AsyncComponent));
export default withProject(withOrganization(ProjectDataForwarding));
//# sourceMappingURL=projectDataForwarding.jsx.map