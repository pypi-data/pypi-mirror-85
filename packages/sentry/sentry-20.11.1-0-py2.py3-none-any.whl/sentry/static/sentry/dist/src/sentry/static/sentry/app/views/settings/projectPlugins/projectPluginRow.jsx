import { __assign, __extends, __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import { Link } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ExternalLink from 'app/components/links/externalLink';
import Access from 'app/components/acl/access';
import PluginIcon from 'app/plugins/components/pluginIcon';
import SentryTypes from 'app/sentryTypes';
import Switch from 'app/components/switch';
import getDynamicText from 'app/utils/getDynamicText';
import recreateRoute from 'app/utils/recreateRoute';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
var grayText = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: #979ba0;\n"], ["\n  color: #979ba0;\n"])));
var ProjectPluginRow = /** @class */ (function (_super) {
    __extends(ProjectPluginRow, _super);
    function ProjectPluginRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function () {
            var _a = _this.props, onChange = _a.onChange, id = _a.id, enabled = _a.enabled;
            onChange(id, !enabled);
            var eventKey = !enabled ? 'integrations.enabled' : 'integrations.disabled';
            var eventName = !enabled ? 'Integrations: Enabled' : 'Integrations: Disabled';
            trackIntegrationEvent({
                eventKey: eventKey,
                eventName: eventName,
                integration: id,
                integration_type: 'plugin',
                view: 'legacy_integrations',
                project_id: _this.props.project.id,
            }, _this.props.organization);
        };
        return _this;
    }
    ProjectPluginRow.prototype.render = function () {
        var _this = this;
        var _a = this.props, id = _a.id, name = _a.name, slug = _a.slug, version = _a.version, author = _a.author, hasConfiguration = _a.hasConfiguration, enabled = _a.enabled, canDisable = _a.canDisable;
        var configureUrl = recreateRoute(id, this.props);
        return (<Access access={['project:write']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            var LinkOrSpan = hasAccess ? Link : 'span';
            return (<PluginItem key={id} className={slug}>
              <PluginInfo>
                <StyledPluginIcon size={48} pluginId={id}/>
                <PluginDescription>
                  <PluginName>
                    {name + " "}
                    {getDynamicText({
                value: (<Version>{version ? "v" + version : <em>{t('n/a')}</em>}</Version>),
                fixed: <Version>v10</Version>,
            })}
                  </PluginName>
                  <div>
                    {author && (<ExternalLink css={grayText} href={author.url}>
                        {author.name}
                      </ExternalLink>)}
                    {hasConfiguration && (<span>
                        {' '}
                        &middot;{' '}
                        <LinkOrSpan css={grayText} to={configureUrl}>
                          {t('Configure plugin')}
                        </LinkOrSpan>
                      </span>)}
                  </div>
                </PluginDescription>
              </PluginInfo>
              <Switch size="lg" isDisabled={!hasAccess || !canDisable} isActive={enabled} toggle={_this.handleChange}/>
            </PluginItem>);
        }}
      </Access>);
    };
    ProjectPluginRow.propTypes = __assign(__assign({}, SentryTypes.Plugin), { onChange: PropTypes.func });
    return ProjectPluginRow;
}(React.PureComponent));
export default withOrganization(withProject(ProjectPluginRow));
var PluginItem = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var PluginDescription = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n"], ["\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n"])));
var PluginInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  line-height: 24px;\n"], ["\n  display: flex;\n  flex: 1;\n  line-height: 24px;\n"])));
var PluginName = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 16px;\n"], ["\n  font-size: 16px;\n"])));
var StyledPluginIcon = styled(PluginIcon)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: 16px;\n"], ["\n  margin-right: 16px;\n"])));
// Keeping these colors the same from old integrations page
var Version = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: #babec2;\n"], ["\n  color: #babec2;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=projectPluginRow.jsx.map