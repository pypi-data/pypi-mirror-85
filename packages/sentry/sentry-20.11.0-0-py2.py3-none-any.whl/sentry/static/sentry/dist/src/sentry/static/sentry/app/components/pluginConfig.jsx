import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Button from 'app/components/button';
import LoadingIndicator from 'app/components/loadingIndicator';
import PluginIcon from 'app/plugins/components/pluginIcon';
import plugins from 'app/plugins';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var PluginConfig = /** @class */ (function (_super) {
    __extends(PluginConfig, _super);
    function PluginConfig() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: !plugins.isLoaded(_this.props.data),
            testResults: '',
        };
        _this.handleDisablePlugin = function () {
            _this.props.onDisablePlugin(_this.props.data);
        };
        _this.handleTestPlugin = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ testResults: '' });
                        addLoadingMessage(t('Sending test...'));
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(this.getPluginEndpoint(), {
                                method: 'POST',
                                data: {
                                    test: true,
                                },
                            })];
                    case 2:
                        data = _a.sent();
                        this.setState({ testResults: JSON.stringify(data.detail) });
                        addSuccessMessage(t('Test Complete!'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('An unexpected error occurred while testing your plugin. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    PluginConfig.prototype.componentDidMount = function () {
        this.loadPlugin(this.props.data);
    };
    PluginConfig.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        this.loadPlugin(nextProps.data);
    };
    PluginConfig.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return !isEqual(nextState, this.state) || !isEqual(nextProps.data, this.props.data);
    };
    PluginConfig.prototype.loadPlugin = function (data) {
        var _this = this;
        this.setState({
            loading: true,
        }, function () {
            plugins.load(data, function () {
                _this.setState({ loading: false });
            });
        });
    };
    PluginConfig.prototype.getPluginEndpoint = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, data = _a.data;
        return "/projects/" + organization.slug + "/" + project.slug + "/plugins/" + data.id + "/";
    };
    PluginConfig.prototype.createMarkup = function () {
        return { __html: this.props.data.doc };
    };
    PluginConfig.prototype.render = function () {
        var data = this.props.data;
        // If passed via props, use that value instead of from `data`
        var enabled = typeof this.props.enabled !== 'undefined' ? this.props.enabled : data.enabled;
        return (<Panel className={"plugin-config ref-plugin-config-" + data.id} data-test-id="plugin-config">
        <PanelHeader hasButtons>
          <PluginName>
            <StyledPluginIcon pluginId={data.id}/>
            <span>{data.name}</span>
          </PluginName>

          {data.canDisable && enabled && (<Actions>
              {data.isTestable && (<TestPluginButton onClick={this.handleTestPlugin} size="small">
                  {t('Test Plugin')}
                </TestPluginButton>)}
              <Button size="small" onClick={this.handleDisablePlugin}>
                {t('Disable')}
              </Button>
            </Actions>)}
        </PanelHeader>

        {data.status === 'beta' && (<PanelAlert type="warning">
            {t('This plugin is considered beta and may change in the future.')}
          </PanelAlert>)}

        {this.state.testResults !== '' && (<PanelAlert type="info">
            <strong>Test Results</strong>
            <div>{this.state.testResults}</div>
          </PanelAlert>)}

        <StyledPanelBody>
          <div dangerouslySetInnerHTML={this.createMarkup()}/>
          {this.state.loading ? (<LoadingIndicator />) : (plugins.get(data).renderSettings({
            organization: this.props.organization,
            project: this.props.project,
        }))}
        </StyledPanelBody>
      </Panel>);
    };
    PluginConfig.propTypes = {
        api: PropTypes.object,
        organization: PropTypes.object.isRequired,
        project: PropTypes.object.isRequired,
        data: PropTypes.object.isRequired,
        onDisablePlugin: PropTypes.func,
        enabled: PropTypes.bool,
    };
    PluginConfig.defaultProps = {
        onDisablePlugin: function () { },
    };
    return PluginConfig;
}(React.Component));
export { PluginConfig };
export default withApi(PluginConfig);
var PluginName = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n"])));
var StyledPluginIcon = styled(PluginIcon)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Actions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var TestPluginButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledPanelBody = styled(PanelBody)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", ";\n  padding-bottom: 0;\n"], ["\n  padding: ", ";\n  padding-bottom: 0;\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=pluginConfig.jsx.map