import PropTypes from 'prop-types';
import React from 'react';
import { enablePlugin, disablePlugin } from 'app/actionCreators/plugins';
import InactivePlugins from 'app/components/inactivePlugins';
import PluginConfig from 'app/components/pluginConfig';
import { t } from 'app/locale';
import { Panel, PanelItem } from './panels';
var PluginList = function (_a) {
    var organization = _a.organization, project = _a.project, pluginList = _a.pluginList, _b = _a.onDisablePlugin, onDisablePlugin = _b === void 0 ? function () { } : _b, _c = _a.onEnablePlugin, onEnablePlugin = _c === void 0 ? function () { } : _c;
    var handleEnablePlugin = function (plugin) {
        enablePlugin({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onEnablePlugin(plugin);
    };
    var handleDisablePlugin = function (plugin) {
        disablePlugin({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onDisablePlugin(plugin);
    };
    if (!pluginList.length) {
        return (<Panel>
        <PanelItem>
          {t("Oops! Looks like there aren't any available integrations installed.")}
        </PanelItem>
      </Panel>);
    }
    return (<div>
      {pluginList
        .filter(function (p) { return p.enabled; })
        .map(function (data) { return (<PluginConfig data={data} organization={organization} project={project} key={data.id} onDisablePlugin={handleDisablePlugin}/>); })}

      <InactivePlugins plugins={pluginList.filter(function (p) { return !p.enabled && !p.isHidden; })} onEnablePlugin={handleEnablePlugin}/>
    </div>);
};
PluginList.propTypes = {
    organization: PropTypes.object.isRequired,
    project: PropTypes.object.isRequired,
    pluginList: PropTypes.array.isRequired,
    onDisablePlugin: PropTypes.func,
    onEnablePlugin: PropTypes.func,
};
export default PluginList;
//# sourceMappingURL=pluginList.jsx.map