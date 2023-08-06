var _a;
import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { convertDatasetEventTypesToSource, DATA_SOURCE_LABELS, DATA_SOURCE_TO_SET_AND_EVENT_TYPES, } from 'app/views/alerts/utils';
import { Panel, PanelBody } from 'app/components/panels';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { getDisplayName } from 'app/utils/environment';
import { t, tct } from 'app/locale';
import FormField from 'app/views/settings/components/forms/formField';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import SearchBar from 'app/views/events/searchBar';
import SelectField from 'app/views/settings/components/forms/selectField';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import Feature from 'app/components/acl/feature';
import { TimeWindow, Datasource } from './types';
import MetricField from './metricField';
import { DEFAULT_AGGREGATE } from './constants';
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
var RuleConditionsFormWithGuiFilters = /** @class */ (function (_super) {
    __extends(RuleConditionsFormWithGuiFilters, _super);
    function RuleConditionsFormWithGuiFilters() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            environments: null,
        };
        return _this;
    }
    RuleConditionsFormWithGuiFilters.prototype.componentDidMount = function () {
        this.fetchData();
    };
    RuleConditionsFormWithGuiFilters.prototype.fetchData = function () {
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
    RuleConditionsFormWithGuiFilters.prototype.render = function () {
        var _a;
        var _b = this.props, organization = _b.organization, disabled = _b.disabled, onFilterSearch = _b.onFilterSearch;
        var environments = this.state.environments;
        var environmentList = (_a = environments === null || environments === void 0 ? void 0 : environments.map(function (env) { return [env.name, getDisplayName(env)]; })) !== null && _a !== void 0 ? _a : [];
        var anyEnvironmentLabel = (<React.Fragment>
        {t('All Environments')}
        <div className="all-environment-note">
          {tct("This will count events across every environment. For example,\n             having 50 [code1:production] events and 50 [code2:development]\n             events would trigger an alert with a critical threshold of 100.", { code1: <code />, code2: <code /> })}
        </div>
      </React.Fragment>);
        environmentList.unshift([null, anyEnvironmentLabel]);
        var formElemBaseStyle = {
            padding: "" + space(0.5),
            border: 'none',
        };
        return (<Panel>
        <StyledPanelBody>
          <List symbol="colored-numeric">
            <StyledListItem>{t('Select the events you want to alert on')}</StyledListItem>
            <FormRow>
              <SelectField name="environment" placeholder={t('All Environments')} style={__assign(__assign({}, formElemBaseStyle), { minWidth: 250, flex: 2 })} styles={{
            singleValue: function (base) { return (__assign(__assign({}, base), { '.all-environment-note': { display: 'none' } })); },
            option: function (base, state) { return (__assign(__assign({}, base), { '.all-environment-note': __assign(__assign({}, (!state.isSelected && !state.isFocused
                    ? { color: theme.gray400 }
                    : {})), { fontSize: theme.fontSizeSmall }) })); },
        }} choices={environmentList} isDisabled={disabled || this.state.environments === null} isClearable inline={false} flexibleControlStateSize inFieldLabel={t('Env: ')}/>
              <Feature requireAll features={['organizations:performance-view']}>
                <FormField name="datasource" inline={false} style={__assign(__assign({}, formElemBaseStyle), { minWidth: 250, flex: 3 })} flexibleControlStateSize>
                  {function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, model = _a.model;
            var formDataset = model.getValue('dataset');
            var formEventTypes = model.getValue('eventTypes');
            var mappedValue = convertDatasetEventTypesToSource(formDataset, formEventTypes);
            return (<SelectControl value={mappedValue} inFieldLabel={t('Data Source: ')} onChange={function (optionObj) {
                var _a;
                var optionValue = optionObj.value;
                onChange(optionValue, {});
                onBlur(optionValue, {});
                // Reset the aggregate to the default (which works across
                // datatypes), otherwise we may send snuba an invalid query
                // (transaction aggregate on events datasource = bad).
                model.setValue('aggregate', DEFAULT_AGGREGATE);
                // set the value of the dataset and event type from data source
                var _b = (_a = DATA_SOURCE_TO_SET_AND_EVENT_TYPES[optionValue]) !== null && _a !== void 0 ? _a : {}, dataset = _b.dataset, eventTypes = _b.eventTypes;
                model.setValue('dataset', dataset);
                model.setValue('eventTypes', eventTypes);
            }} options={[
                {
                    label: t('Errors'),
                    options: [
                        {
                            value: Datasource.ERROR_DEFAULT,
                            label: DATA_SOURCE_LABELS[Datasource.ERROR_DEFAULT],
                        },
                        {
                            value: Datasource.DEFAULT,
                            label: DATA_SOURCE_LABELS[Datasource.DEFAULT],
                        },
                        {
                            value: Datasource.ERROR,
                            label: DATA_SOURCE_LABELS[Datasource.ERROR],
                        },
                    ],
                },
                {
                    label: t('Transactions'),
                    options: [
                        {
                            value: Datasource.TRANSACTION,
                            label: DATA_SOURCE_LABELS[Datasource.TRANSACTION],
                        },
                    ],
                },
            ]} isDisabled={disabled} required/>);
        }}
                </FormField>
              </Feature>
              <FormField name="query" inline={false} style={__assign(__assign({}, formElemBaseStyle), { flex: 6, minWidth: 400 })} flexibleControlStateSize>
                {function (_a) {
            var _b;
            var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, initialData = _a.initialData, model = _a.model;
            return (<SearchContainer>
                    <StyledSearchBar defaultQuery={(_b = initialData === null || initialData === void 0 ? void 0 : initialData.query) !== null && _b !== void 0 ? _b : ''} omitTags={['event.type']} disabled={disabled} useFormWrapper={false} organization={organization} placeholder={model.getValue('dataset') === 'events'
                ? t('Filter events by level, message, or other properties...')
                : t('Filter transactions by URL, tags, and other properties...')} onChange={onChange} onKeyDown={function (e) {
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
            </FormRow>
            <StyledListItem>{t('Choose a metric')}</StyledListItem>
            <FormRow>
              <MetricField name="aggregate" help={null} organization={organization} disabled={disabled} style={__assign(__assign({}, formElemBaseStyle), { flex: 6, minWidth: 300 })} inline={false} flexibleControlStateSize required/>
              <FormRowText>over</FormRowText>
              <SelectField name="timeWindow" style={__assign(__assign({}, formElemBaseStyle), { flex: 1, minWidth: 150 })} choices={Object.entries(TIME_WINDOW_MAP)} required isDisabled={disabled} getValue={function (value) { return Number(value); }} setValue={function (value) { return "" + value; }} inline={false} flexibleControlStateSize/>
            </FormRow>
            {this.props.thresholdChart}
          </List>
        </StyledPanelBody>
      </Panel>);
    };
    return RuleConditionsFormWithGuiFilters;
}(React.PureComponent));
var StyledPanelBody = styled(PanelBody)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  h4 {\n    margin-bottom: ", ";\n  }\n"], ["\n  h4 {\n    margin-bottom: ", ";\n  }\n"])), space(1));
var SearchContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledListItem = styled(ListItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " ", " 0 ", ";\n"], ["\n  font-size: ", ";\n  margin: ", " ", " 0 ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(3), space(3), space(3));
var FormRow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  padding: ", " ", ";\n  align-items: flex-end;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-direction: row;\n  padding: ", " ", ";\n  align-items: flex-end;\n  flex-wrap: wrap;\n"])), space(1.5), space(3));
var FormRowText = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", ";\n  line-height: 38px;\n"], ["\n  padding: ", ";\n  line-height: 38px;\n"])), space(0.5));
export default RuleConditionsFormWithGuiFilters;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=ruleConditionsFormWithGuiFilters.jsx.map