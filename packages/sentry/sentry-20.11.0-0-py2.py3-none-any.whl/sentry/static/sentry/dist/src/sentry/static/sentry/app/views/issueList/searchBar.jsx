import { __awaiter, __extends, __generator, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { SavedSearchType } from 'app/types';
import { fetchRecentSearches } from 'app/actionCreators/savedSearches';
import SentryTypes from 'app/sentryTypes';
import SmartSearchBar from 'app/components/smartSearchBar';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var SEARCH_ITEMS = [
    {
        title: t('Tag'),
        desc: 'browser:"Chrome 34", has:browser',
        value: 'browser:',
        type: 'default',
    },
    {
        title: t('Status'),
        desc: 'is:resolved, unresolved, ignored, assigned, unassigned',
        value: 'is:',
        type: 'default',
    },
    {
        title: t('Time or Count'),
        desc: 'firstSeen, lastSeen, event.timestamp, timesSeen',
        value: '',
        type: 'default',
    },
    {
        title: t('Assigned'),
        desc: 'assigned:[me|user@example.com]',
        value: 'assigned:',
        type: 'default',
    },
    {
        title: t('Bookmarked By'),
        desc: 'bookmarks:[me|user@example.com]',
        value: 'bookmarks:',
        type: 'default',
    },
];
var IssueListSearchBar = /** @class */ (function (_super) {
    __extends(IssueListSearchBar, _super);
    function IssueListSearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            defaultSearchItems: [SEARCH_ITEMS, []],
            recentSearches: [],
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var resp;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.props.api.clear();
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        resp = _a.sent();
                        this.setState({
                            defaultSearchItems: [
                                SEARCH_ITEMS,
                                resp
                                    ? resp.map(function (query) { return ({
                                        desc: query,
                                        value: query,
                                        type: 'recent-search',
                                    }); })
                                    : [],
                            ],
                            recentSearches: resp,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * @returns array of tag values that substring match `query`
         */
        _this.getTagValues = function (tag, query) { return __awaiter(_this, void 0, void 0, function () {
            var tagValueLoader, values;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        tagValueLoader = this.props.tagValueLoader;
                        return [4 /*yield*/, tagValueLoader(tag.key, query)];
                    case 1:
                        values = _a.sent();
                        return [2 /*return*/, values.map(function (_a) {
                                var value = _a.value;
                                return value;
                            })];
                }
            });
        }); };
        _this.getRecentSearches = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, recent;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, fetchRecentSearches(api, organization.slug, SavedSearchType.ISSUE)];
                    case 1:
                        recent = _c.sent();
                        return [2 /*return*/, (_b = recent === null || recent === void 0 ? void 0 : recent.map(function (_a) {
                                var query = _a.query;
                                return query;
                            })) !== null && _b !== void 0 ? _b : []];
                }
            });
        }); };
        _this.handleSavedRecentSearch = function () {
            // Reset recent searches
            _this.fetchData();
        };
        return _this;
    }
    IssueListSearchBar.prototype.componentDidMount = function () {
        // Ideally, we would fetch on demand (e.g. when input gets focus)
        // but `<SmartSearchBar>` is a bit complicated and this is the easiest route
        this.fetchData();
    };
    IssueListSearchBar.prototype.render = function () {
        var _a = this.props, _ = _a.tagValueLoader, savedSearch = _a.savedSearch, onSidebarToggle = _a.onSidebarToggle, props = __rest(_a, ["tagValueLoader", "savedSearch", "onSidebarToggle"]);
        return (<SmartSearchBarNoLeftCorners hasPinnedSearch hasRecentSearches hasSearchBuilder canCreateSavedSearch maxSearchItems={5} savedSearchType={SavedSearchType.ISSUE} onGetTagValues={this.getTagValues} defaultSearchItems={this.state.defaultSearchItems} onSavedRecentSearch={this.handleSavedRecentSearch} onSidebarToggle={onSidebarToggle} pinnedSearch={(savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.isPinned) ? savedSearch : undefined} {...props}/>);
    };
    IssueListSearchBar.propTypes = {
        savedSearch: SentryTypes.SavedSearch,
        tagValueLoader: PropTypes.func.isRequired,
        onSidebarToggle: PropTypes.func,
    };
    return IssueListSearchBar;
}(React.Component));
var SmartSearchBarNoLeftCorners = styled(SmartSearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: ", ";\n  flex-grow: 1;\n"], ["\n  border-radius: ",
    ";\n  flex-grow: 1;\n"])), function (p) {
    return p.isOpen
        ? "0 " + p.theme.borderRadius + " 0 0"
        : "0 " + p.theme.borderRadius + " " + p.theme.borderRadius + " 0";
});
export default withApi(withOrganization(IssueListSearchBar));
var templateObject_1;
//# sourceMappingURL=searchBar.jsx.map