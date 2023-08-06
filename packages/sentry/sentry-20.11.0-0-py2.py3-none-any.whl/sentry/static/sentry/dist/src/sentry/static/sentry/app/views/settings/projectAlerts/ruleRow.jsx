import { __extends, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import { css } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { AlertRuleThresholdType, } from 'app/views/settings/incidentRules/types';
import { getDisplayName } from 'app/utils/environment';
import { t, tct } from 'app/locale';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
function isIssueAlert(data) {
    return !data.hasOwnProperty('triggers');
}
var RuleRow = /** @class */ (function (_super) {
    __extends(RuleRow, _super);
    function RuleRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { loading: false, error: false };
        return _this;
    }
    RuleRow.prototype.renderIssueRule = function (data) {
        var _a = this.props, params = _a.params, routes = _a.routes, location = _a.location, canEdit = _a.canEdit;
        var editLink = recreateRoute("rules/" + data.id + "/", {
            params: params,
            routes: routes,
            location: location,
        });
        var environmentName = data.environment
            ? getDisplayName({ name: data.environment })
            : t('All Environments');
        return (<React.Fragment>
        <RuleType>{t('Issue')}</RuleType>
        <div>
          {canEdit ? <RuleName to={editLink}>{data.name}</RuleName> : data.name}
          <RuleDescription>
            {t('Environment')}: {environmentName}
          </RuleDescription>
        </div>

        <ConditionsWithHeader>
          <MatchTypeHeader>
            {tct('[matchType] of the following:', {
            matchType: data.actionMatch,
        })}
          </MatchTypeHeader>
          {data.conditions.length !== 0 && (<Conditions>
              {data.conditions.map(function (condition, i) { return (<div key={i}>{condition.name}</div>); })}
            </Conditions>)}
        </ConditionsWithHeader>

        <Actions>
          {data.actions.map(function (action, i) { return (<Action key={i}>{action.name}</Action>); })}
        </Actions>
      </React.Fragment>);
    };
    RuleRow.prototype.renderMetricRule = function (data) {
        var _a = this.props, params = _a.params, routes = _a.routes, location = _a.location, canEdit = _a.canEdit;
        var editLink = recreateRoute("metric-rules/" + data.id + "/", {
            params: params,
            routes: routes,
            location: location,
        });
        var numberOfTriggers = data.triggers.length;
        return (<React.Fragment>
        <RuleType rowSpans={numberOfTriggers}>{t('Metric')}</RuleType>
        <RuleNameAndDescription rowSpans={numberOfTriggers}>
          {canEdit ? <RuleName to={editLink}>{data.name}</RuleName> : data.name}
          <RuleDescription />
        </RuleNameAndDescription>

        {numberOfTriggers !== 0 &&
            data.triggers.map(function (trigger, i) {
                var _a;
                var hideBorder = i !== numberOfTriggers - 1;
                return (<React.Fragment key={i}>
                <Trigger key={"trigger-" + i} hideBorder={hideBorder}>
                  <StatusBadge>{trigger.label}</StatusBadge>
                  <TriggerDescription>
                    {data.aggregate}{' '}
                    {data.thresholdType === AlertRuleThresholdType.ABOVE
                    ? t('above')
                    : t('below')}{' '}
                    {trigger.alertThreshold}/{data.timeWindow}
                    {t('min')}
                  </TriggerDescription>
                </Trigger>
                <Actions key={"actions-" + i} hideBorder={hideBorder}>
                  {((_a = trigger.actions) === null || _a === void 0 ? void 0 : _a.length) ? trigger.actions.map(function (action, j) { return (<Action key={j}>{action.desc}</Action>); })
                    : t('None')}
                </Actions>
              </React.Fragment>);
            })}
      </React.Fragment>);
    };
    RuleRow.prototype.render = function () {
        var data = this.props.data;
        return isIssueAlert(data) ? this.renderIssueRule(data) : this.renderMetricRule(data);
    };
    RuleRow.propTypes = {
        data: PropTypes.object.isRequired,
        canEdit: PropTypes.bool,
    };
    return RuleRow;
}(React.Component));
export default RuleRow;
var RuleType = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n  ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n  ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.rowSpans && "grid-row: auto / span " + p.rowSpans; });
var RuleNameAndDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return p.rowSpans && "grid-row: auto / span " + p.rowSpans; });
var RuleName = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var listingCss = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var Conditions = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), listingCss);
var Actions = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, listingCss, function (p) { return p.hideBorder && "border-bottom: none"; });
var Action = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  line-height: 14px;\n"], ["\n  line-height: 14px;\n"])));
var ConditionsWithHeader = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var MatchTypeHeader = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-weight: bold;\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-weight: bold;\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
var RuleDescription = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " 0;\n  white-space: nowrap;\n"], ["\n  font-size: ", ";\n  margin: ", " 0;\n  white-space: nowrap;\n"])), function (p) { return p.theme.fontSizeSmall; }, space(0.5));
var Trigger = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  font-size: ", ";\n\n  ", ";\n"], ["\n  display: flex;\n  align-items: flex-start;\n  font-size: ", ";\n\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.hideBorder && "border-bottom: none"; });
var TriggerDescription = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var StatusBadge = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  background-color: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  padding: ", " ", ";\n  font-weight: 600;\n  margin-right: ", ";\n  border-radius: ", ";\n  font-size: ", ";\n"], ["\n  background-color: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  padding: ", " ", ";\n  font-weight: 600;\n  margin-right: ", ";\n  border-radius: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.textColor; }, space(0.25), space(0.5), space(0.5), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeRelativeSmall; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=ruleRow.jsx.map