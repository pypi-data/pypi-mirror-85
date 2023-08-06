import { __assign, __extends, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelAlert, PanelBody, PanelHeader, PanelItem, } from 'app/components/panels';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import AsyncComponent from 'app/components/asyncComponent';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
import FormField from 'app/views/settings/components/forms/formField';
import HookStore from 'app/stores/hookStore';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import Switch from 'app/components/switch';
import filterGroups, { customFilterFields } from 'app/data/forms/inboundFilters';
var LEGACY_BROWSER_SUBFILTERS = {
    ie_pre_9: {
        icon: 'internet-explorer',
        helpText: 'Version 8 and lower',
        title: 'Internet Explorer',
    },
    ie9: {
        icon: 'internet-explorer',
        helpText: 'Version 9',
        title: 'Internet Explorer',
    },
    ie10: {
        icon: 'internet-explorer',
        helpText: 'Version 10',
        title: 'Internet Explorer',
    },
    ie11: {
        icon: 'internet-explorer',
        helpText: 'Version 11',
        title: 'Internet Explorer',
    },
    safari_pre_6: {
        icon: 'safari',
        helpText: 'Version 5 and lower',
        title: 'Safari',
    },
    opera_pre_15: {
        icon: 'opera',
        helpText: 'Version 14 and lower',
        title: 'Opera',
    },
    opera_mini_pre_8: {
        icon: 'opera',
        helpText: 'Version 8 and lower',
        title: 'Opera Mini',
    },
    android_pre_4: {
        icon: 'android',
        helpText: 'Version 3 and lower',
        title: 'Android',
    },
};
var LEGACY_BROWSER_KEYS = Object.keys(LEGACY_BROWSER_SUBFILTERS);
var LegacyBrowserFilterRow = /** @class */ (function (_super) {
    __extends(LegacyBrowserFilterRow, _super);
    function LegacyBrowserFilterRow(props) {
        var _this = _super.call(this, props) || this;
        _this.handleToggleSubfilters = function (subfilter, e) {
            var subfilters = _this.state.subfilters;
            if (subfilter === true) {
                subfilters = new Set(LEGACY_BROWSER_KEYS);
            }
            else if (subfilter === false) {
                subfilters = new Set();
            }
            else if (subfilters.has(subfilter)) {
                subfilters.delete(subfilter);
            }
            else {
                subfilters.add(subfilter);
            }
            _this.setState({
                subfilters: new Set(subfilters),
            }, function () {
                _this.props.onToggle(_this.props.data, subfilters, e);
            });
        };
        var initialSubfilters;
        if (props.data.active === true) {
            initialSubfilters = new Set(LEGACY_BROWSER_KEYS);
        }
        else if (props.data.active === false) {
            initialSubfilters = new Set();
        }
        else {
            initialSubfilters = new Set(props.data.active);
        }
        _this.state = {
            loading: false,
            error: false,
            subfilters: initialSubfilters,
        };
        return _this;
    }
    LegacyBrowserFilterRow.prototype.render = function () {
        var _this = this;
        var disabled = this.props.disabled;
        return (<div>
        {!disabled && (<BulkFilter>
            <BulkFilterLabel>{t('Filter')}:</BulkFilterLabel>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, true)}>
              {t('All')}
            </BulkFilterItem>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, false)}>
              {t('None')}
            </BulkFilterItem>
          </BulkFilter>)}

        <FilterGrid>
          {LEGACY_BROWSER_KEYS.map(function (key) {
            var subfilter = LEGACY_BROWSER_SUBFILTERS[key];
            return (<FilterGridItemWrapper key={key}>
                <FilterGridItem>
                  <FilterItem>
                    <FilterGridIcon className={"icon-" + subfilter.icon}/>
                    <div>
                      <FilterTitle>{subfilter.title}</FilterTitle>
                      <FilterDescription>{subfilter.helpText}</FilterDescription>
                    </div>
                  </FilterItem>

                  <Switch isActive={_this.state.subfilters.has(key)} isDisabled={disabled} css={{ flexShrink: 0, marginLeft: 6 }} toggle={_this.handleToggleSubfilters.bind(_this, key)} size="lg"/>
                </FilterGridItem>
              </FilterGridItemWrapper>);
        })}
        </FilterGrid>
      </div>);
    };
    LegacyBrowserFilterRow.propTypes = {
        data: PropTypes.object.isRequired,
        onToggle: PropTypes.func.isRequired,
        disabled: PropTypes.bool,
    };
    return LegacyBrowserFilterRow;
}(React.Component));
var ProjectFiltersSettings = /** @class */ (function (_super) {
    __extends(ProjectFiltersSettings, _super);
    function ProjectFiltersSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegacyChange = function (onChange, onBlur, _filter, subfilters, e) {
            onChange === null || onChange === void 0 ? void 0 : onChange(subfilters, e);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(subfilters, e);
        };
        _this.renderDisabledCustomFilters = function (p) { return (<FeatureDisabled featureName={t('Custom Inbound Filters')} features={p.features} alert={PanelAlert} message={t('Release and Error Message filtering are not enabled on your Sentry installation')}/>); };
        _this.renderCustomFilters = function (disabled) { return function () { return (<Feature features={['projects:custom-inbound-filters']} hookName="feature-disabled:custom-inbound-filters" renderDisabled={function (_a) {
            var children = _a.children, props = __rest(_a, ["children"]);
            if (typeof children === 'function') {
                return children(__assign(__assign({}, props), { renderDisabled: _this.renderDisabledCustomFilters }));
            }
            return null;
        }}>
      {function (_a) {
            var hasFeature = _a.hasFeature, organization = _a.organization, renderDisabled = _a.renderDisabled, featureProps = __rest(_a, ["hasFeature", "organization", "renderDisabled"]);
            return (<React.Fragment>
          {!hasFeature &&
                typeof renderDisabled === 'function' &&
                // XXX: children is set to null as we're doing tricksy things
                // in the renderDisabled prop a few lines higher.
                renderDisabled(__assign({ organization: organization, hasFeature: hasFeature, children: null }, featureProps))}

          {customFilterFields.map(function (field) { return (<FieldFromConfig key={field.name} field={field} disabled={disabled || !hasFeature}/>); })}
        </React.Fragment>);
        }}
    </Feature>); }; };
        return _this;
    }
    ProjectFiltersSettings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { hooksDisabled: HookStore.get('feature-disabled:custom-inbound-filters') });
    };
    ProjectFiltersSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [
            ['filterList', "/projects/" + orgId + "/" + projectId + "/filters/"],
            ['project', "/projects/" + orgId + "/" + projectId + "/"],
        ];
    };
    ProjectFiltersSettings.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevProps.project !== this.props.project) {
            this.reloadData();
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    ProjectFiltersSettings.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, features = _a.features, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var project = this.state.project;
        if (!project) {
            return null;
        }
        var projectEndpoint = "/projects/" + orgId + "/" + projectId + "/";
        var filtersEndpoint = projectEndpoint + "filters/";
        return (<Access access={['project:write']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<React.Fragment>
            <Panel>
              <PanelHeader>{t('Filters')}</PanelHeader>
              <PanelBody>
                {_this.state.filterList.map(function (filter) {
                var _a;
                var fieldProps = {
                    name: filter.id,
                    label: filter.name,
                    help: filter.description,
                    disabled: !hasAccess,
                };
                // Note by default, forms generate data in the format of:
                // { [fieldName]: [value] }
                // Endpoints for these filters expect data to be:
                // { 'active': [value] }
                return (<PanelItem key={filter.id} p={0}>
                      <NestedForm apiMethod="PUT" apiEndpoint={"" + filtersEndpoint + filter.id + "/"} initialData={_a = {}, _a[filter.id] = filter.active, _a} saveOnBlur>
                        {filter.id !== 'legacy-browsers' ? (<FieldFromConfig key={filter.id} getData={function (data) { return ({ active: data[filter.id] }); }} field={__assign({ type: 'boolean' }, fieldProps)}/>) : (<FormField inline={false} {...fieldProps} getData={function (data) { return ({ subfilters: __spread(data[filter.id]) }); }}>
                            {function (_a) {
                    var onChange = _a.onChange, onBlur = _a.onBlur;
                    return (<LegacyBrowserFilterRow key={filter.id} data={filter} disabled={!hasAccess} onToggle={_this.handleLegacyChange.bind(_this, onChange, onBlur)}/>);
                }}
                          </FormField>)}
                      </NestedForm>
                    </PanelItem>);
            })}
              </PanelBody>
            </Panel>

            <Form apiMethod="PUT" apiEndpoint={projectEndpoint} initialData={_this.state.project.options} saveOnBlur>
              <JsonForm features={features} forms={filterGroups} disabled={!hasAccess} renderFooter={_this.renderCustomFilters(!hasAccess)}/>
            </Form>
          </React.Fragment>);
        }}
      </Access>);
    };
    return ProjectFiltersSettings;
}(AsyncComponent));
export default ProjectFiltersSettings;
var NestedForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var FilterGrid = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var FilterGridItem = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  background: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"], ["\n  display: flex;\n  align-items: center;\n  background: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"])), function (p) { return p.theme.backgroundSecondary; });
// We want this wrapper to maining 30% width
var FilterGridItemWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 12px;\n  width: 50%;\n"], ["\n  padding: 12px;\n  width: 50%;\n"])));
var FilterItem = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var FilterGridIcon = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: 38px;\n  height: 38px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 38px 38px;\n  margin-right: 6px;\n  flex-shrink: 0;\n"], ["\n  width: 38px;\n  height: 38px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 38px 38px;\n  margin-right: 6px;\n  flex-shrink: 0;\n"])));
var FilterTitle = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: 14px;\n  font-weight: bold;\n  line-height: 1;\n  white-space: nowrap;\n"], ["\n  font-size: 14px;\n  font-weight: bold;\n  line-height: 1;\n  white-space: nowrap;\n"])));
var FilterDescription = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 12px;\n  line-height: 1;\n  white-space: nowrap;\n"], ["\n  color: ", ";\n  font-size: 12px;\n  line-height: 1;\n  white-space: nowrap;\n"])), function (p) { return p.theme.subText; });
var BulkFilter = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  text-align: right;\n  padding: 0 12px;\n"], ["\n  text-align: right;\n  padding: 0 12px;\n"])));
var BulkFilterLabel = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-weight: bold;\n  margin-right: 6px;\n"], ["\n  font-weight: bold;\n  margin-right: 6px;\n"])));
var BulkFilterItem = styled('a')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  border-right: 1px solid #f1f2f3;\n  margin-right: 6px;\n  padding-right: 6px;\n\n  &:last-child {\n    border-right: none;\n    margin-right: 0;\n  }\n"], ["\n  border-right: 1px solid #f1f2f3;\n  margin-right: 6px;\n  padding-right: 6px;\n\n  &:last-child {\n    border-right: none;\n    margin-right: 0;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=projectFiltersSettings.jsx.map