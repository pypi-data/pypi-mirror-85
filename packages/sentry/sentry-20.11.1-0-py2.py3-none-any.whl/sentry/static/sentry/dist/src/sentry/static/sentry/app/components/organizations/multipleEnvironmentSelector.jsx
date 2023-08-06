import { __extends, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import uniq from 'lodash/uniq';
import { analytics } from 'app/utils/analytics';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import GlobalSelectionHeaderRow from 'app/components/globalSelectionHeaderRow';
import HeaderItem from 'app/components/organizations/headerItem';
import Highlight from 'app/components/highlight';
import MultipleSelectorSubmitRow from 'app/components/organizations/multipleSelectorSubmitRow';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import { IconWindow } from 'app/icons';
/**
 * Environment Selector
 *
 * Note we only fetch environments when this component is mounted
 */
var MultipleEnvironmentSelector = /** @class */ (function (_super) {
    __extends(MultipleEnvironmentSelector, _super);
    function MultipleEnvironmentSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            selectedEnvs: new Set(_this.props.value),
            hasChanges: false,
        };
        _this.syncSelectedStateFromProps = function () {
            return _this.setState({ selectedEnvs: new Set(_this.props.value) });
        };
        /**
         * If value in state is different than value from props, propagate changes
         */
        _this.doChange = function (environments) {
            _this.props.onChange(environments);
        };
        /**
         * Checks if "onUpdate" is callable. Only calls if there are changes
         */
        _this.doUpdate = function () {
            _this.setState({ hasChanges: false }, _this.props.onUpdate);
        };
        /**
         * Toggle selected state of an environment
         */
        _this.toggleSelected = function (environment) {
            _this.setState(function (state) {
                var selectedEnvs = new Set(state.selectedEnvs);
                if (selectedEnvs.has(environment)) {
                    selectedEnvs.delete(environment);
                }
                else {
                    selectedEnvs.add(environment);
                }
                analytics('environmentselector.toggle', {
                    action: selectedEnvs.has(environment) ? 'added' : 'removed',
                    path: getRouteStringFromRoutes(_this.context.router.routes),
                    org_id: parseInt(_this.props.organization.id, 10),
                });
                _this.doChange(Array.from(selectedEnvs.values()));
                return {
                    selectedEnvs: selectedEnvs,
                    hasChanges: true,
                };
            });
        };
        /**
         * Calls "onUpdate" callback and closes the dropdown menu
         */
        _this.handleUpdate = function (actions) {
            actions.close();
            _this.doUpdate();
        };
        _this.handleClose = function () {
            // Only update if there are changes
            if (!_this.state.hasChanges) {
                return;
            }
            analytics('environmentselector.update', {
                count: _this.state.selectedEnvs.size,
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.doUpdate();
        };
        /**
         * Clears all selected environments and updates
         */
        _this.handleClear = function () {
            analytics('environmentselector.clear', {
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                hasChanges: false,
                selectedEnvs: new Set(),
            }, function () {
                _this.doChange([]);
                _this.doUpdate();
            });
        };
        /**
         * Selects an environment, should close menu and initiate an update
         */
        _this.handleSelect = function (item) {
            var environment = item.value;
            analytics('environmentselector.direct_selection', {
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState(function () {
                _this.doChange([environment]);
                return {
                    selectedEnvs: new Set([environment]),
                };
            }, _this.doUpdate);
        };
        /**
         * Handler for when an environment is selected by the multiple select component
         * Does not initiate an "update"
         */
        _this.handleMultiSelect = function (environment) {
            _this.toggleSelected(environment);
        };
        return _this;
    }
    MultipleEnvironmentSelector.prototype.componentDidUpdate = function (prevProps) {
        // Need to sync state
        if (this.props.value !== prevProps.value) {
            this.syncSelectedStateFromProps();
        }
    };
    MultipleEnvironmentSelector.prototype.getEnvironments = function () {
        var _a = this.props, projects = _a.projects, selectedProjects = _a.selectedProjects;
        var environments = [];
        projects.forEach(function (project) {
            var projectId = parseInt(project.id, 10);
            // Include environments from:
            // - the requested projects
            // - all member projects if 'my projects' (empty list) is selected.
            // - all projects if -1 is the only selected project.
            if ((selectedProjects.length === 1 &&
                selectedProjects[0] === ALL_ACCESS_PROJECTS &&
                project.hasAccess) ||
                (selectedProjects.length === 0 && project.isMember) ||
                selectedProjects.includes(projectId)) {
                environments = environments.concat(project.environments);
            }
        });
        return uniq(environments);
    };
    MultipleEnvironmentSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, value = _a.value, loadingProjects = _a.loadingProjects;
        var environments = this.getEnvironments();
        var validatedValue = value.filter(function (env) { return environments.includes(env); });
        var summary = validatedValue.length
            ? "" + validatedValue.join(', ')
            : t('All Environments');
        return loadingProjects ? (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<IconWindow />} loading={loadingProjects} hasChanges={false} hasSelected={false} isOpen={false} locked={false}>
        {t('Loading\u2026')}
      </StyledHeaderItem>) : (<ClassNames>
        {function (_a) {
            var css = _a.css;
            return (<StyledDropdownAutoComplete alignMenu="left" allowActorToggle closeOnSelect blendCorner={false} searchPlaceholder={t('Filter environments')} onSelect={_this.handleSelect} onClose={_this.handleClose} maxHeight={500} rootClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n              position: relative;\n              display: flex;\n              left: -1px;\n            "], ["\n              position: relative;\n              display: flex;\n              left: -1px;\n            "])))} inputProps={{ style: { padding: 8, paddingLeft: 14 } }} emptyMessage={t('You have no environments')} noResultsMessage={t('No environments found')} virtualizedHeight={theme.headerSelectorRowHeight} emptyHidesInput menuFooter={function (_a) {
                var actions = _a.actions;
                return _this.state.hasChanges ? (<MultipleSelectorSubmitRow onSubmit={function () { return _this.handleUpdate(actions); }}/>) : null;
            }} items={environments.map(function (env) { return ({
                value: env,
                searchKey: env,
                label: function (_a) {
                    var inputValue = _a.inputValue;
                    return (<EnvironmentSelectorItem environment={env} inputValue={inputValue} isChecked={_this.state.selectedEnvs.has(env)} onMultiSelect={_this.handleMultiSelect}/>);
                },
            }); })}>
            {function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<IconWindow />} isOpen={isOpen} hasSelected={value && !!value.length} onClear={_this.handleClear} hasChanges={false} locked={false} loading={false} {...getActorProps()}>
                {summary}
              </StyledHeaderItem>);
            }}
          </StyledDropdownAutoComplete>);
        }}
      </ClassNames>);
    };
    MultipleEnvironmentSelector.contextTypes = {
        router: PropTypes.object,
    };
    MultipleEnvironmentSelector.defaultProps = {
        value: [],
    };
    return MultipleEnvironmentSelector;
}(React.PureComponent));
export default withApi(MultipleEnvironmentSelector);
var StyledHeaderItem = styled(HeaderItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var StyledDropdownAutoComplete = styled(DropdownAutoComplete)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  box-shadow: ", ";\n  border-radius: ", ";\n  margin-top: 0;\n  min-width: 100%;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  box-shadow: ", ";\n  border-radius: ", ";\n  margin-top: 0;\n  min-width: 100%;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadiusBottom; });
var EnvironmentSelectorItem = /** @class */ (function (_super) {
    __extends(EnvironmentSelectorItem, _super);
    function EnvironmentSelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleMultiSelect = function () {
            var _a = _this.props, environment = _a.environment, onMultiSelect = _a.onMultiSelect;
            onMultiSelect(environment);
        };
        _this.handleClick = function (e) {
            e.stopPropagation();
            _this.handleMultiSelect();
        };
        return _this;
    }
    EnvironmentSelectorItem.prototype.render = function () {
        var _a = this.props, environment = _a.environment, inputValue = _a.inputValue, isChecked = _a.isChecked;
        return (<GlobalSelectionHeaderRow data-test-id={"environment-" + environment} checked={isChecked} onCheckClick={this.handleClick}>
        <Highlight text={inputValue}>{environment}</Highlight>
      </GlobalSelectionHeaderRow>);
    };
    return EnvironmentSelectorItem;
}(React.PureComponent));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=multipleEnvironmentSelector.jsx.map