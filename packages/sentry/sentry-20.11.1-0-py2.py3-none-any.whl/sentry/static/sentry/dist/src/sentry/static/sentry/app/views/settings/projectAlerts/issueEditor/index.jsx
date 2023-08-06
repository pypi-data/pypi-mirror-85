import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { ALL_ENVIRONMENTS_KEY } from 'app/constants';
import { OnboardingTaskKey } from 'app/types';
import { IconWarning, IconChevron } from 'app/icons';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import Input from 'app/views/settings/components/forms/controls/input';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { getDisplayName } from 'app/utils/environment';
import { t, tct } from 'app/locale';
import Access from 'app/components/acl/access';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Form from 'app/views/settings/components/forms/form';
import LoadingMask from 'app/components/loadingMask';
import SelectField from 'app/views/settings/components/forms/selectField';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import { updateOnboardingTask } from 'app/actionCreators/onboardingTasks';
import Field from 'app/views/settings/components/forms/field';
import RuleNodeList from './ruleNodeList';
var FREQUENCY_CHOICES = [
    ['5', t('5 minutes')],
    ['10', t('10 minutes')],
    ['30', t('30 minutes')],
    ['60', t('60 minutes')],
    ['180', t('3 hours')],
    ['720', t('12 hours')],
    ['1440', t('24 hours')],
    ['10080', t('one week')],
    ['43200', t('30 days')],
];
var ACTION_MATCH_CHOICES = [
    ['all', t('all')],
    ['any', t('any')],
    ['none', t('none')],
];
var ACTION_MATCH_CHOICES_MIGRATED = [
    ['all', t('all')],
    ['any', t('any')],
];
var defaultRule = {
    actionMatch: 'all',
    filterMatch: 'all',
    actions: [],
    conditions: [],
    filters: [],
    name: '',
    frequency: 30,
    environment: ALL_ENVIRONMENTS_KEY,
};
var POLLING_MAX_TIME_LIMIT = 3 * 60000;
function isSavedAlertRule(rule) {
    var _a;
    return (_a = rule === null || rule === void 0 ? void 0 : rule.hasOwnProperty('id')) !== null && _a !== void 0 ? _a : false;
}
var IssueRuleEditor = /** @class */ (function (_super) {
    __extends(IssueRuleEditor, _super);
    function IssueRuleEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pollHandler = function (quitTime) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, uuid, origRule, response, status_1, rule, error, ruleId, isNew, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (Date.now() > quitTime) {
                            addErrorMessage(t('Looking for that channel took too long :('));
                            this.setState({ loading: false });
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, project = _a.project;
                        uuid = this.state.uuid;
                        origRule = this.state.rule;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/rule-task/" + uuid + "/")];
                    case 2:
                        response = _c.sent();
                        status_1 = response.status, rule = response.rule, error = response.error;
                        if (status_1 === 'pending') {
                            setTimeout(function () {
                                _this.pollHandler(quitTime);
                            }, 1000);
                            return [2 /*return*/];
                        }
                        if (status_1 === 'failed') {
                            this.setState({
                                detailedError: { actions: [error ? error : t('An error occurred')] },
                                loading: false,
                            });
                            addErrorMessage(t('An error occurred'));
                        }
                        if (rule) {
                            ruleId = isSavedAlertRule(origRule) ? origRule.id + "/" : '';
                            isNew = !ruleId;
                            this.handleRuleSuccess(isNew, rule);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRuleSuccess = function (isNew, rule) {
            var _a = _this.props, organization = _a.organization, router = _a.router;
            _this.setState({ detailedError: null, loading: false, rule: rule });
            // The onboarding task will be completed on the server side when the alert
            // is created
            updateOnboardingTask(null, organization, {
                task: OnboardingTaskKey.ALERT_RULE,
                status: 'complete',
            });
            router.push("/organizations/" + organization.slug + "/alerts/rules/");
            addSuccessMessage(isNew ? t('Created alert rule') : t('Updated alert rule'));
        };
        _this.handleSubmit = function () { return __awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, _b, resp, xhr, err_1;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        if (rule && rule.environment === ALL_ENVIRONMENTS_KEY) {
                            delete rule.environment;
                        }
                        addLoadingMessage();
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                includeAllArgs: true,
                                method: isNew ? 'POST' : 'PUT',
                                data: rule,
                            })];
                    case 2:
                        _b = __read.apply(void 0, [_c.sent(), 3]), resp = _b[0], xhr = _b[2];
                        // if we get a 202 back it means that we have an async task
                        // running to lookup and verify the channel id for Slack.
                        if (xhr && xhr.status === 202) {
                            this.setState({ detailedError: null, loading: true, uuid: resp.uuid });
                            this.fetchStatus();
                            addLoadingMessage(t('Looking through all your channels...'));
                        }
                        else {
                            this.handleRuleSuccess(isNew, resp);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        this.setState({
                            detailedError: err_1.responseJSON || { __all__: 'Unknown error' },
                            loading: false,
                        });
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleDeleteRule = function () { return __awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, err_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        if (isNew) {
                            return [2 /*return*/];
                        }
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        addLoadingMessage(t('Deleting...'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(t('Deleted alert rule'));
                        browserHistory.replace(recreateRoute('', __assign(__assign({}, this.props), { stepBack: -2 })));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _b.sent();
                        this.setState({
                            detailedError: err_2.responseJSON || { __all__: 'Unknown error' },
                        });
                        addErrorMessage(t('There was a problem deleting the alert'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCancel = function () {
            var _a = _this.props, organization = _a.organization, router = _a.router;
            router.push("/organizations/" + organization.slug + "/alerts/rules/");
        };
        _this.hasError = function (field) {
            var detailedError = _this.state.detailedError;
            if (!detailedError) {
                return false;
            }
            return detailedError.hasOwnProperty(field);
        };
        _this.handleEnvironmentChange = function (val) {
            // If 'All Environments' is selected the value should be null
            if (val === ALL_ENVIRONMENTS_KEY) {
                _this.handleChange('environment', null);
            }
            else {
                _this.handleChange('environment', val);
            }
        };
        _this.handleChange = function (prop, val) {
            _this.setState(function (state) {
                var rule = __assign({}, state.rule);
                rule[prop] = val;
                return { rule: rule, detailedError: omit(state.detailedError, prop) };
            });
        };
        _this.handlePropertyChange = function (type, idx, prop, val) {
            _this.setState(function (state) {
                var rule = __assign({}, state.rule);
                rule[type][idx][prop] = val;
                return { rule: rule };
            });
        };
        _this.handleAddRow = function (type, id) {
            _this.setState(function (state) {
                var _a;
                var _b, _c;
                var configuration = (_c = (_b = _this.state.configs) === null || _b === void 0 ? void 0 : _b[type]) === null || _c === void 0 ? void 0 : _c.find(function (c) { return c.id === id; });
                // Set initial configuration
                var initialValue = (configuration === null || configuration === void 0 ? void 0 : configuration.formFields) ? Object.fromEntries(Object.entries(configuration.formFields)
                    // TODO(ts): Doesn't work if I cast formField as IssueAlertRuleFormField
                    .map(function (_a) {
                    var _b, _c, _d;
                    var _e = __read(_a, 2), key = _e[0], formField = _e[1];
                    return [
                        key,
                        (_b = formField === null || formField === void 0 ? void 0 : formField.initial) !== null && _b !== void 0 ? _b : (_d = (_c = formField === null || formField === void 0 ? void 0 : formField.choices) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d[0],
                    ];
                })
                    .filter(function (_a) {
                    var _b = __read(_a, 2), initial = _b[1];
                    return !!initial;
                }))
                    : {};
                var newRule = __assign({ id: id }, initialValue);
                var rule = __assign(__assign({}, state.rule), (_a = {}, _a[type] = __spread((state.rule ? state.rule[type] : []), [newRule]), _a));
                return {
                    rule: rule,
                };
            });
        };
        _this.handleDeleteRow = function (type, idx) {
            _this.setState(function (prevState) {
                var _a;
                var newTypeList = prevState.rule ? __spread(prevState.rule[type]) : [];
                if (prevState.rule) {
                    newTypeList.splice(idx, 1);
                }
                var rule = __assign(__assign({}, prevState.rule), (_a = {}, _a[type] = newTypeList, _a));
                return {
                    rule: rule,
                };
            });
        };
        _this.handleAddCondition = function (id) { return _this.handleAddRow('conditions', id); };
        _this.handleAddAction = function (id) { return _this.handleAddRow('actions', id); };
        _this.handleAddFilter = function (id) { return _this.handleAddRow('filters', id); };
        _this.handleDeleteCondition = function (ruleIndex) {
            return _this.handleDeleteRow('conditions', ruleIndex);
        };
        _this.handleDeleteAction = function (ruleIndex) { return _this.handleDeleteRow('actions', ruleIndex); };
        _this.handleDeleteFilter = function (ruleIndex) { return _this.handleDeleteRow('filters', ruleIndex); };
        _this.handleChangeConditionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('conditions', ruleIndex, prop, val);
        };
        _this.handleChangeActionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('actions', ruleIndex, prop, val);
        };
        _this.handleChangeFilterProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('filters', ruleIndex, prop, val);
        };
        _this.handleValidateRuleName = function () {
            var _a;
            var isRuleNameEmpty = !((_a = _this.state.rule) === null || _a === void 0 ? void 0 : _a.name.trim());
            if (!isRuleNameEmpty) {
                return;
            }
            _this.setState(function (prevState) { return ({
                detailedError: __assign(__assign({}, prevState.detailedError), { name: [t('Field Required')] }),
            }); });
        };
        return _this;
    }
    IssueRuleEditor.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { configs: null, detailedError: null, rule: __assign({}, defaultRule), environments: [], uuid: null });
    };
    IssueRuleEditor.prototype.getEndpoints = function () {
        var _a = this.props.params, ruleId = _a.ruleId, projectId = _a.projectId, orgId = _a.orgId;
        var endpoints = [
            ['environments', "/projects/" + orgId + "/" + projectId + "/environments/"],
            ['configs', "/projects/" + orgId + "/" + projectId + "/rules/configuration/"],
        ];
        if (ruleId) {
            endpoints.push(['rule', "/projects/" + orgId + "/" + projectId + "/rules/" + ruleId + "/"]);
        }
        return endpoints;
    };
    IssueRuleEditor.prototype.fetchStatus = function () {
        var _this = this;
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        var quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(function () {
            _this.pollHandler(quitTime);
        }, 1000);
    };
    IssueRuleEditor.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IssueRuleEditor.prototype.renderError = function () {
        return (<Alert type="error" icon={<IconWarning />}>
        {t('Unable to access this alert rule -- check to make sure you have the correct permissions')}
      </Alert>);
    };
    IssueRuleEditor.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var _b = this.props, project = _b.project, organization = _b.organization;
        var environments = this.state.environments;
        var environmentChoices = __spread([
            [ALL_ENVIRONMENTS_KEY, t('All Environments')]
        ], ((_a = environments === null || environments === void 0 ? void 0 : environments.map(function (env) { return [env.name, getDisplayName(env)]; })) !== null && _a !== void 0 ? _a : []));
        var _c = this.state, rule = _c.rule, detailedError = _c.detailedError;
        var _d = rule || {}, actions = _d.actions, filters = _d.filters, conditions = _d.conditions, frequency = _d.frequency, name = _d.name;
        var environment = !rule || !rule.environment ? ALL_ENVIRONMENTS_KEY : rule.environment;
        // Note `key` on `<Form>` below is so that on initial load, we show
        // the form with a loading mask on top of it, but force a re-render by using
        // a different key when we have fetched the rule so that form inputs are filled in
        return (<Access access={['project:write']}>
        {function (_a) {
            var _b, _c, _d, _e, _f;
            var hasAccess = _a.hasAccess;
            return (<StyledForm key={isSavedAlertRule(rule) ? rule.id : undefined} onCancel={_this.handleCancel} onSubmit={_this.handleSubmit} initialData={__assign(__assign({}, rule), { environment: environment, frequency: "" + frequency })} submitDisabled={!hasAccess} submitLabel={isSavedAlertRule(rule) ? t('Save Rule') : t('Create Alert Rule')} extraButton={isSavedAlertRule(rule) ? (<Confirm disabled={!hasAccess} priority="danger" confirmText={t('Delete Rule')} onConfirm={_this.handleDeleteRule} header={t('Delete Rule')} message={t('Are you sure you want to delete this rule?')}>
                  <Button priority="danger" type="button">
                    {t('Delete Rule')}
                  </Button>
                </Confirm>) : null}>
            {_this.state.loading && <SemiTransparentLoadingMask />}
            <Panel>
              <PanelHeader>{t('Alert Setup')}</PanelHeader>
              <PanelBody>
                <SelectField className={classNames({
                error: _this.hasError('environment'),
            })} label={t('Environment')} help={t('Choose an environment for these conditions to apply to')} placeholder={t('Select an Environment')} clearable={false} name="environment" choices={environmentChoices} onChange={function (val) { return _this.handleEnvironmentChange(val); }} disabled={!hasAccess}/>

                <StyledField label={t('Alert name')} help={t('Add a name for this alert')} error={(_b = detailedError === null || detailedError === void 0 ? void 0 : detailedError.name) === null || _b === void 0 ? void 0 : _b[0]} disabled={!hasAccess} required stacked>
                  <Input type="text" name="name" value={name} placeholder={t('My Rule Name')} onChange={function (event) {
                return _this.handleChange('name', event.target.value);
            }} onBlur={_this.handleValidateRuleName}/>
                </StyledField>
              </PanelBody>
            </Panel>

            <Panel>
              <PanelHeader>{t('Alert Conditions')}</PanelHeader>
              <PanelBody>
                <Step>
                  <StepConnector />

                  <StepContainer>
                    <ChevronContainer>
                      <IconChevron color="gray200" isCircled direction="right" size="sm"/>
                    </ChevronContainer>

                    <Feature features={['projects:alert-filters']} project={project}>
                      {function (_a) {
                var _b, _c;
                var hasFeature = _a.hasFeature;
                return (<StepContent>
                          <StepLead>
                            {tct('[when:When] an event is captured by Sentry and [selector] of the following happens', {
                    when: <Badge />,
                    selector: (<EmbeddedWrapper>
                                    <EmbeddedSelectField className={classNames({
                        error: _this.hasError('actionMatch'),
                    })} inline={false} styles={{
                        control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '20px', height: '20px' })); },
                    }} isSearchable={false} isClearable={false} name="actionMatch" required flexibleControlStateSize choices={hasFeature
                        ? ACTION_MATCH_CHOICES_MIGRATED
                        : ACTION_MATCH_CHOICES} onChange={function (val) {
                        return _this.handleChange('actionMatch', val);
                    }} disabled={!hasAccess}/>
                                  </EmbeddedWrapper>),
                })}
                          </StepLead>
                          <RuleNodeList nodes={(_c = (_b = _this.state.configs) === null || _b === void 0 ? void 0 : _b.conditions) !== null && _c !== void 0 ? _c : null} items={conditions !== null && conditions !== void 0 ? conditions : []} placeholder={hasFeature
                    ? t('Add optional trigger...')
                    : t('Add optional condition...')} onPropertyChange={_this.handleChangeConditionProperty} onAddRow={_this.handleAddCondition} onDeleteRow={_this.handleDeleteCondition} organization={organization} project={project} disabled={!hasAccess} error={_this.hasError('conditions') && (<StyledAlert type="error">
                                  {detailedError === null || detailedError === void 0 ? void 0 : detailedError.conditions[0]}
                                </StyledAlert>)}/>
                        </StepContent>);
            }}
                    </Feature>
                  </StepContainer>
                </Step>

                <Feature features={['organizations:alert-filters', 'projects:alert-filters']} organization={organization} project={project} requireAll={false}>
                  <Step>
                    <StepConnector />

                    <StepContainer>
                      <ChevronContainer>
                        <IconChevron color="gray200" isCircled direction="right" size="sm"/>
                      </ChevronContainer>

                      <StepContent>
                        <StepLead>
                          {tct('[if:If] [selector] of these filters match', {
                if: <Badge />,
                selector: (<EmbeddedWrapper>
                                <EmbeddedSelectField className={classNames({
                    error: _this.hasError('filterMatch'),
                })} inline={false} styles={{
                    control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '20px', height: '20px' })); },
                }} isSearchable={false} isClearable={false} name="filterMatch" required flexibleControlStateSize choices={ACTION_MATCH_CHOICES} onChange={function (val) { return _this.handleChange('filterMatch', val); }} disabled={!hasAccess}/>
                              </EmbeddedWrapper>),
            })}
                        </StepLead>
                        <RuleNodeList nodes={(_d = (_c = _this.state.configs) === null || _c === void 0 ? void 0 : _c.filters) !== null && _d !== void 0 ? _d : null} items={filters !== null && filters !== void 0 ? filters : []} placeholder={t('Add optional filter...')} onPropertyChange={_this.handleChangeFilterProperty} onAddRow={_this.handleAddFilter} onDeleteRow={_this.handleDeleteFilter} organization={organization} project={project} disabled={!hasAccess} error={_this.hasError('filters') && (<StyledAlert type="error">
                                {detailedError === null || detailedError === void 0 ? void 0 : detailedError.filters[0]}
                              </StyledAlert>)}/>
                      </StepContent>
                    </StepContainer>
                  </Step>
                </Feature>

                <Step>
                  <StepContainer>
                    <ChevronContainer>
                      <IconChevron isCircled color="gray200" direction="right" size="sm"/>
                    </ChevronContainer>
                    <StepContent>
                      <StepLead>
                        {tct('[then:Then] perform these actions', {
                then: <Badge />,
            })}
                      </StepLead>

                      <RuleNodeList nodes={(_f = (_e = _this.state.configs) === null || _e === void 0 ? void 0 : _e.actions) !== null && _f !== void 0 ? _f : null} items={actions !== null && actions !== void 0 ? actions : []} placeholder={t('Add action...')} onPropertyChange={_this.handleChangeActionProperty} onAddRow={_this.handleAddAction} onDeleteRow={_this.handleDeleteAction} organization={organization} project={project} disabled={!hasAccess} error={_this.hasError('actions') && (<StyledAlert type="error">
                              {detailedError === null || detailedError === void 0 ? void 0 : detailedError.actions[0]}
                            </StyledAlert>)}/>
                    </StepContent>
                  </StepContainer>
                </Step>
              </PanelBody>
            </Panel>

            <Panel>
              <PanelHeader>{t('Rate Limit')}</PanelHeader>
              <PanelBody>
                <SelectField label={t('Action Interval')} help={t('Perform these actions once this often for an issue')} clearable={false} name="frequency" className={_this.hasError('frequency') ? ' error' : ''} value={frequency} required choices={FREQUENCY_CHOICES} onChange={function (val) { return _this.handleChange('frequency', val); }} disabled={!hasAccess}/>
              </PanelBody>
            </Panel>
          </StyledForm>);
        }}
      </Access>);
    };
    return IssueRuleEditor;
}(AsyncView));
export default withProject(withOrganization(IssueRuleEditor));
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledAlert = styled(Alert)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var Step = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  margin: ", " ", " ", " ", ";\n"], ["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  margin: ", " ", " ", " ", ";\n"])), space(4), space(4), space(3), space(1));
var StepContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  flex-grow: 1;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  flex-grow: 1;\n"])));
var StepContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StepConnector = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: absolute;\n  height: 100%;\n  top: 28px;\n  left: 19px;\n  border-right: 1px ", " dashed;\n"], ["\n  position: absolute;\n  height: 100%;\n  top: 28px;\n  left: 19px;\n  border-right: 1px ", " dashed;\n"])), function (p) { return p.theme.gray300; });
var StepLead = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(0.5));
var ChevronContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " ", ";\n"])), space(0.5), space(1.5));
var Badge = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: inline-block;\n  min-width: 56px;\n  background-color: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  text-align: center;\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.5;\n"], ["\n  display: inline-block;\n  min-width: 56px;\n  background-color: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  text-align: center;\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.5;\n"])), function (p) { return p.theme.purple300; }, space(0.75), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeMedium; });
var EmbeddedWrapper = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: inline-block;\n  margin: 0 ", ";\n  width: 80px;\n"], ["\n  display: inline-block;\n  margin: 0 ", ";\n  width: 80px;\n"])), space(0.5));
var EmbeddedSelectField = styled(SelectField)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"], ["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"])));
var SemiTransparentLoadingMask = styled(LoadingMask)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"], ["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"])));
var StyledField = styled(Field)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  :last-child {\n    padding-bottom: ", ";\n  }\n"], ["\n  :last-child {\n    padding-bottom: ", ";\n  }\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=index.jsx.map