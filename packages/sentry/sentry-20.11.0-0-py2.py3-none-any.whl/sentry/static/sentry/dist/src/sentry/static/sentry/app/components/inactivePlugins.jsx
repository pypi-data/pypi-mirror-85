import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import PluginIcon from 'app/plugins/components/pluginIcon';
import TextOverflow from 'app/components/textOverflow';
import space from 'app/styles/space';
var InactivePlugins = function (_a) {
    var plugins = _a.plugins, onEnablePlugin = _a.onEnablePlugin;
    if (plugins.length === 0) {
        return null;
    }
    return (<Panel>
      <PanelHeader>{t('Inactive Integrations')}</PanelHeader>

      <PanelBody>
        <Plugins>
          {plugins.map(function (plugin) { return (<IntegrationButton key={plugin.id} onClick={function () { return onEnablePlugin(plugin); }} className={"ref-plugin-enable-" + plugin.id}>
              <Label>
                <StyledPluginIcon pluginId={plugin.id}/>
                <TextOverflow>{plugin.shortName || plugin.name}</TextOverflow>
              </Label>
            </IntegrationButton>); })}
        </Plugins>
      </PanelBody>
    </Panel>);
};
var Plugins = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  padding: ", ";\n  flex: 1;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  padding: ", ";\n  flex: 1;\n  flex-wrap: wrap;\n"])), space(1));
var IntegrationButton = styled('button')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", ";\n  width: 175px;\n  text-align: center;\n  font-size: ", ";\n  color: #889ab0;\n  letter-spacing: 0.1px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border: 1px solid #eee;\n  background: inherit;\n  border-radius: ", ";\n  padding: 10px;\n\n  &:hover {\n    border-color: #ccc;\n  }\n"], ["\n  margin: ", ";\n  width: 175px;\n  text-align: center;\n  font-size: ", ";\n  color: #889ab0;\n  letter-spacing: 0.1px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border: 1px solid #eee;\n  background: inherit;\n  border-radius: ", ";\n  padding: 10px;\n\n  &:hover {\n    border-color: #ccc;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.borderRadius; });
var Label = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var StyledPluginIcon = styled(PluginIcon)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
export default InactivePlugins;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=inactivePlugins.jsx.map