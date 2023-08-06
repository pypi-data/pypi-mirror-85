import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { Client } from 'app/api';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import Button from 'app/components/button';
import { openModal } from 'app/actionCreators/modal';
import Edit from './modals/edit';
import Add from './modals/add';
import OrganizationRules from './organizationRules';
import convertRelayPiiConfig from './convertRelayPiiConfig';
import submitRules from './submitRules';
import Content from './content';
var ADVANCED_DATASCRUBBING_LINK = 'https://docs.sentry.io/data-management/advanced-datascrubbing/';
var DataScrubbing = /** @class */ (function (_super) {
    __extends(DataScrubbing, _super);
    function DataScrubbing() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rules: [],
            savedRules: [],
            relayPiiConfig: _this.props.relayPiiConfig,
            orgRules: [],
        };
        _this.api = new Client();
        _this.handleOpenAddModal = function () {
            var rules = _this.state.rules;
            openModal(function (modalProps) { return (<Add {...modalProps} projectId={_this.props.projectId} savedRules={rules} api={_this.api} endpoint={_this.props.endpoint} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully added data scrubbing rule'));
            }}/>); });
        };
        _this.handleOpenEditModal = function (id) { return function () {
            var rules = _this.state.rules;
            openModal(function (modalProps) { return (<Edit {...modalProps} rule={rules[id]} projectId={_this.props.projectId} savedRules={rules} api={_this.api} endpoint={_this.props.endpoint} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully updated data scrubbing rule'));
            }}/>); });
        }; };
        _this.handleDelete = function (id) { return function () { return __awaiter(_this, void 0, void 0, function () {
            var rules, filteredRules, data, convertedRules, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        rules = this.state.rules;
                        filteredRules = rules.filter(function (rule) { return rule.id !== id; });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, submitRules(this.api, this.props.endpoint, filteredRules)];
                    case 2:
                        data = _b.sent();
                        if (data === null || data === void 0 ? void 0 : data.relayPiiConfig) {
                            convertedRules = convertRelayPiiConfig(data.relayPiiConfig);
                            this.setState({ rules: convertedRules });
                            addSuccessMessage(t('Successfully deleted data scrubbing rule'));
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('An unknown error occurred while deleting data scrubbing rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        return _this;
    }
    DataScrubbing.prototype.componentDidMount = function () {
        this.loadRules();
        this.loadOrganizationRules();
    };
    DataScrubbing.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.relayPiiConfig !== this.state.relayPiiConfig) {
            this.loadRules();
        }
    };
    DataScrubbing.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    DataScrubbing.prototype.loadOrganizationRules = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        if (projectId) {
            try {
                this.setState({
                    orgRules: convertRelayPiiConfig(organization.relayPiiConfig),
                });
            }
            catch (_b) {
                addErrorMessage(t('Unable to load organization rules'));
            }
        }
    };
    DataScrubbing.prototype.loadRules = function () {
        try {
            var convertedRules = convertRelayPiiConfig(this.state.relayPiiConfig);
            this.setState({
                rules: convertedRules,
                savedRules: convertedRules,
            });
        }
        catch (_a) {
            addErrorMessage(t('Unable to load project rules'));
        }
    };
    DataScrubbing.prototype.successfullySaved = function (response, successMessage) {
        var onSubmitSuccess = this.props.onSubmitSuccess;
        this.setState({ rules: convertRelayPiiConfig(response.relayPiiConfig) });
        addSuccessMessage(successMessage);
        onSubmitSuccess === null || onSubmitSuccess === void 0 ? void 0 : onSubmitSuccess(response);
    };
    DataScrubbing.prototype.render = function () {
        var _a = this.props, additionalContext = _a.additionalContext, disabled = _a.disabled, projectId = _a.projectId;
        var _b = this.state, orgRules = _b.orgRules, rules = _b.rules;
        return (<React.Fragment>
        <Panel data-test-id="advanced-data-scrubbing">
          <PanelHeader>
            <div>{t('Advanced Data Scrubbing')}</div>
          </PanelHeader>
          <PanelAlert type="info">
            {additionalContext}{' '}
            {"" + t('The new rules will only apply to upcoming events. ')}{' '}
            {tct('For more details, see [linkToDocs].', {
            linkToDocs: (<ExternalLink href={ADVANCED_DATASCRUBBING_LINK}>
                  {t('full documentation on data scrubbing')}
                </ExternalLink>),
        })}
          </PanelAlert>
          <PanelBody>
            {projectId && <OrganizationRules rules={orgRules}/>}
            <Content rules={rules} onDeleteRule={this.handleDelete} onEditRule={this.handleOpenEditModal} disabled={disabled}/>
            <PanelAction>
              <Button href={ADVANCED_DATASCRUBBING_LINK} target="_blank">
                {t('Read the docs')}
              </Button>
              <Button disabled={disabled} onClick={this.handleOpenAddModal} priority="primary">
                {t('Add Rule')}
              </Button>
            </PanelAction>
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return DataScrubbing;
}(React.Component));
export default DataScrubbing;
var PanelAction = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"])), space(1), space(2), space(1), function (p) { return p.theme.border; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map