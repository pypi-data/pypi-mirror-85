import { __assign, __awaiter, __extends, __generator, __read, __rest, __spread } from "tslib";
import React from 'react';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { fetchOrganizationTags } from 'app/actionCreators/tags';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Feature from 'app/components/acl/feature';
import Form from 'app/views/settings/components/forms/form';
import RuleNameForm from 'app/views/settings/incidentRules/ruleNameForm';
import Triggers from 'app/views/settings/incidentRules/triggers';
import TriggersChart from 'app/views/settings/incidentRules/triggers/chart';
import hasThresholdValue from 'app/views/settings/incidentRules/utils/hasThresholdValue';
import withProject from 'app/utils/withProject';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { convertDatasetEventTypesToSource } from 'app/views/alerts/utils';
import { AlertRuleThresholdType, Dataset, Datasource, } from '../types';
import { addOrUpdateRule } from '../actions';
import { createDefaultTrigger, DATASET_EVENT_TYPE_FILTERS, DATASOURCE_EVENT_TYPE_FILTERS, } from '../constants';
import RuleConditionsForm from '../ruleConditionsForm';
import RuleConditionsFormWithGuiFilters from '../ruleConditionsFormWithGuiFilters';
var POLLING_MAX_TIME_LIMIT = 3 * 60000;
var isEmpty = function (str) { return str === '' || !defined(str); };
var RuleFormContainer = /** @class */ (function (_super) {
    __extends(RuleFormContainer, _super);
    function RuleFormContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.resetPollingState = function () {
            _this.setState({ loading: false, uuid: undefined });
        };
        _this.pollHandler = function (model, quitTime) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, onSubmitSuccess, ruleId, uuid, response, status_1, alertRule, error, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (Date.now() > quitTime) {
                            addErrorMessage(t('Looking for that channel took too long :('));
                            this.resetPollingState();
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, project = _a.project, onSubmitSuccess = _a.onSubmitSuccess, ruleId = _a.params.ruleId;
                        uuid = this.state.uuid;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/alert-rule-task/" + uuid + "/")];
                    case 2:
                        response = _c.sent();
                        status_1 = response.status, alertRule = response.alertRule, error = response.error;
                        if (status_1 === 'pending') {
                            setTimeout(function () {
                                _this.pollHandler(model, quitTime);
                            }, 1000);
                            return [2 /*return*/];
                        }
                        this.resetPollingState();
                        if (status_1 === 'failed') {
                            addErrorMessage(error);
                        }
                        if (alertRule) {
                            addSuccessMessage(ruleId ? t('Updated alert rule') : t('Created alert rule'));
                            if (onSubmitSuccess) {
                                onSubmitSuccess(alertRule, model);
                            }
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred'));
                        this.resetPollingState();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * Checks to see if threshold is valid given target value, and state of
         * inverted threshold as well as the *other* threshold
         *
         * @param type The threshold type to be updated
         * @param value The new threshold value
         */
        _this.isValidTrigger = function (triggerIndex, trigger, errors, resolveThreshold) {
            var alertThreshold = trigger.alertThreshold;
            var thresholdType = _this.state.thresholdType;
            // If value and/or other value is empty
            // then there are no checks to perform against
            if (!hasThresholdValue(alertThreshold) || !hasThresholdValue(resolveThreshold)) {
                return true;
            }
            // If this is alert threshold and not inverted, it can't be below resolve
            // If this is alert threshold and inverted, it can't be above resolve
            // If this is resolve threshold and not inverted, it can't be above resolve
            // If this is resolve threshold and inverted, it can't be below resolve
            // Since we're comparing non-inclusive thresholds here (>, <), we need
            // to modify the values when we compare. An example of why:
            // Alert > 0, resolve < 1. This means that we want to alert on values
            // of 1 or more, and resolve on values of 0 or less. This is valid, but
            // without modifying the values, this boundary case will fail.
            var isValid = thresholdType === AlertRuleThresholdType.BELOW
                ? alertThreshold - 1 <= resolveThreshold + 1
                : alertThreshold + 1 >= resolveThreshold - 1;
            var otherErrors = errors.get(triggerIndex) || {};
            if (isValid) {
                return true;
            }
            // Not valid... let's figure out an error message
            var isBelow = thresholdType === AlertRuleThresholdType.BELOW;
            var errorMessage = '';
            if (typeof resolveThreshold !== 'number') {
                errorMessage = isBelow
                    ? t('Resolution threshold must be greater than alert')
                    : t('Resolution threshold must be less than alert');
            }
            else {
                errorMessage = isBelow
                    ? t('Alert threshold must be less than resolution')
                    : t('Alert threshold must be greater than resolution');
            }
            errors.set(triggerIndex, __assign(__assign({}, otherErrors), { alertThreshold: errorMessage }));
            return false;
        };
        _this.handleFieldChange = function (name, value) {
            var _a;
            if (['dataset', 'eventTypes', 'timeWindow', 'environment', 'aggregate'].includes(name)) {
                _this.setState((_a = {}, _a[name] = value, _a));
            }
        };
        // We handle the filter update outside of the fieldChange handler since we
        // don't want to update the filter on every input change, just on blurs and
        // searches.
        _this.handleFilterUpdate = function (query) {
            var _a = _this.props, organization = _a.organization, sessionId = _a.sessionId;
            trackAnalyticsEvent({
                eventKey: 'alert_builder.filter',
                eventName: 'Alert Builder: Filter',
                query: query,
                organization_id: organization.id,
                session_id: sessionId,
            });
            _this.setState({ query: query });
        };
        _this.handleSubmit = function (_data, _onSubmitSuccess, _onSubmitError, _e, model) { return __awaiter(_this, void 0, void 0, function () {
            var validRule, triggerErrors, validTriggers, _a, organization, params, rule, onSubmitSuccess, location, sessionId, ruleId, _b, resolveThreshold, triggers, thresholdType, uuid, sanitizedTriggers, _c, resp, xhr, err_1, errors, apiErrors;
            var _d;
            return __generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        validRule = model.validateForm();
                        triggerErrors = this.validateTriggers();
                        validTriggers = Array.from(triggerErrors).length === 0;
                        if (!validTriggers) {
                            this.setState(function (state) { return ({
                                triggerErrors: new Map(__spread(triggerErrors, state.triggerErrors)),
                            }); });
                        }
                        if (!validRule || !validTriggers) {
                            addErrorMessage(t('Alert not valid'));
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, params = _a.params, rule = _a.rule, onSubmitSuccess = _a.onSubmitSuccess, location = _a.location, sessionId = _a.sessionId;
                        ruleId = this.props.params.ruleId;
                        _b = this.state, resolveThreshold = _b.resolveThreshold, triggers = _b.triggers, thresholdType = _b.thresholdType, uuid = _b.uuid;
                        sanitizedTriggers = triggers.filter(function (trigger) { return trigger.label !== 'warning' || !isEmpty(trigger.alertThreshold); });
                        _f.label = 1;
                    case 1:
                        _f.trys.push([1, 3, , 4]);
                        addLoadingMessage();
                        return [4 /*yield*/, addOrUpdateRule(this.api, organization.slug, params.projectId, __assign(__assign(__assign({}, rule), model.getTransformedData()), { triggers: sanitizedTriggers, resolveThreshold: isEmpty(resolveThreshold) ? null : resolveThreshold, thresholdType: thresholdType }), {
                                referrer: (_d = location === null || location === void 0 ? void 0 : location.query) === null || _d === void 0 ? void 0 : _d.referrer,
                                sessionId: sessionId,
                            })];
                    case 2:
                        _c = __read.apply(void 0, [_f.sent(), 3]), resp = _c[0], xhr = _c[2];
                        // if we get a 202 back it means that we have an async task
                        // running to lookup and verify the channel id for Slack.
                        if (xhr && xhr.status === 202) {
                            // if we have a uuid in state, no need to start a new polling cycle
                            if (!uuid) {
                                this.setState({ loading: true, uuid: resp.uuid });
                                this.fetchStatus(model);
                                addLoadingMessage(t('Looking through all your channels...'));
                            }
                        }
                        else {
                            addSuccessMessage(ruleId ? t('Updated alert rule') : t('Created alert rule'));
                            if (onSubmitSuccess) {
                                onSubmitSuccess(resp, model);
                            }
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _f.sent();
                        errors = (err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) ? Array.isArray(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            ? err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON : Object.values(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            : [];
                        apiErrors = errors.length > 0 ? ": " + errors.join(', ') : '';
                        addErrorMessage(t('Unable to save alert%s', apiErrors));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * Callback for when triggers change
         *
         * Re-validate triggers on every change and reset indicators when no errors
         */
        _this.handleChangeTriggers = function (triggers, triggerIndex) {
            _this.setState(function (state) {
                var triggerErrors = state.triggerErrors;
                var newTriggerErrors = _this.validateTriggers(triggers, state.thresholdType, state.resolveThreshold, triggerIndex);
                triggerErrors = newTriggerErrors;
                if (Array.from(newTriggerErrors).length === 0) {
                    clearIndicators();
                }
                return { triggers: triggers, triggerErrors: triggerErrors };
            });
        };
        _this.handleThresholdTypeChange = function (thresholdType) {
            var triggers = _this.state.triggers;
            var triggerErrors = _this.validateTriggers(triggers, thresholdType);
            _this.setState(function (state) { return ({
                thresholdType: thresholdType,
                triggerErrors: new Map(__spread(triggerErrors, state.triggerErrors)),
            }); });
        };
        _this.handleResolveThresholdChange = function (resolveThreshold) {
            var triggers = _this.state.triggers;
            var triggerErrors = _this.validateTriggers(triggers, undefined, resolveThreshold);
            _this.setState(function (state) { return ({
                resolveThreshold: resolveThreshold,
                triggerErrors: new Map(__spread(triggerErrors, state.triggerErrors)),
            }); });
        };
        _this.handleDeleteRule = function () { return __awaiter(_this, void 0, void 0, function () {
            var params, orgId, projectId, ruleId, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId, projectId = params.projectId, ruleId = params.ruleId;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/alert-rules/" + ruleId + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.goBack();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCancel = function () {
            _this.goBack();
        };
        return _this;
    }
    RuleFormContainer.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        // SearchBar gets its tags from Reflux.
        fetchOrganizationTags(this.api, organization.slug, [project.id]);
    };
    RuleFormContainer.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        var triggersClone = __spread(rule.triggers);
        // Warning trigger is removed if it is blank when saving
        if (triggersClone.length !== 2) {
            triggersClone.push(createDefaultTrigger('warning'));
        }
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { dataset: rule.dataset, aggregate: rule.aggregate, query: rule.query || '', timeWindow: rule.timeWindow, environment: rule.environment || null, triggerErrors: new Map(), availableActions: null, triggers: triggersClone, resolveThreshold: rule.resolveThreshold, thresholdType: rule.thresholdType, projects: [this.props.project] });
    };
    RuleFormContainer.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        // TODO(incidents): This is temporary until new API endpoints
        // We should be able to just fetch the rule if rule.id exists
        return [
            ['availableActions', "/organizations/" + orgId + "/alert-rules/available-actions/"],
        ];
    };
    Object.defineProperty(RuleFormContainer.prototype, "eventTypeFilter", {
        get: function () {
            var _a, _b;
            if (this.state.eventTypes) {
                return DATASOURCE_EVENT_TYPE_FILTERS[(_a = convertDatasetEventTypesToSource(this.state.dataset, this.state.eventTypes)) !== null && _a !== void 0 ? _a : Datasource.ERROR];
            }
            else {
                return DATASET_EVENT_TYPE_FILTERS[(_b = this.state.dataset) !== null && _b !== void 0 ? _b : Dataset.ERRORS];
            }
        },
        enumerable: false,
        configurable: true
    });
    RuleFormContainer.prototype.goBack = function () {
        var router = this.props.router;
        var orgId = this.props.params.orgId;
        router.push("/organizations/" + orgId + "/alerts/rules/");
    };
    RuleFormContainer.prototype.fetchStatus = function (model) {
        var _this = this;
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        var quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(function () {
            _this.pollHandler(model, quitTime);
        }, 1000);
    };
    RuleFormContainer.prototype.validateFieldInTrigger = function (_a) {
        var _b;
        var errors = _a.errors, triggerIndex = _a.triggerIndex, field = _a.field, message = _a.message, isValid = _a.isValid;
        // If valid, reset error for fieldName
        if (isValid()) {
            var _c = errors.get(triggerIndex) || {}, _d = field, _validatedField = _c[_d], otherErrors = __rest(_c, [typeof _d === "symbol" ? _d : _d + ""]);
            if (Object.keys(otherErrors).length > 0) {
                errors.set(triggerIndex, otherErrors);
            }
            else {
                errors.delete(triggerIndex);
            }
            return errors;
        }
        if (!errors.has(triggerIndex)) {
            errors.set(triggerIndex, {});
        }
        var currentErrors = errors.get(triggerIndex);
        errors.set(triggerIndex, __assign(__assign({}, currentErrors), (_b = {}, _b[field] = message, _b)));
        return errors;
    };
    /**
     * Validate triggers
     *
     * @return Returns true if triggers are valid
     */
    RuleFormContainer.prototype.validateTriggers = function (triggers, thresholdType, resolveThreshold, changedTriggerIndex) {
        var _this = this;
        var _a, _b;
        if (triggers === void 0) { triggers = this.state.triggers; }
        if (thresholdType === void 0) { thresholdType = this.state.thresholdType; }
        if (resolveThreshold === void 0) { resolveThreshold = this.state.resolveThreshold; }
        var triggerErrors = new Map();
        var requiredFields = ['label', 'alertThreshold'];
        triggers.forEach(function (trigger, triggerIndex) {
            requiredFields.forEach(function (field) {
                // check required fields
                _this.validateFieldInTrigger({
                    errors: triggerErrors,
                    triggerIndex: triggerIndex,
                    isValid: function () {
                        if (trigger.label === 'critical') {
                            return !isEmpty(trigger[field]);
                        }
                        // If warning trigger has actions, it must have a value
                        return trigger.actions.length === 0 || !isEmpty(trigger[field]);
                    },
                    field: field,
                    message: t('Field is required'),
                });
            });
            // Check thresholds
            _this.isValidTrigger(changedTriggerIndex !== null && changedTriggerIndex !== void 0 ? changedTriggerIndex : triggerIndex, trigger, triggerErrors, resolveThreshold);
        });
        // If we have 2 triggers, we need to make sure that the critical and warning
        // alert thresholds are valid (e.g. if critical is above x, warning must be less than x)
        var criticalTriggerIndex = triggers.findIndex(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTriggerIndex = criticalTriggerIndex ^ 1;
        var criticalTrigger = triggers[criticalTriggerIndex];
        var warningTrigger = triggers[warningTriggerIndex];
        var isEmptyWarningThreshold = isEmpty(warningTrigger.alertThreshold);
        var warningThreshold = (_a = warningTrigger.alertThreshold) !== null && _a !== void 0 ? _a : 0;
        var criticalThreshold = (_b = criticalTrigger.alertThreshold) !== null && _b !== void 0 ? _b : 0;
        var hasError = thresholdType === AlertRuleThresholdType.ABOVE
            ? warningThreshold > criticalThreshold
            : warningThreshold < criticalThreshold;
        if (hasError && !isEmptyWarningThreshold) {
            [criticalTriggerIndex, warningTriggerIndex].forEach(function (index) {
                var _a;
                var otherErrors = (_a = triggerErrors.get(index)) !== null && _a !== void 0 ? _a : {};
                triggerErrors.set(index, __assign(__assign({}, otherErrors), { alertThreshold: thresholdType === AlertRuleThresholdType.BELOW
                        ? t('Warning threshold must be greater than critical alert')
                        : t('Warning threshold must be less than critical alert') }));
            });
        }
        return triggerErrors;
    };
    RuleFormContainer.prototype.renderLoading = function () {
        return this.renderBody();
    };
    RuleFormContainer.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, ruleId = _a.ruleId, rule = _a.rule, params = _a.params, onSubmitSuccess = _a.onSubmitSuccess;
        var _b = this.state, query = _b.query, timeWindow = _b.timeWindow, triggers = _b.triggers, aggregate = _b.aggregate, environment = _b.environment, thresholdType = _b.thresholdType, resolveThreshold = _b.resolveThreshold;
        var queryWithTypeFilter = (query + " " + this.eventTypeFilter).trim();
        var chart = (<TriggersChart organization={organization} projects={this.state.projects} triggers={triggers} query={queryWithTypeFilter} aggregate={aggregate} timeWindow={timeWindow} environment={environment} resolveThreshold={resolveThreshold} thresholdType={thresholdType}/>);
        return (<Access access={['project:write']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Feature features={['metric-alert-gui-filters']} organization={organization}>
            {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<Form apiMethod={ruleId ? 'PUT' : 'POST'} apiEndpoint={"/organizations/" + organization.slug + "/alert-rules/" + (ruleId ? ruleId + "/" : '')} submitDisabled={!hasAccess} initialData={{
                    name: rule.name || '',
                    dataset: rule.dataset,
                    eventTypes: hasFeature ? rule.eventTypes : undefined,
                    aggregate: rule.aggregate,
                    query: rule.query || '',
                    timeWindow: rule.timeWindow,
                    environment: rule.environment || null,
                }} saveOnBlur={false} onSubmit={_this.handleSubmit} onSubmitSuccess={onSubmitSuccess} onCancel={_this.handleCancel} onFieldChange={_this.handleFieldChange} extraButton={!!rule.id ? (<Confirm disabled={!hasAccess} message={t('Are you sure you want to delete this alert rule?')} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={_this.handleDeleteRule}>
                      <Button type="button" priority="danger">
                        {t('Delete Rule')}
                      </Button>
                    </Confirm>) : null} submitLabel={t('Save Rule')}>
                {hasFeature ? (<RuleConditionsFormWithGuiFilters api={_this.api} projectSlug={params.projectId} organization={organization} disabled={!hasAccess} thresholdChart={chart} onFilterSearch={_this.handleFilterUpdate}/>) : (<RuleConditionsForm api={_this.api} projectSlug={params.projectId} organization={organization} disabled={!hasAccess} thresholdChart={chart} onFilterSearch={_this.handleFilterUpdate}/>)}

                <Triggers disabled={!hasAccess} projects={_this.state.projects} errors={_this.state.triggerErrors} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType} currentProject={params.projectId} organization={organization} ruleId={ruleId} availableActions={_this.state.availableActions} onChange={_this.handleChangeTriggers} onThresholdTypeChange={_this.handleThresholdTypeChange} onResolveThresholdChange={_this.handleResolveThresholdChange}/>

                <RuleNameForm disabled={!hasAccess}/>
              </Form>);
            }}
          </Feature>);
        }}
      </Access>);
    };
    return RuleFormContainer;
}(AsyncComponent));
export { RuleFormContainer };
export default withProject(RuleFormContainer);
//# sourceMappingURL=index.jsx.map