var _a;
import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { DATA_SOURCE_LABELS } from 'app/views/alerts/utils';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { defined } from 'app/utils';
import { getDisplayName } from 'app/utils/environment';
import { t, tct } from 'app/locale';
import FormField from 'app/views/settings/components/forms/formField';
import SearchBar from 'app/views/events/searchBar';
import FieldLabel from 'app/views/settings/components/forms/field/fieldLabel';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
import SelectField from 'app/views/settings/components/forms/selectField';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import Tooltip from 'app/components/tooltip';
import Feature from 'app/components/acl/feature';
import { TimeWindow, Dataset } from './types';
import MetricField from './metricField';
import { DATASET_EVENT_TYPE_FILTERS, DEFAULT_AGGREGATE } from './constants';
var TIME_WINDOW_MAP = (_a = {},
    _a[TimeWindow.ONE_MINUTE] = t('1 minute'),
    _a[TimeWindow.FIVE_MINUTES] = t('5 minutes'),
    _a[TimeWindow.TEN_MINUTES] = t('10 minutes'),
    _a[TimeWindow.FIFTEEN_MINUTES] = t('15 minutes'),
    _a[TimeWindow.THIRTY_MINUTES] = t('30 minutes'),
    _a[TimeWindow.ONE_HOUR] = t('1 hour'),
    _a[TimeWindow.TWO_HOURS] = t('2 hours'),
    _a[TimeWindow.FOUR_HOURS] = t('4 hours'),
    _a[TimeWindow.ONE_DAY] = t('24 hours'),
    _a);
var RuleConditionsForm = /** @class */ (function (_super) {
    __extends(RuleConditionsForm, _super);
    function RuleConditionsForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            environments: null,
        };
        return _this;
    }
    RuleConditionsForm.prototype.componentDidMount = function () {
        this.fetchData();
    };
    RuleConditionsForm.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, projectSlug, environments, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/environments/", {
                                query: {
                                    visibility: 'visible',
                                },
                            })];
                    case 2:
                        environments = _b.sent();
                        this.setState({ environments: environments });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        addErrorMessage(t('Unable to fetch environments'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    RuleConditionsForm.prototype.render = function () {
        var _a = this.props, organization = _a.organization, disabled = _a.disabled, onFilterSearch = _a.onFilterSearch;
        var environments = this.state.environments;
        var environmentList = defined(environments)
            ? environments.map(function (env) { return [env.name, getDisplayName(env)]; })
            : [];
        var anyEnvironmentLabel = (<React.Fragment>
        {t('All Environments')}
        <div className="all-environment-note">
          {tct("This will count events across every environment. For example,\n             having 50 [code1:production] events and 50 [code2:development]\n             events would trigger an alert with a critical threshold of 100.", { code1: <code />, code2: <code /> })}
        </div>
      </React.Fragment>);
        environmentList.unshift([null, anyEnvironmentLabel]);
        return (<React.Fragment>
        <Feature requireAll features={['organizations:performance-view']}>
          <StyledPanel>
            <PanelHeader>{t('Alert Conditions')}</PanelHeader>
            <PanelBody>
              <FormField required name="dataset" label="Data source">
                {function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, model = _a.model, label = _a.label;
            return (<RadioGroup orientInline disabled={disabled} value={value} label={label} onChange={function (id, e) {
                onChange(id, e);
                onBlur(id, e);
                // Reset the aggregate to the default (which works across
                // datatypes), otherwise we may send snuba an invalid query
                // (transaction aggregate on events datasource = bad).
                model.setValue('aggregate', DEFAULT_AGGREGATE);
            }} choices={[
                [Dataset.ERRORS, DATA_SOURCE_LABELS[Dataset.ERRORS]],
                [Dataset.TRANSACTIONS, DATA_SOURCE_LABELS[Dataset.TRANSACTIONS]],
            ]}/>);
        }}
              </FormField>
            </PanelBody>
          </StyledPanel>
        </Feature>

        <div>
          
          {this.props.thresholdChart}
          <StyledPanel>
            <PanelHeader>{t('Alert Conditions')}</PanelHeader>
            <PanelBody>
              <FormField name="query" inline={false}>
                {function (_a) {
            var _b;
            var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, initialData = _a.initialData, model = _a.model;
            return (<SearchContainer>
                    <SearchLabel>{t('Filter')}</SearchLabel>
                    <StyledSearchBar defaultQuery={(_b = initialData === null || initialData === void 0 ? void 0 : initialData.query) !== null && _b !== void 0 ? _b : ''} inlineLabel={<Tooltip title={t('Metric alerts are automatically filtered to your data source')}>
                          <SearchEventTypeNote>
                            {DATASET_EVENT_TYPE_FILTERS[model.getValue('dataset')]}
                          </SearchEventTypeNote>
                        </Tooltip>} omitTags={['event.type']} disabled={disabled} useFormWrapper={false} organization={organization} onChange={onChange} onKeyDown={function (e) {
                /**
                 * Do not allow enter key to submit the alerts form since it is unlikely
                 * users will be ready to create the rule as this sits above required fields.
                 */
                if (e.key === 'Enter') {
                    e.preventDefault();
                    e.stopPropagation();
                }
                onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
            }} onBlur={function (query) {
                onFilterSearch(query);
                onBlur(query);
            }} onSearch={function (query) {
                onFilterSearch(query);
                onChange(query, {});
            }}/>
                  </SearchContainer>);
        }}
              </FormField>
              <MetricField name="aggregate" label={t('Metric')} organization={organization} disabled={disabled} required/>
              <SelectField name="timeWindow" label={t('Time Window')} help={<React.Fragment>
                    <div>{t('The time window over which the Metric is evaluated')}</div>
                    <div>
                      {t('Note: Triggers are evaluated every minute regardless of this value.')}
                    </div>
                  </React.Fragment>} choices={Object.entries(TIME_WINDOW_MAP)} required isDisabled={disabled} getValue={function (value) { return Number(value); }} setValue={function (value) { return "" + value; }}/>
              <SelectField name="environment" label={t('Environment')} placeholder={t('All Environments')} help={t('Choose which environment events must match')} styles={{
            singleValue: function (base) { return (__assign(__assign({}, base), { '.all-environment-note': { display: 'none' } })); },
            option: function (base, state) { return (__assign(__assign({}, base), { '.all-environment-note': __assign(__assign({}, (!state.isSelected && !state.isFocused
                    ? { color: theme.gray400 }
                    : {})), { fontSize: theme.fontSizeSmall }) })); },
        }} choices={environmentList} isDisabled={disabled || this.state.environments === null} isClearable/>
            </PanelBody>
          </StyledPanel>
        </div>
      </React.Fragment>);
    };
    return RuleConditionsForm;
}(React.PureComponent));
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Sticky graph panel cannot have margin-bottom */\n  margin-top: ", ";\n"], ["\n  /* Sticky graph panel cannot have margin-bottom */\n  margin-top: ", ";\n"])), space(2));
var SearchContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var SearchLabel = styled(FieldLabel)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  align-items: center;\n  margin-right: ", ";\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var SearchEventTypeNote = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border-radius: 2px;\n  padding: ", " ", ";\n  margin: 0 ", " 0 ", ";\n  user-select: none;\n"], ["\n  font: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border-radius: 2px;\n  padding: ", " ", ";\n  margin: 0 ", " 0 ", ";\n  user-select: none;\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.backgroundSecondary; }, space(0.5), space(0.75), space(0.5), space(1));
export default RuleConditionsForm;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=ruleConditionsForm.jsx.map