import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Panel, PanelAlert, PanelBody, PanelHeader, PanelItem, } from 'app/components/panels';
import { t, tct } from 'app/locale';
import Access from 'app/components/acl/access';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import RouteError from 'app/views/routeError';
import SentryTypes from 'app/sentryTypes';
import ProjectPluginRow from './projectPluginRow';
var ProjectPlugins = /** @class */ (function (_super) {
    __extends(ProjectPlugins, _super);
    function ProjectPlugins() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectPlugins.prototype.render = function () {
        var _a = this.props, plugins = _a.plugins, loading = _a.loading, error = _a.error, onChange = _a.onChange, routes = _a.routes, params = _a.params;
        var orgId = this.props.params.orgId;
        var hasError = error;
        var isLoading = !hasError && loading;
        if (hasError) {
            return <RouteError error={error}/>;
        }
        if (isLoading) {
            return <LoadingIndicator />;
        }
        return (<Panel>
        <PanelHeader>
          <div>{t('Legacy Integration')}</div>
          <div>{t('Enabled')}</div>
        </PanelHeader>
        <PanelBody>
          <PanelAlert type="warning">
            <Access access={['org:integrations']}>
              {function (_a) {
            var hasAccess = _a.hasAccess;
            return hasAccess
                ? tct("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available. Visit the [link:organization integrations] settings to manage them.", {
                    link: <Link to={"/settings/" + orgId + "/integrations"}/>,
                })
                : t("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available.");
        }}
            </Access>
          </PanelAlert>

          {plugins
            .filter(function (p) {
            return !p.isHidden;
        })
            .map(function (plugin) { return (<PanelItem key={plugin.id}>
                <ProjectPluginRow params={params} routes={routes} {...plugin} onChange={onChange}/>
              </PanelItem>); })}
        </PanelBody>
      </Panel>);
    };
    ProjectPlugins.propTypes = {
        plugins: PropTypes.arrayOf(SentryTypes.PluginShape),
        loading: PropTypes.bool,
        error: PropTypes.any,
        onChange: PropTypes.func,
        onError: PropTypes.func,
        routes: PropTypes.array,
    };
    return ProjectPlugins;
}(Component));
export default ProjectPlugins;
//# sourceMappingURL=projectPlugins.jsx.map