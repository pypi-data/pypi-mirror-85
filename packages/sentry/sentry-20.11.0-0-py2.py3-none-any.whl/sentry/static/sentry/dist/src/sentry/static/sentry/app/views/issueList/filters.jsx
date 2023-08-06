import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { PageHeader } from 'app/styles/organization';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { t } from 'app/locale';
import PageHeading from 'app/components/pageHeading';
import QueryCount from 'app/components/queryCount';
import Feature from 'app/components/acl/feature';
import space from 'app/styles/space';
import IssueListSearchBar from './searchBar';
import IssueListSortOptions from './sortOptions';
import SavedSearchSelector from './savedSearchSelector';
var IssueListFilters = /** @class */ (function (_super) {
    __extends(IssueListFilters, _super);
    function IssueListFilters() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSavedSearchSelect = function (savedSearch) {
            trackAnalyticsEvent({
                eventKey: 'organization_saved_search.selected',
                eventName: 'Organization Saved Search: Selected saved search',
                organization_id: _this.props.organization.id,
                query: savedSearch.query,
                search_type: 'issues',
                id: savedSearch.id ? parseInt(savedSearch.id, 10) : -1,
            });
            if (_this.props.onSavedSearchSelect) {
                _this.props.onSavedSearchSelect(savedSearch);
            }
        };
        return _this;
    }
    IssueListFilters.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, savedSearch = _a.savedSearch, queryCount = _a.queryCount, queryMaxCount = _a.queryMaxCount, query = _a.query, savedSearchList = _a.savedSearchList, isSearchDisabled = _a.isSearchDisabled, sort = _a.sort, onSidebarToggle = _a.onSidebarToggle, onSearch = _a.onSearch, onSavedSearchDelete = _a.onSavedSearchDelete, onSortChange = _a.onSortChange, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        return (<Feature features={['organizations:inbox']}>
        {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<PageHeader>
            {!hasFeature && (<PageHeading>
                {t('Issues')}
                <QueryCount count={queryCount} max={queryMaxCount}/>
              </PageHeading>)}

            <SearchContainer isInbox={hasFeature}>
              <IssueListSortOptions sort={sort} onSelect={onSortChange}/>

              <SearchSelectorContainer isInbox={hasFeature}>
                <SavedSearchSelector key={query} organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={_this.handleSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query}/>

                <IssueListSearchBar organization={organization} query={query || ''} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle}/>
              </SearchSelectorContainer>
            </SearchContainer>
          </PageHeader>);
        }}
      </Feature>);
    };
    IssueListFilters.contextTypes = {
        location: PropTypes.object,
    };
    return IssueListFilters;
}(React.Component));
var SearchContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  width: ", ";\n  flex-direction: ", ";\n"], ["\n  display: flex;\n  width: ", ";\n  flex-direction: ", ";\n"])), function (p) { return (p.isInbox ? '100%' : '70%'); }, function (p) { return (p.isInbox ? 'row-reverse' : 'row'); });
var SearchSelectorContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-grow: 1;\n\n  margin-right: ", ";\n  margin-left: ", ";\n"], ["\n  display: flex;\n  flex-grow: 1;\n\n  margin-right: ", ";\n  margin-left: ", ";\n"])), function (p) { return (p.isInbox ? space(1) : 0); }, function (p) { return (p.isInbox ? 0 : space(1)); });
export default IssueListFilters;
var templateObject_1, templateObject_2;
//# sourceMappingURL=filters.jsx.map