import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconDelete, IconEdit } from 'app/icons';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import { deleteRule } from './actions';
var IncidentRulesList = /** @class */ (function (_super) {
    __extends(IncidentRulesList, _super);
    function IncidentRulesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemoveRule = function (rule) { return __awaiter(_this, void 0, void 0, function () {
            var orgId, oldRules, newRules, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        orgId = this.props.params.orgId;
                        oldRules = this.state.rules.slice(0);
                        newRules = this.state.rules.filter(function (_a) {
                            var id = _a.id;
                            return id !== rule.id;
                        });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        this.setState({
                            rules: newRules,
                        });
                        return [4 /*yield*/, deleteRule(this.api, orgId, rule)];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        this.setState({
                            rules: oldRules,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    IncidentRulesList.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['rules', "/organizations/" + orgId + "/alert-rules/"]];
    };
    IncidentRulesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentRulesList.prototype.renderBody = function () {
        var _this = this;
        var isLoading = this.state.loading;
        var isEmpty = !isLoading && !this.state.rules.length;
        return (<Panel>
        <GridPanelHeader>
          <NameColumn>{t('Name')}</NameColumn>

          <div>{t('Metric')}</div>

          <div>{t('Threshold')}</div>
        </GridPanelHeader>

        <PanelBody>
          {isLoading && <LoadingIndicator />}

          {!isLoading &&
            !isEmpty &&
            this.state.rules.map(function (rule) {
                var ruleLink = recreateRoute(rule.id + "/", _this.props);
                return (<RuleRow key={rule.id}>
                  <RuleLink to={ruleLink}>{rule.name}</RuleLink>

                  <MetricName>{rule.aggregate}</MetricName>

                  <ThresholdColumn>
                    <Thresholds>
                      {rule.triggers.map(function (trigger) { return trigger.alertThreshold; }).join(', ')}
                    </Thresholds>

                    <Actions>
                      <Button to={ruleLink} size="small" aria-label={t('Edit Rule')}>
                        <IconEdit size="xs"/>
                        &nbsp;
                        {t('Edit')}
                      </Button>

                      <Confirm priority="danger" onConfirm={function () { return _this.handleRemoveRule(rule); }} message={t('Are you sure you want to remove this rule?')}>
                        <Button type="button" size="small" icon={<IconDelete />} label={t('Remove Rule')}/>
                      </Confirm>
                    </Actions>
                  </ThresholdColumn>
                </RuleRow>);
            })}

          {!isLoading && isEmpty && (<EmptyMessage>{t('No Alert Rules have been created yet.')}</EmptyMessage>)}
        </PanelBody>
      </Panel>);
    };
    return IncidentRulesList;
}(AsyncView));
export default IncidentRulesList;
var gridCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 3fr 1fr 2fr;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 3fr 1fr 2fr;\n  align-items: center;\n"])));
var nameColumnCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var GridPanelHeader = styled(PanelHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 0;\n  ", ";\n"], ["\n  padding: 0;\n  ", ";\n"])), gridCss);
var RuleRow = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 0;\n  align-items: center;\n  ", ";\n"], ["\n  padding: 0;\n  align-items: center;\n  ", ";\n"])), gridCss);
var NameColumn = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), nameColumnCss);
var RuleLink = styled(Link)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), nameColumnCss);
// For tests
var MetricName = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject([""], [""])));
var ThresholdColumn = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
// For tests
var Thresholds = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
var Actions = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin: ", ";\n"])), space(1), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=list.jsx.map