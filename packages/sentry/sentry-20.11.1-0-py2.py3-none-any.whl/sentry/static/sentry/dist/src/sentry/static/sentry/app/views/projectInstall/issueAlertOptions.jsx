var _a;
import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import AsyncComponent from 'app/components/asyncComponent';
import Input from 'app/views/settings/components/forms/controls/input';
import PageHeading from 'app/components/pageHeading';
import SelectControl from 'app/components/forms/selectControl';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
var MetricValues;
(function (MetricValues) {
    MetricValues[MetricValues["ERRORS"] = 0] = "ERRORS";
    MetricValues[MetricValues["USERS"] = 1] = "USERS";
})(MetricValues || (MetricValues = {}));
var Actions;
(function (Actions) {
    Actions[Actions["ALERT_ON_EVERY_ISSUE"] = 0] = "ALERT_ON_EVERY_ISSUE";
    Actions[Actions["CUSTOMIZED_ALERTS"] = 1] = "CUSTOMIZED_ALERTS";
    Actions[Actions["CREATE_ALERT_LATER"] = 2] = "CREATE_ALERT_LATER";
})(Actions || (Actions = {}));
var UNIQUE_USER_FREQUENCY_CONDITION = 'sentry.rules.conditions.event_frequency.EventUniqueUserFrequencyCondition';
var EVENT_FREQUENCY_CONDITION = 'sentry.rules.conditions.event_frequency.EventFrequencyCondition';
var NOTIFY_EVENT_ACTION = 'sentry.rules.actions.notify_event.NotifyEventAction';
var METRIC_CONDITION_MAP = (_a = {},
    _a[MetricValues.ERRORS] = EVENT_FREQUENCY_CONDITION,
    _a[MetricValues.USERS] = UNIQUE_USER_FREQUENCY_CONDITION,
    _a);
