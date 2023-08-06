import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import omit from 'lodash/omit';
import ErrorBoundary from 'app/components/errorBoundary';
import EventDataSection from 'app/components/events/eventDataSection';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { t } from 'app/locale';
import space from 'app/styles/space';
import SearchBar from 'app/components/searchBar';
import Button from 'app/components/button';
import { IconWarning } from 'app/icons/iconWarning';
import { defined } from 'app/utils';
import { BreadcrumbType, BreadcrumbLevelType, } from './types';
import transformCrumbs from './transformCrumbs';
import Filter from './filter';
import List from './list';
import Level from './level';
import Icon from './icon';
import { aroundContentStyle } from './styles';
var ISO_STRING_DATE_AND_TIME_DIVISION = 10;
var Breadcrumbs = /** @class */ (function (_super) {
    __extends(Breadcrumbs, _super);
    function Breadcrumbs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            breadcrumbs: [],
            filteredByFilter: [],
            filteredBySearch: [],
            filterOptions: [[], []],
            displayRelativeTime: false,
        };
        _this.handleSearch = function (value) {
            _this.setState(function (prevState) { return ({
                searchTerm: value,
                filteredBySearch: _this.filterBySearch(value, prevState.filteredByFilter),
            }); });
        };
        _this.handleFilter = function (filterOptions) {
            var hasCheckedType = filterOptions[0].some(function (filterOption) { return filterOption.isChecked; });
            var hasCheckedLevel = filterOptions[1].some(function (filterOption) { return filterOption.isChecked; });
            var filteredCrumbs = _this.getFilteredCrumbs(hasCheckedType, hasCheckedLevel, filterOptions);
            _this.setState(function (prevState) { return ({
                filterOptions: filterOptions,
                filteredByFilter: filteredCrumbs,
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, filteredCrumbs),
            }); });
        };
        _this.handleSwitchTimeFormat = function () {
            _this.setState(function (prevState) { return ({
                displayRelativeTime: !prevState.displayRelativeTime,
            }); });
        };
        _this.handleCleanSearch = function () {
            _this.setState({
                searchTerm: '',
            });
        };
        _this.handleResetFilter = function () {
            _this.setState(function (prevState) { return ({
                filteredByFilter: prevState.breadcrumbs,
                filterOptions: prevState.filterOptions.map(function (filterOption) {
                    return filterOption.map(function (option) { return (__assign(__assign({}, option), { isChecked: false })); });
                }),
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, prevState.breadcrumbs),
            }); });
        };
        return _this;
    }
    Breadcrumbs.prototype.componentDidMount = function () {
        this.loadBreadcrumbs();
    };
    Breadcrumbs.prototype.loadBreadcrumbs = function () {
        var _a;
        var data = this.props.data;
        var breadcrumbs = data.values;
        // Add the error event as the final (virtual) breadcrumb
        var virtualCrumb = this.getVirtualCrumb(breadcrumbs[0]);
        if (virtualCrumb) {
            breadcrumbs = __spread(breadcrumbs, [virtualCrumb]);
        }
        var transformedCrumbs = transformCrumbs(breadcrumbs);
        var filterOptions = this.getFilterOptions(transformedCrumbs);
        this.setState({
            breadcrumbs: transformedCrumbs,
            filteredByFilter: transformedCrumbs,
            filteredBySearch: transformedCrumbs,
            filterOptions: filterOptions,
            relativeTime: (_a = transformedCrumbs[transformedCrumbs.length - 1]) === null || _a === void 0 ? void 0 : _a.timestamp,
        });
    };
    Breadcrumbs.prototype.getFilterOptions = function (breadcrumbs) {
        var types = this.getFilterTypes(breadcrumbs);
        var levels = this.getFilterLevels(types);
        return [types, levels];
    };
    Breadcrumbs.prototype.getFilterTypes = function (breadcrumbs) {
        var filterTypes = [];
        var _loop_1 = function (index) {
            var breadcrumb = breadcrumbs[index];
            var foundFilterType = filterTypes.findIndex(function (f) { return f.type === breadcrumb.type; });
            if (foundFilterType === -1) {
                filterTypes.push({
                    type: breadcrumb.type,
                    description: breadcrumb.description,
                    symbol: <Icon {...omit(breadcrumb, 'description')} size="xs"/>,
                    levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                    isChecked: false,
                });
                return "continue";
            }
            if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                filterTypes[foundFilterType].levels.push(breadcrumb.level);
            }
        };
        for (var index in breadcrumbs) {
            _loop_1(index);
        }
        return filterTypes;
    };
    Breadcrumbs.prototype.getFilterLevels = function (types) {
        var filterLevels = [];
        for (var indexType in types) {
            var _loop_2 = function (indexLevel) {
                var level = types[indexType].levels[indexLevel];
                if (filterLevels.some(function (f) { return f.type === level; })) {
                    return "continue";
                }
                filterLevels.push({
                    type: level,
                    symbol: <Level level={level}/>,
                    isChecked: false,
                });
            };
            for (var indexLevel in types[indexType].levels) {
                _loop_2(indexLevel);
            }
        }
        return filterLevels;
    };
    Breadcrumbs.prototype.moduleToCategory = function (module) {
        if (!module) {
            return undefined;
        }
        var match = module.match(/^.*\/(.*?)(:\d+)/);
        if (!match) {
            return module.split(/./)[0];
        }
        return match[1];
    };
    Breadcrumbs.prototype.getVirtualCrumb = function (breadcrumb) {
        var event = this.props.event;
        var timestamp = (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.timestamp) && event.dateCreated
            ? "" + breadcrumb.timestamp.slice(0, ISO_STRING_DATE_AND_TIME_DIVISION) + event.dateCreated.slice(ISO_STRING_DATE_AND_TIME_DIVISION)
            : undefined;
        var exception = event.entries.find(function (entry) { return entry.type === BreadcrumbType.EXCEPTION; });
        if (!exception && !event.message) {
            return undefined;
        }
        if (exception) {
            var _a = exception.data.values[0], type = _a.type, value = _a.value, mdl = _a.module;
            return {
                type: BreadcrumbType.ERROR,
                level: BreadcrumbLevelType.ERROR,
                category: this.moduleToCategory(mdl) || 'exception',
                data: {
                    type: type,
                    value: value,
                },
                timestamp: timestamp,
            };
        }
        var levelTag = (event.tags || []).find(function (tag) { return tag.key === 'level'; });
        return {
            type: BreadcrumbType.INFO,
            level: (levelTag === null || levelTag === void 0 ? void 0 : levelTag.value) || BreadcrumbLevelType.UNDEFINED,
            category: 'message',
            message: event.message,
            timestamp: timestamp,
        };
    };
    Breadcrumbs.prototype.filterBySearch = function (searchTerm, breadcrumbs) {
        if (!searchTerm.trim()) {
            return breadcrumbs;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        var searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        return breadcrumbs.filter(function (obj) {
            return Object.keys(pick(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(function (key) {
                var info = obj[key];
                if (!defined(info) || !String(info).trim()) {
                    return false;
                }
                return JSON.stringify(info)
                    .replace(/((^")|("$))/g, '')
                    .toLocaleLowerCase()
                    .trim()
                    .includes(searchFor);
            });
        });
    };
    Breadcrumbs.prototype.filterCrumbsBy = function (type, breadcrumbs, filterOptions) {
        return breadcrumbs.filter(function (b) {
            var crumbProperty = b[type];
            if (!crumbProperty) {
                return true;
            }
            var foundInFilterOptions = filterOptions.find(function (f) { return f.type === crumbProperty; });
            if (foundInFilterOptions) {
                return foundInFilterOptions.isChecked;
            }
            return false;
        });
    };
    Breadcrumbs.prototype.getFilteredCrumbs = function (hasCheckedType, hasCheckedLevel, filterOptions) {
        var breadcrumbs = this.state.breadcrumbs;
        if (!hasCheckedType && !hasCheckedLevel) {
            return breadcrumbs;
        }
        if (hasCheckedType) {
            var filteredCrumbsByType = this.filterCrumbsBy('type', breadcrumbs, filterOptions[0]);
            if (hasCheckedLevel) {
                var filteredCrumbsByLevel_1 = this.filterCrumbsBy('level', filteredCrumbsByType, filterOptions[1]);
                return filteredCrumbsByLevel_1;
            }
            return filteredCrumbsByType;
        }
        var filteredCrumbsByLevel = this.filterCrumbsBy('level', breadcrumbs, filterOptions[1]);
        return filteredCrumbsByLevel;
    };
    Breadcrumbs.prototype.render = function () {
        var _a = this.props, type = _a.type, event = _a.event, orgId = _a.orgId;
        var _b = this.state, filterOptions = _b.filterOptions, searchTerm = _b.searchTerm, filteredBySearch = _b.filteredBySearch, displayRelativeTime = _b.displayRelativeTime, relativeTime = _b.relativeTime;
        return (<StyledEventDataSection type={type} title={<GuideAnchor target="breadcrumbs" position="bottom">
            <h3>{t('Breadcrumbs')}</h3>
          </GuideAnchor>} actions={<Search>
            <Filter onFilter={this.handleFilter} options={filterOptions}/>
            <StyledSearchBar placeholder={t('Search breadcrumbs\u2026')} onSearch={this.handleSearch}/>
          </Search>} wrapTitle={false} isCentered>
        {filteredBySearch.length > 0 ? (<ErrorBoundary>
            <List breadcrumbs={filteredBySearch} event={event} orgId={orgId} onSwitchTimeFormat={this.handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm} relativeTime={relativeTime} // relativeTime has to be always available, as the last item timestamp is the event created time
        />
          </ErrorBoundary>) : (<StyledEmptyMessage icon={<IconWarning size="xl"/>} action={<Button onClick={this.handleResetFilter} priority="primary">
                {t('Reset Filter')}
              </Button>}>
            {t('Sorry, no breadcrumbs match your search query.')}
          </StyledEmptyMessage>)}
      </StyledEventDataSection>);
    };
    return Breadcrumbs;
}(React.Component));
export default Breadcrumbs;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StyledEmptyMessage = styled(EmptyMessage)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), aroundContentStyle);
var Search = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space(1), function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
var StyledSearchBar = styled(SearchBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 100%;\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  width: 100%;\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map