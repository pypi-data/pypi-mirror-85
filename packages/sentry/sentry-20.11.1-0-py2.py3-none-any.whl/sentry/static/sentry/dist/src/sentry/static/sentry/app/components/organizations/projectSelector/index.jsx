import { __assign, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import sortBy from 'lodash/sortBy';
import { t } from 'app/locale';
import space from 'app/styles/space';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import Button from 'app/components/button';
import theme from 'app/utils/theme';
import { IconAdd } from 'app/icons';
import SelectorItem from './selectorItem';
var ProjectSelector = function (_a) {
    var children = _a.children, organization = _a.organization, menuFooter = _a.menuFooter, className = _a.className, rootClassName = _a.rootClassName, onClose = _a.onClose, onFilterChange = _a.onFilterChange, onScroll = _a.onScroll, searching = _a.searching, paginated = _a.paginated, multiProjects = _a.multiProjects, onSelect = _a.onSelect, onMultiSelect = _a.onMultiSelect, _b = _a.multi, multi = _b === void 0 ? false : _b, _c = _a.selectedProjects, selectedProjects = _c === void 0 ? [] : _c, props = __rest(_a, ["children", "organization", "menuFooter", "className", "rootClassName", "onClose", "onFilterChange", "onScroll", "searching", "paginated", "multiProjects", "onSelect", "onMultiSelect", "multi", "selectedProjects"]);
    var getProjects = function () {
        var _a = props.nonMemberProjects, nonMemberProjects = _a === void 0 ? [] : _a;
        return [
            sortBy(multiProjects, function (project) { return [
                !selectedProjects.find(function (selectedProject) { return selectedProject.slug === project.slug; }),
                !project.isBookmarked,
                project.slug,
            ]; }),
            sortBy(nonMemberProjects, function (project) { return [project.slug]; }),
        ];
    };
    var _d = __read(getProjects(), 2), projects = _d[0], nonMemberProjects = _d[1];
    var handleSelect = function (_a) {
        var project = _a.value;
        onSelect(project);
    };
    var handleMultiSelect = function (project, event) {
        if (!onMultiSelect) {
            // eslint-disable-next-line no-console
            console.error('ProjectSelector is a controlled component but `onMultiSelect` callback is not defined');
            return;
        }
        var selectedProjectsMap = new Map(selectedProjects.map(function (p) { return [p.slug, p]; }));
        if (selectedProjectsMap.has(project.slug)) {
            // unselected a project
            selectedProjectsMap.delete(project.slug);
            onMultiSelect(Array.from(selectedProjectsMap.values()), event);
            return;
        }
        selectedProjectsMap.set(project.slug, project);
        onMultiSelect(Array.from(selectedProjectsMap.values()), event);
    };
    var getProjectItem = function (project) { return ({
        value: project,
        searchKey: project.slug,
        label: function (_a) {
            var inputValue = _a.inputValue;
            return (<SelectorItem project={project} organization={organization} multi={multi} inputValue={inputValue} isChecked={!!selectedProjects.find(function (_a) {
                var slug = _a.slug;
                return slug === project.slug;
            })} onMultiSelect={handleMultiSelect}/>);
        },
    }); };
    var getItems = function (hasProjects) {
        if (!hasProjects) {
            return [];
        }
        return [
            {
                hideGroupLabel: true,
                items: projects.map(getProjectItem),
            },
            {
                hideGroupLabel: nonMemberProjects.length === 0,
                itemSize: 'small',
                id: 'no-membership-header',
                label: <Label>{t("Projects I don't belong to")}</Label>,
                items: nonMemberProjects.map(getProjectItem),
            },
        ];
    };
    var hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length) || !!(nonMemberProjects === null || nonMemberProjects === void 0 ? void 0 : nonMemberProjects.length);
    var newProjectUrl = "/organizations/" + organization.slug + "/projects/new/";
    var hasProjectWrite = organization.access.includes('project:write');
    return (<DropdownAutoComplete blendCorner={false} searchPlaceholder={t('Filter projects')} onSelect={handleSelect} onClose={onClose} onChange={onFilterChange} busyItemsStillVisible={searching} onScroll={onScroll} maxHeight={500} inputProps={{ style: { padding: 8, paddingLeft: 10 } }} rootClassName={rootClassName} className={className} emptyMessage={t('You have no projects')} noResultsMessage={t('No projects found')} virtualizedHeight={theme.headerSelectorRowHeight} virtualizedLabelHeight={theme.headerSelectorLabelHeight} emptyHidesInput={!paginated} inputActions={<AddButton disabled={!hasProjectWrite} to={newProjectUrl} size="xsmall" icon={<IconAdd size="xs" isCircled/>} title={!hasProjectWrite ? t("You don't have permission to add a project") : undefined}>
          {t('Project')}
        </AddButton>} menuFooter={function (renderProps) {
        var renderedFooter = typeof menuFooter === 'function' ? menuFooter(renderProps) : menuFooter;
        var showCreateProjectButton = !hasProjects && hasProjectWrite;
        if (!renderedFooter && !showCreateProjectButton) {
            return null;
        }
        return (<React.Fragment>
            {showCreateProjectButton && (<CreateProjectButton priority="primary" size="small" to={newProjectUrl}>
                {t('Create project')}
              </CreateProjectButton>)}
            {renderedFooter}
          </React.Fragment>);
    }} items={getItems(hasProjects)} allowActorToggle closeOnSelect>
      {function (renderProps) { return children(__assign(__assign({}, renderProps), { selectedProjects: selectedProjects })); }}
    </DropdownAutoComplete>);
};
export default ProjectSelector;
var Label = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var AddButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin: 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  display: block;\n  margin: 0 ", ";\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
var CreateProjectButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: block;\n  text-align: center;\n  margin: ", " 0;\n"], ["\n  display: block;\n  text-align: center;\n  margin: ", " 0;\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map