var DEFAULT_PLACEHOLDER_VALUE = '10';
function getConditionFrom(interval, metricValue, threshold) {
    var condition;
    switch (metricValue) {
        case MetricValues.ERRORS:
            condition = EVENT_FREQUENCY_CONDITION;
            break;
        case MetricValues.USERS:
            condition = UNIQUE_USER_FREQUENCY_CONDITION;
            break;
        default:
            throw new RangeError('Supplied metric value is not handled');
    }
    return {
        interval: interval,
        id: condition,
        value: threshold,
    };
}
function unpackConditions(conditions) {
    var _a;
    var equalityReducer = function (acc, curr) {
        if (!acc || !curr || !isEqual(acc, curr)) {
            return null;
        }
        return acc;
    };
    var intervalChoices = conditions
        .map(function (condition) { var _a, _b; return (_b = (_a = condition.formFields) === null || _a === void 0 ? void 0 : _a.interval) === null || _b === void 0 ? void 0 : _b.choices; })
        .reduce(equalityReducer);
    return { intervalChoices: intervalChoices, interval: (_a = intervalChoices === null || intervalChoices === void 0 ? void 0 : intervalChoices[0]) === null || _a === void 0 ? void 0 : _a[0] };
}
var IssueAlertOptions = /** @class */ (function (_super) {
    __extends(IssueAlertOptions, _super);
    function IssueAlertOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueAlertOptions.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { conditions: [], intervalChoices: [], alertSetting: Actions.CREATE_ALERT_LATER.toString(), metric: MetricValues.ERRORS, interval: '', threshold: '' });
    };
    IssueAlertOptions.prototype.getAvailableMetricChoices = function () {
        var _this = this;
        return [
            [MetricValues.ERRORS, t('occurrences of')],
            [MetricValues.USERS, t('users affected by')],
        ].filter(function (valueDescriptionPair) {
            var _a, _b;
            var _c = __read(valueDescriptionPair, 1), value = _c[0];
            return (_b = (_a = _this.state.conditions) === null || _a === void 0 ? void 0 : _a.some) === null || _b === void 0 ? void 0 : _b.call(_a, function (object) { return (object === null || object === void 0 ? void 0 : object.id) === METRIC_CONDITION_MAP[value]; });
        });
    };
    IssueAlertOptions.prototype.getIssueAlertsChoices = function (hasProperlyLoadedConditions) {
        var _this = this;
        var options = [
            [Actions.CREATE_ALERT_LATER.toString(), t("I'll create my own alerts later")],
            [Actions.ALERT_ON_EVERY_ISSUE.toString(), t('Alert me on every new issue')],
        ];
        if (hasProperlyLoadedConditions) {
            options.push([
                Actions.CUSTOMIZED_ALERTS.toString(),
                <CustomizeAlertsGrid key={Actions.CUSTOMIZED_ALERTS} onClick={function (e) {
                    // XXX(epurkhiser): The `e.preventDefault` here is needed to stop
                    // propegation of the click up to the label, causing it to focus
                    // the radio input and lose focus on the select.
                    e.preventDefault();
                    var alertSetting = Actions.CUSTOMIZED_ALERTS.toString();
                    _this.setStateAndUpdateParents({ alertSetting: alertSetting });
                }}>
          {t('When there are more than')}
          <InlineInput type="number" min="0" name="" placeholder={DEFAULT_PLACEHOLDER_VALUE} value={this.state.threshold} key={name} onChange={function (threshold) {
                    return _this.setStateAndUpdateParents({ threshold: threshold.target.value });
                }} data-test-id="range-input"/>
          <InlineSelectControl value={this.state.metric} choices={this.getAvailableMetricChoices()} onChange={function (metric) { return _this.setStateAndUpdateParents({ metric: metric.value }); }} data-test-id="metric-select-control"/>
          {t('a unique error in')}
          <InlineSelectControl value={this.state.interval} choices={this.state.intervalChoices} onChange={function (interval) {
                    return _this.setStateAndUpdateParents({ interval: interval.value });
                }} data-test-id="interval-select-control"/>
        </CustomizeAlertsGrid>,
            ]);
        }
        return options.map(function (_a) {
            var _b = __read(_a, 2), choiceValue = _b[0], node = _b[1];
            return [
                choiceValue,
                <RadioItemWrapper key={choiceValue}>{node}</RadioItemWrapper>,
            ];
        });
    };
    IssueAlertOptions.prototype.getUpdatedData = function () {
        var defaultRules;
        var shouldCreateCustomRule;
        var alertSetting = parseInt(this.state.alertSetting, 10);
        switch (alertSetting) {
            case Actions.ALERT_ON_EVERY_ISSUE:
                defaultRules = true;
                shouldCreateCustomRule = false;
                break;
            case Actions.CREATE_ALERT_LATER:
                defaultRules = false;
                shouldCreateCustomRule = false;
                break;
            case Actions.CUSTOMIZED_ALERTS:
                defaultRules = false;
                shouldCreateCustomRule = true;
                break;
            default:
                throw new RangeError('Supplied alert creation action is not handled');
        }
        return {
            defaultRules: defaultRules,
            shouldCreateCustomRule: shouldCreateCustomRule,
            name: 'Send a notification for new issues',
            conditions: this.state.interval.length > 0 && this.state.threshold.length > 0
                ? [
                    getConditionFrom(this.state.interval, this.state.metric, this.state.threshold),
                ]
                : undefined,
            actions: [{ id: NOTIFY_EVENT_ACTION }],
            actionMatch: 'all',
            frequency: 5,
        };
    };
    IssueAlertOptions.prototype.setStateAndUpdateParents = function (state, callback) {
        var _this = this;
        this.setState(state, function () {
            callback === null || callback === void 0 ? void 0 : callback();
            _this.props.onChange(_this.getUpdatedData());
        });
    };
    IssueAlertOptions.prototype.getEndpoints = function () {
        return [['conditions', "/projects/" + this.props.organization.slug + "/rule-conditions/"]];
    };
    IssueAlertOptions.prototype.onLoadAllEndpointsSuccess = function () {
        var _this = this;
        var _a, _b;
        var conditions = (_b = (_a = this.state.conditions) === null || _a === void 0 ? void 0 : _a.filter) === null || _b === void 0 ? void 0 : _b.call(_a, function (object) {
            return Object.values(METRIC_CONDITION_MAP).includes(object === null || object === void 0 ? void 0 : object.id);
        });
        if (!conditions || conditions.length === 0) {
            this.setStateAndUpdateParents({
                conditions: undefined,
            });
            return;
        }
        var _c = unpackConditions(conditions), intervalChoices = _c.intervalChoices, interval = _c.interval;
        if (!intervalChoices || !interval) {
            Sentry.withScope(function (scope) {
                scope.setExtra('props', _this.props);
                scope.setExtra('state', _this.state);
                Sentry.captureException(new Error('Interval choices or sent from API endpoint is inconsistent or empty'));
            });
            this.setStateAndUpdateParents({
                conditions: undefined,
            });
            return;
        }
        this.setStateAndUpdateParents({
            conditions: conditions,
            intervalChoices: intervalChoices,
            interval: interval,
        });
    };
    IssueAlertOptions.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var issueAlertOptionsChoices = this.getIssueAlertsChoices(((_a = this.state.conditions) === null || _a === void 0 ? void 0 : _a.length) > 0);
        return (<React.Fragment>
        <PageHeadingWithTopMargins withMargins>
          {t('Set your default alert settings')}
        </PageHeadingWithTopMargins>
        <RadioGroupWithPadding choices={issueAlertOptionsChoices} label={t('Options for creating an alert')} onChange={function (alertSetting) { return _this.setStateAndUpdateParents({ alertSetting: alertSetting }); }} value={this.state.alertSetting}/>
      </React.Fragment>);
    };
    return IssueAlertOptions;
}(AsyncComponent));
export default withOrganization(IssueAlertOptions);
var CustomizeAlertsGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(5, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(5, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var InlineInput = styled(Input)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 80px;\n"], ["\n  width: 80px;\n"])));
var InlineSelectControl = styled(SelectControl)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 160px;\n"], ["\n  width: 160px;\n"])));
var RadioGroupWithPadding = styled(RadioGroup)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " 0;\n  margin-bottom: 50px;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n"], ["\n  padding: ", " 0;\n  margin-bottom: 50px;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n"])), space(3));
var PageHeadingWithTopMargins = styled(PageHeading)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-top: 65px;\n"], ["\n  margin-top: 65px;\n"])));
var RadioItemWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  min-height: 35px;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"], ["\n  min-height: 35px;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=issueAlertOptions.jsx.map