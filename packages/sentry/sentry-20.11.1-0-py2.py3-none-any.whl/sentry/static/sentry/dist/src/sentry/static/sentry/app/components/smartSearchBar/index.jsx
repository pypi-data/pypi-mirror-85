import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import { ClassNames } from '@emotion/core';
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import debounce from 'lodash/debounce';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { callIfFunction } from 'app/utils/callIfFunction';
import { defined } from 'app/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateSavedSearchButton from 'app/views/issueList/createSavedSearchButton';
import DropdownLink from 'app/components/dropdownLink';
import { IconEllipsis, IconSearch, IconSliders, IconClose, IconPin } from 'app/icons';
import MemberListStore from 'app/stores/memberListStore';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import { SavedSearchType } from 'app/types';
import { fetchRecentSearches, pinSearch, saveRecentSearch, unpinSearch, } from 'app/actionCreators/savedSearches';
import { DEFAULT_DEBOUNCE_DURATION, MAX_AUTOCOMPLETE_RELEASES, NEGATION_OPERATOR, } from 'app/constants';
import SearchDropdown from './searchDropdown';
import { addSpace, removeSpace, createSearchGroups, filterSearchGroupsByIndex, } from './utils';
var DROPDOWN_BLUR_DURATION = 200;
var getMediaQuery = function (size, type) { return "\n  display: " + type + ";\n\n  @media (min-width: " + size + ") {\n    display: " + (type === 'none' ? 'block' : 'none') + ";\n  }\n"; };
var getInputButtonStyles = function (p) { return "\n  color: " + (p.isActive ? theme.blue300 : theme.gray300) + ";\n  margin-left: " + space(0.5) + ";\n  width: 18px;\n\n  &,\n  &:hover,\n  &:focus {\n    background: transparent;\n  }\n\n  &:hover {\n    color: " + theme.gray400 + ";\n  }\n\n  " + (p.collapseIntoEllipsisMenu &&
    getMediaQuery(theme.breakpoints[p.collapseIntoEllipsisMenu], 'none')) + ";\n"; };
var getDropdownElementStyles = function (p) { return "\n  padding: 0 " + space(1) + " " + (p.last ? null : space(0.5)) + ";\n  margin-bottom: " + (p.last ? null : space(0.5)) + ";\n  display: none;\n  color: " + theme.textColor + ";\n  align-items: center;\n  min-width: 190px;\n  height: 38px;\n  padding-left: " + space(1.5) + ";\n  padding-right: " + space(1.5) + ";\n\n  &,\n  &:hover,\n  &:focus {\n    border-bottom: " + (p.last ? null : "1px solid " + theme.border) + ";\n    border-radius: 0;\n  }\n\n  &:hover {\n    color: " + theme.blue300 + ";\n  }\n  & > svg {\n    margin-right: " + space(1) + ";\n  }\n\n  " + (p.showBelowMediaQuery &&
    getMediaQuery(theme.breakpoints[p.showBelowMediaQuery], 'flex')) + "\n"; };
var SmartSearchBar = /** @class */ (function (_super) {
    __extends(SmartSearchBar, _super);
    function SmartSearchBar() {
        var _a;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.state = {
            query: _this.props.query !== null
                ? addSpace(_this.props.query)
                : (_a = _this.props.defaultQuery) !== null && _a !== void 0 ? _a : '',
            searchTerm: '',
            searchGroups: [],
            flatSearchItems: [],
            activeSearchItem: -1,
            tags: {},
            dropdownVisible: false,
            loading: false,
        };
        /**
         * Ref to the search element itself
         */
        _this.searchInput = React.createRef();
        _this.blur = function () {
            if (!_this.searchInput.current) {
                return;
            }
            _this.searchInput.current.blur();
        };
        _this.onSubmit = function (evt) {
            var _a = _this.props, organization = _a.organization, savedSearchType = _a.savedSearchType;
            evt.preventDefault();
            trackAnalyticsEvent({
                eventKey: 'search.searched',
                eventName: 'Search: Performed search',
                organization_id: organization.id,
                query: removeSpace(_this.state.query),
                search_type: savedSearchType === 0 ? 'issues' : 'events',
                search_source: 'main_search',
            });
            _this.doSearch();
        };
        _this.doSearch = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, onSearch, onSavedRecentSearch, api, organization, savedSearchType, query, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, onSearch = _a.onSearch, onSavedRecentSearch = _a.onSavedRecentSearch, api = _a.api, organization = _a.organization, savedSearchType = _a.savedSearchType;
                        this.blur();
                        query = removeSpace(this.state.query);
                        callIfFunction(onSearch, query);
                        // Only save recent search query if we have a savedSearchType (also 0 is a valid value)
                        // Do not save empty string queries (i.e. if they clear search)
                        if (typeof savedSearchType === 'undefined' || !query) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, saveRecentSearch(api, organization.slug, savedSearchType, query)];
                    case 2:
                        _b.sent();
                        if (onSavedRecentSearch) {
                            onSavedRecentSearch(query);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        // Silently capture errors if it fails to save
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.clearSearch = function () {
            return _this.setState({ query: '' }, function () {
                return callIfFunction(_this.props.onSearch, _this.state.query);
            });
        };
        _this.onQueryFocus = function () { return _this.setState({ dropdownVisible: true }); };
        _this.onQueryBlur = function (e) {
            // wait before closing dropdown in case blur was a result of clicking a
            // menu option
            var value = e.target.value;
            var blurHandler = function () {
                _this.blurTimeout = undefined;
                _this.setState({ dropdownVisible: false });
                callIfFunction(_this.props.onBlur, value);
            };
            _this.blurTimeout = window.setTimeout(blurHandler, DROPDOWN_BLUR_DURATION);
        };
        _this.onQueryChange = function (evt) {
            _this.setState({ query: evt.target.value }, _this.updateAutoCompleteItems);
            callIfFunction(_this.props.onChange, evt.target.value, evt);
        };
        _this.onInputClick = function () { return _this.updateAutoCompleteItems(); };
        /**
         * Handle keyboard navigation
         */
        _this.onKeyDown = function (evt) {
            var _a, _b, _c;
            var onKeyDown = _this.props.onKeyDown;
            var key = evt.key;
            callIfFunction(onKeyDown, evt);
            if (!_this.state.searchGroups.length) {
                return;
            }
            var useFormWrapper = _this.props.useFormWrapper;
            var isSelectingDropdownItems = _this.state.activeSearchItem !== -1;
            if (key === 'ArrowDown' || key === 'ArrowUp') {
                evt.preventDefault();
                var _d = _this.state, flatSearchItems = _d.flatSearchItems, activeSearchItem = _d.activeSearchItem;
                var searchGroups = __spread(_this.state.searchGroups);
                var _e = __read(isSelectingDropdownItems
                    ? filterSearchGroupsByIndex(searchGroups, activeSearchItem)
                    : [], 2), groupIndex = _e[0], childrenIndex = _e[1];
                // Remove the previous 'active' property
                if (typeof groupIndex !== 'undefined') {
                    if (childrenIndex !== undefined && ((_b = (_a = searchGroups[groupIndex]) === null || _a === void 0 ? void 0 : _a.children) === null || _b === void 0 ? void 0 : _b[childrenIndex])) {
                        delete searchGroups[groupIndex].children[childrenIndex].active;
                    }
                }
                var currIndex = isSelectingDropdownItems ? activeSearchItem : 0;
                var totalItems = flatSearchItems.length;
                // Move the selected index up/down
                var nextActiveSearchItem = key === 'ArrowUp'
                    ? (currIndex - 1 + totalItems) % totalItems
                    : isSelectingDropdownItems
                        ? (currIndex + 1) % totalItems
                        : 0;
                var _f = __read(filterSearchGroupsByIndex(searchGroups, nextActiveSearchItem), 2), nextGroupIndex = _f[0], nextChildrenIndex = _f[1];
                // Make sure search items exist (e.g. both groups could be empty) and
                // attach the 'active' property to the item
                if (nextGroupIndex !== undefined &&
                    nextChildrenIndex !== undefined && ((_c = searchGroups[nextGroupIndex]) === null || _c === void 0 ? void 0 : _c.children)) {
                    searchGroups[nextGroupIndex].children[nextChildrenIndex] = __assign(__assign({}, searchGroups[nextGroupIndex].children[nextChildrenIndex]), { active: true });
                }
                _this.setState({ searchGroups: searchGroups, activeSearchItem: nextActiveSearchItem });
            }
            if ((key === 'Tab' || key === 'Enter') && isSelectingDropdownItems) {
                evt.preventDefault();
                var _g = _this.state, activeSearchItem = _g.activeSearchItem, searchGroups = _g.searchGroups;
                var _h = __read(filterSearchGroupsByIndex(searchGroups, activeSearchItem), 2), groupIndex = _h[0], childrenIndex = _h[1];
                var item = groupIndex !== undefined &&
                    childrenIndex !== undefined &&
                    searchGroups[groupIndex].children[childrenIndex];
                if (item && !_this.isDefaultDropdownItem(item)) {
                    _this.onAutoComplete(item.value, item);
                }
                return;
            }
            if (key === 'Enter') {
                if (!useFormWrapper && !isSelectingDropdownItems) {
                    // If enter is pressed, and we are not wrapping input in a `<form>`,
                    // and we are not selecting an item from the dropdown, then we should
                    // consider the user as finished selecting and perform a "search" since
                    // there is no `<form>` to catch and call `this.onSubmit`
                    _this.doSearch();
                }
                return;
            }
        };
        _this.onKeyUp = function (evt) {
            // Other keys are managed at onKeyDown function
            if (evt.key !== 'Escape') {
                return;
            }
            evt.preventDefault();
            var isSelectingDropdownItems = _this.state.activeSearchItem > -1;
            if (!isSelectingDropdownItems) {
                _this.blur();
                return;
            }
            var _a = _this.state, searchGroups = _a.searchGroups, activeSearchItem = _a.activeSearchItem;
            var _b = __read(isSelectingDropdownItems
                ? filterSearchGroupsByIndex(searchGroups, activeSearchItem)
                : [], 2), groupIndex = _b[0], childrenIndex = _b[1];
            if (groupIndex !== undefined && childrenIndex !== undefined) {
                delete searchGroups[groupIndex].children[childrenIndex].active;
            }
            _this.setState({
                activeSearchItem: -1,
                searchGroups: __spread(_this.state.searchGroups),
            });
        };
        _this.getCursorPosition = function () {
            var _a;
            if (!_this.searchInput.current) {
                return -1;
            }
            return (_a = _this.searchInput.current.selectionStart) !== null && _a !== void 0 ? _a : -1;
        };
        /**
         * Returns array of possible key values that substring match `query`
         */
        _this.getTagKeys = function (query) {
            var _a;
            var prepareQuery = _this.props.prepareQuery;
            var supportedTags = (_a = _this.props.supportedTags) !== null && _a !== void 0 ? _a : {};
            // Return all if query is empty
            var tagKeys = Object.keys(supportedTags).map(function (key) { return key + ":"; });
            if (query) {
                var preparedQuery_1 = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
                tagKeys = tagKeys.filter(function (key) { return key.indexOf(preparedQuery_1) > -1; });
            }
            // If the environment feature is active and excludeEnvironment = true
            // then remove the environment key
            if (_this.props.excludeEnvironment) {
                tagKeys = tagKeys.filter(function (key) { return key !== 'environment:'; });
            }
            return tagKeys.map(function (value) { return ({ value: value, desc: value }); });
        };
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        _this.getTagValues = debounce(function (tag, query) { return __awaiter(_this, void 0, void 0, function () {
            var location, endpointParams, values, err_2, noValueQuery;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        // Strip double quotes if there are any
                        query = query.replace(/"/g, '').trim();
                        if (!this.props.onGetTagValues) {
                            return [2 /*return*/, []];
                        }
                        if (this.state.noValueQuery !== undefined &&
                            query.startsWith(this.state.noValueQuery)) {
                            return [2 /*return*/, []];
                        }
                        location = this.context.router.location;
                        endpointParams = getParams(location.query);
                        this.setState({ loading: true });
                        values = [];
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.onGetTagValues(tag, query, endpointParams)];
                    case 2:
                        values = _a.sent();
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _a.sent();
                        this.setState({ loading: false });
                        Sentry.captureException(err_2);
                        return [2 /*return*/, []];
                    case 4:
                        if (tag.key === 'release' && !values.includes('latest')) {
                            values.push('latest');
                        }
                        noValueQuery = values.length === 0 && query.length > 0 ? query : undefined;
                        this.setState({ noValueQuery: noValueQuery });
                        return [2 /*return*/, values.map(function (value) {
                                // Wrap in quotes if there is a space
                                var escapedValue = value.includes(' ') || value.includes('"')
                                    ? "\"" + value.replace(/"/g, '\\"') + "\""
                                    : value;
                                return { value: escapedValue, desc: escapedValue, type: 'tag-value' };
                            })];
                }
            });
        }); }, DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with results
         */
        _this.getPredefinedTagValues = function (tag, query) {
            var _a;
            return ((_a = tag.values) !== null && _a !== void 0 ? _a : [])
                .filter(function (value) { return value.indexOf(query) > -1; })
                .map(function (value) { return ({
                value: value,
                desc: value,
                type: 'tag-value',
            }); });
        };
        /**
         * Get recent searches
         */
        _this.getRecentSearches = debounce(function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, savedSearchType, hasRecentSearches, onGetRecentSearches, fetchFn;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, savedSearchType = _a.savedSearchType, hasRecentSearches = _a.hasRecentSearches, onGetRecentSearches = _a.onGetRecentSearches;
                        // `savedSearchType` can be 0
                        if (!defined(savedSearchType) || !hasRecentSearches) {
                            return [2 /*return*/, []];
                        }
                        fetchFn = onGetRecentSearches || this.fetchRecentSearches;
                        return [4 /*yield*/, fetchFn(this.state.query)];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        }); }, DEFAULT_DEBOUNCE_DURATION, { leading: true });
        _this.fetchRecentSearches = function (fullQuery) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, savedSearchType, recentSearches, e_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, savedSearchType = _a.savedSearchType;
                        if (savedSearchType === undefined) {
                            return [2 /*return*/, []];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchRecentSearches(api, organization.slug, savedSearchType, fullQuery)];
                    case 2:
                        recentSearches = _b.sent();
                        // If `recentSearches` is undefined or not an array, the function will
                        // return an array anyway
                        return [2 /*return*/, recentSearches.map(function (searches) { return ({
                                desc: searches.query,
                                value: searches.query,
                                type: 'recent-search',
                            }); })];
                    case 3:
                        e_1 = _b.sent();
                        Sentry.captureException(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/, []];
                }
            });
        }); };
        _this.getReleases = debounce(function (tag, query) { return __awaiter(_this, void 0, void 0, function () {
            var releasePromise, tags, tagValues, releases, releaseValues;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        releasePromise = this.fetchReleases(query);
                        tags = this.getPredefinedTagValues(tag, query);
                        tagValues = tags.map(function (v) { return (__assign(__assign({}, v), { type: 'first-release' })); });
                        return [4 /*yield*/, releasePromise];
                    case 1:
                        releases = _a.sent();
                        releaseValues = releases.map(function (r) { return ({
                            value: r.shortVersion,
                            desc: r.shortVersion,
                            type: 'first-release',
                        }); });
                        return [2 /*return*/, __spread(tagValues, releaseValues)];
                }
            });
        }); }, DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Fetches latest releases from a organization/project. Returns an empty array
         * if an error is encountered.
         */
        _this.fetchReleases = function (releaseVersion) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, location, project, url, fetchQuery, e_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        location = this.context.router.location;
                        project = location && location.query ? location.query.projectId : undefined;
                        url = "/organizations/" + organization.slug + "/releases/";
                        fetchQuery = {
                            per_page: MAX_AUTOCOMPLETE_RELEASES,
                        };
                        if (releaseVersion) {
                            fetchQuery.query = releaseVersion;
                        }
                        if (project) {
                            fetchQuery.project = project;
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(url, {
                                method: 'GET',
                                query: fetchQuery,
                            })];
                    case 2: return [2 /*return*/, _b.sent()];
                    case 3:
                        e_2 = _b.sent();
                        addErrorMessage(t('Unable to fetch releases'));
                        Sentry.captureException(e_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/, []];
                }
            });
        }); };
        _this.updateAutoCompleteItems = function () { return __awaiter(_this, void 0, void 0, function () {
            var cursor, query, lastTermIndex, terms, _a, defaultSearchItems, defaultRecentItems, tagKeys, recentSearches_1, last, autoCompleteItems, matchValue, tagName, index, recentSearches_2, _b, prepareQuery, excludeEnvironment, supportedTags, preparedQuery, filteredSearchGroups, tag, fetchTagValuesFn, _c, tagValues, recentSearches;
            var _d, _e;
            return __generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        if (this.blurTimeout) {
                            clearTimeout(this.blurTimeout);
                            this.blurTimeout = undefined;
                        }
                        cursor = this.getCursorPosition();
                        query = this.state.query;
                        // Don't continue if the query hasn't changed
                        if (query === this.state.previousQuery) {
                            return [2 /*return*/];
                        }
                        this.setState({ previousQuery: query });
                        lastTermIndex = SmartSearchBar.getLastTermIndex(query, cursor);
                        terms = SmartSearchBar.getQueryTerms(query, lastTermIndex);
                        if (!(!terms || // no terms
                            terms.length === 0 || // no terms
                            (terms.length === 1 && terms[0] === this.props.defaultQuery) || // default term
                            /^\s+$/.test(query.slice(cursor - 1, cursor + 1)))) return [3 /*break*/, 3];
                        _a = __read(this.props.defaultSearchItems, 2), defaultSearchItems = _a[0], defaultRecentItems = _a[1];
                        if (!!defaultSearchItems.length) return [3 /*break*/, 2];
                        // Update searchTerm, otherwise <SearchDropdown> will have wrong state
                        // (e.g. if you delete a query, the last letter will be highlighted if `searchTerm`
                        // does not get updated)
                        this.setState({ searchTerm: query });
                        tagKeys = this.getTagKeys('');
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        recentSearches_1 = _f.sent();
                        this.updateAutoCompleteState(tagKeys, recentSearches_1, '', 'tag-key');
                        return [2 /*return*/];
                    case 2:
                        // cursor on whitespace show default "help" search terms
                        this.setState({ searchTerm: '' });
                        this.updateAutoCompleteState(defaultSearchItems, defaultRecentItems, '', 'default');
                        return [2 /*return*/];
                    case 3:
                        last = (_d = terms.pop()) !== null && _d !== void 0 ? _d : '';
                        index = last.indexOf(':');
                        if (!(index === -1)) return [3 /*break*/, 5];
                        // No colon present; must still be deciding key
                        matchValue = last.replace(new RegExp("^" + NEGATION_OPERATOR), '');
                        autoCompleteItems = this.getTagKeys(matchValue);
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 4:
                        recentSearches_2 = _f.sent();
                        this.setState({ searchTerm: matchValue });
                        this.updateAutoCompleteState(autoCompleteItems, recentSearches_2, matchValue, 'tag-key');
                        return [2 /*return*/];
                    case 5:
                        _b = this.props, prepareQuery = _b.prepareQuery, excludeEnvironment = _b.excludeEnvironment;
                        supportedTags = (_e = this.props.supportedTags) !== null && _e !== void 0 ? _e : {};
                        // TODO(billy): Better parsing for these examples
                        //
                        // > sentry:release:
                        // > url:"http://with/colon"
                        tagName = last.slice(0, index);
                        // e.g. given "!gpu" we want "gpu"
                        tagName = tagName.replace(new RegExp("^" + NEGATION_OPERATOR), '');
                        query = last.slice(index + 1);
                        preparedQuery = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
                        filteredSearchGroups = !preparedQuery
                            ? this.state.searchGroups
                            : this.state.searchGroups.filter(function (item) { return item.value && item.value.indexOf(preparedQuery) !== -1; });
                        this.setState({
                            searchTerm: query,
                            searchGroups: filteredSearchGroups,
                        });
                        tag = supportedTags[tagName];
                        if (!tag) {
                            this.updateAutoCompleteState([], [], tagName, 'invalid-tag');
                            return [2 /*return*/];
                        }
                        // Ignore the environment tag if the feature is active and
                        // excludeEnvironment = true
                        if (excludeEnvironment && tagName === 'environment') {
                            return [2 /*return*/];
                        }
                        fetchTagValuesFn = tag.key === 'firstRelease'
                            ? this.getReleases
                            : tag.predefined
                                ? this.getPredefinedTagValues
                                : this.getTagValues;
                        return [4 /*yield*/, Promise.all([
                                fetchTagValuesFn(tag, preparedQuery),
                                this.getRecentSearches(),
                            ])];
                    case 6:
                        _c = __read.apply(void 0, [_f.sent(), 2]), tagValues = _c[0], recentSearches = _c[1];
                        this.updateAutoCompleteState(tagValues, recentSearches, tag.key, 'tag-value');
                        return [2 /*return*/];
                }
            });
        }); };
        _this.isDefaultDropdownItem = function (item) { return item && item.type === 'default'; };
        /**
         * Updates autocomplete dropdown items and autocomplete index state
         *
         * @param searchItems List of search item objects with keys: title, desc, value
         * @param recentSearchItems List of recent search items, same format as searchItem
         * @param tagName The current tag name in scope
         * @param type Defines the type/state of the dropdown menu items
         */
        _this.updateAutoCompleteState = function (searchItems, recentSearchItems, tagName, type) {
            var _a = _this.props, hasRecentSearches = _a.hasRecentSearches, maxSearchItems = _a.maxSearchItems;
            _this.setState(createSearchGroups(searchItems, hasRecentSearches ? recentSearchItems : undefined, tagName, type, maxSearchItems));
        };
        _this.onTogglePinnedSearch = function (evt) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, savedSearchType, hasPinnedSearch, pinnedSearch, router, _b, _cursor, _page, currentQuery, resp;
            var _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, savedSearchType = _a.savedSearchType, hasPinnedSearch = _a.hasPinnedSearch, pinnedSearch = _a.pinnedSearch;
                        router = this.context.router;
                        evt.preventDefault();
                        evt.stopPropagation();
                        if (savedSearchType === undefined || !hasPinnedSearch) {
                            return [2 /*return*/];
                        }
                        _b = router.location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
                        trackAnalyticsEvent({
                            eventKey: 'search.pin',
                            eventName: 'Search: Pin',
                            organization_id: organization.id,
                            action: !!pinnedSearch ? 'unpin' : 'pin',
                            search_type: savedSearchType === 0 ? 'issues' : 'events',
                            query: (_c = pinnedSearch === null || pinnedSearch === void 0 ? void 0 : pinnedSearch.query) !== null && _c !== void 0 ? _c : this.state.query,
                        });
                        if (!!pinnedSearch) {
                            unpinSearch(api, organization.slug, savedSearchType, pinnedSearch).then(function () {
                                browserHistory.push(__assign(__assign({}, router.location), { pathname: "/organizations/" + organization.slug + "/issues/", query: __assign(__assign({}, currentQuery), { query: pinnedSearch.query }) }));
                            });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, pinSearch(api, organization.slug, savedSearchType, removeSpace(this.state.query))];
                    case 1:
                        resp = _d.sent();
                        if (!resp || !resp.id) {
                            return [2 /*return*/];
                        }
                        browserHistory.push(__assign(__assign({}, router.location), { pathname: "/organizations/" + organization.slug + "/issues/searches/" + resp.id + "/", query: currentQuery }));
                        return [2 /*return*/];
                }
            });
        }); };
        _this.onAutoComplete = function (replaceText, item) {
            var _a;
            if (item.type === 'recent-search') {
                trackAnalyticsEvent({
                    eventKey: 'search.searched',
                    eventName: 'Search: Performed search',
                    organization_id: _this.props.organization.id,
                    query: replaceText,
                    source: _this.props.savedSearchType === 0 ? 'issues' : 'events',
                    search_source: 'recent_search',
                });
                _this.setState({ query: replaceText }, function () {
                    // Propagate onSearch and save to recent searches
                    _this.doSearch();
                });
                return;
            }
            var cursor = _this.getCursorPosition();
            var query = _this.state.query;
            var lastTermIndex = SmartSearchBar.getLastTermIndex(query, cursor);
            var terms = SmartSearchBar.getQueryTerms(query, lastTermIndex);
            var newQuery;
            // If not postfixed with : (tag value), add trailing space
            replaceText += item.type !== 'tag-value' || cursor < query.length ? '' : ' ';
            var isNewTerm = query.charAt(query.length - 1) === ' ' && item.type !== 'tag-value';
            if (!terms) {
                newQuery = replaceText;
            }
            else if (isNewTerm) {
                newQuery = "" + query + replaceText;
            }
            else {
                var last = (_a = terms.pop()) !== null && _a !== void 0 ? _a : '';
                newQuery = query.slice(0, lastTermIndex); // get text preceding last term
                var prefix = last.startsWith(NEGATION_OPERATOR) ? NEGATION_OPERATOR : '';
                // newQuery is all the terms up to the current term: "... <term>:"
                // replaceText should be the selected value
                if (last.indexOf(':') > -1) {
                    var replacement = ":" + replaceText;
                    // The user tag often contains : within its value and we need to quote it.
                    if (last.startsWith('user:')) {
                        var colonIndex = replaceText.indexOf(':');
                        if (colonIndex > -1) {
                            replacement = ":\"" + replaceText.trim() + "\"";
                        }
                    }
                    // tag key present: replace everything after colon with replaceText
                    newQuery = newQuery.replace(/\:"[^"]*"?$|\:\S*$/, replacement);
                }
                else {
                    // no tag key present: replace last token with replaceText
                    newQuery = newQuery.replace(/\S+$/, "" + prefix + replaceText);
                }
                newQuery = newQuery.concat(query.slice(lastTermIndex));
            }
            _this.setState({ query: newQuery }, function () {
                var _a, _b;
                // setting a new input value will lose focus; restore it
                if (_this.searchInput.current) {
                    _this.searchInput.current.focus();
                }
                // then update the autocomplete box with new contextTypes
                _this.updateAutoCompleteItems();
                (_b = (_a = _this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, newQuery, new MouseEvent('click'));
            });
        };
        return _this;
    }
    SmartSearchBar.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // query was updated by another source (e.g. sidebar filters)
        if (nextProps.query !== this.props.query) {
            this.setState({
                query: addSpace(nextProps.query),
            });
        }
    };
    SmartSearchBar.prototype.componentWillUnmount = function () {
        if (this.blurTimeout) {
            clearTimeout(this.blurTimeout);
            this.blurTimeout = undefined;
        }
    };
    SmartSearchBar.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, dropdownClassName = _a.dropdownClassName, organization = _a.organization, hasPinnedSearch = _a.hasPinnedSearch, hasSearchBuilder = _a.hasSearchBuilder, canCreateSavedSearch = _a.canCreateSavedSearch, pinnedSearch = _a.pinnedSearch, placeholder = _a.placeholder, disabled = _a.disabled, useFormWrapper = _a.useFormWrapper, onSidebarToggle = _a.onSidebarToggle, inlineLabel = _a.inlineLabel;
        var pinTooltip = !!pinnedSearch ? t('Unpin this search') : t('Pin this search');
        var pinIcon = !!pinnedSearch ? (<IconPin isSolid size="xs"/>) : (<IconPin size="xs"/>);
        var hasQuery = !!this.state.query;
        var input = (<React.Fragment>
        <StyledInput type="text" placeholder={placeholder} id="smart-search-input" name="query" ref={this.searchInput} autoComplete="off" value={this.state.query} onFocus={this.onQueryFocus} onBlur={this.onQueryBlur} onKeyUp={this.onKeyUp} onKeyDown={this.onKeyDown} onChange={this.onQueryChange} onClick={this.onInputClick} disabled={disabled}/>
        {(this.state.loading || this.state.searchGroups.length > 0) && (<DropdownWrapper visible={this.state.dropdownVisible}>
            <SearchDropdown className={dropdownClassName} items={this.state.searchGroups} onClick={this.onAutoComplete} loading={this.state.loading} searchSubstring={this.state.searchTerm}/>
          </DropdownWrapper>)}
      </React.Fragment>);
        return (<Container className={className} isOpen={this.state.dropdownVisible}>
        <SearchLabel htmlFor="smart-search-input" aria-label={t('Search events')}>
          <IconSearch />
          {inlineLabel}
        </SearchLabel>

        {useFormWrapper ? (<StyledForm onSubmit={this.onSubmit}>{input}</StyledForm>) : (input)}
        <StyledButtonBar>
          {this.state.query !== '' && (<InputButton type="button" title={t('Clear search')} borderless aria-label="Clear search" size="zero" tooltipProps={{
            containerDisplayMode: 'inline-flex',
        }} onClick={this.clearSearch}>
              <IconClose size="xs"/>
            </InputButton>)}
          {hasPinnedSearch && (<InputButton type="button" title={pinTooltip} borderless disabled={!hasQuery} aria-label={pinTooltip} size="zero" tooltipProps={{
            containerDisplayMode: 'inline-flex',
        }} onClick={this.onTogglePinnedSearch} collapseIntoEllipsisMenu={1} isActive={!!pinnedSearch} icon={pinIcon}/>)}
          {canCreateSavedSearch && (<ClassNames>
              {function (_a) {
            var css = _a.css;
            return (<CreateSavedSearchButton query={_this.state.query} organization={organization} withTooltip iconOnly buttonClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                    ", "\n                  "], ["\n                    ",
                "\n                  "])), getInputButtonStyles({
                collapseIntoEllipsisMenu: 2,
            }))}/>);
        }}
            </ClassNames>)}
          {hasSearchBuilder && (<SearchBuilderButton title={t('Toggle search builder')} borderless size="zero" tooltipProps={{
            containerDisplayMode: 'inline-flex',
        }} collapseIntoEllipsisMenu={2} aria-label={t('Toggle search builder')} onClick={onSidebarToggle} icon={<IconSliders size="xs"/>}/>)}

          {(hasPinnedSearch || canCreateSavedSearch || hasSearchBuilder) && (<StyledDropdownLink anchorRight caret={false} title={<EllipsisButton size="zero" borderless tooltipProps={{
            containerDisplayMode: 'flex',
        }} type="button" aria-label={t('Show more')} icon={<VerticalEllipsisIcon size="xs"/>}/>}>
              {hasPinnedSearch && (<DropdownElement showBelowMediaQuery={1} data-test-id="pin-icon" onClick={this.onTogglePinnedSearch}>
                  {pinIcon}
                  {!!pinnedSearch ? t('Unpin Search') : t('Pin Search')}
                </DropdownElement>)}
              {canCreateSavedSearch && (<ClassNames>
                  {function (_a) {
            var css = _a.css;
            return (<CreateSavedSearchButton query={_this.state.query} organization={organization} buttonClassName={css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n                        ", "\n                      "], ["\n                        ",
                "\n                      "])), getDropdownElementStyles({
                showBelowMediaQuery: 2,
                last: false,
            }))}/>);
        }}
                </ClassNames>)}
              {hasSearchBuilder && (<DropdownElement showBelowMediaQuery={2} last onClick={onSidebarToggle}>
                  <IconSliders size="xs"/>
                  {t('Toggle sidebar')}
                </DropdownElement>)}
            </StyledDropdownLink>)}
        </StyledButtonBar>
      </Container>);
    };
    /**
     * Given a query, and the current cursor position, return the string-delimiting
     * index of the search term designated by the cursor.
     */
    SmartSearchBar.getLastTermIndex = function (query, cursor) {
        // TODO: work with quoted-terms
        var cursorOffset = query.slice(cursor).search(/\s|$/);
        return cursor + (cursorOffset === -1 ? 0 : cursorOffset);
    };
    /**
     * Returns an array of query terms, including incomplete terms
     *
     * e.g. ["is:unassigned", "browser:\"Chrome 33.0\"", "assigned"]
     */
    SmartSearchBar.getQueryTerms = function (query, cursor) {
        return query.slice(0, cursor).match(/\S+:"[^"]*"?|\S+/g);
    };
    SmartSearchBar.contextTypes = {
        router: PropTypes.object,
    };
    SmartSearchBar.defaultProps = {
        defaultQuery: '',
        query: null,
        onSearch: function () { },
        excludeEnvironment: false,
        placeholder: t('Search for events, users, tags, and everything else.'),
        supportedTags: {},
        defaultSearchItems: [[], []],
        hasPinnedSearch: false,
        useFormWrapper: true,
        savedSearchType: SavedSearchType.ISSUE,
    };
    return SmartSearchBar;
}(React.Component));
var SmartSearchBarContainer = createReactClass({
    displayName: 'SmartSearchBarContainer',
    mixins: [Reflux.listenTo(MemberListStore, 'onMemberListStoreChange')],
    getInitialState: function () {
        return {
            members: MemberListStore.getAll(),
        };
    },
    onMemberListStoreChange: function (members) {
        this.setState({ members: members }, this.updateAutoCompleteItems);
    },
    render: function () {
        // SmartSearchBar doesn't use members, but we forward it to cause a re-render.
        return <SmartSearchBar {...this.props} members={this.state.members}/>;
    },
});
export default withApi(withOrganization(SmartSearchBarContainer));
export { SmartSearchBar };
var Container = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: ", ";\n  /* match button height */\n  height: 40px;\n  box-shadow: inset ", ";\n  background: ", ";\n\n  position: relative;\n\n  display: flex;\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"], ["\n  border: 1px solid ", ";\n  border-radius: ",
    ";\n  /* match button height */\n  height: 40px;\n  box-shadow: inset ", ";\n  background: ", ";\n\n  position: relative;\n\n  display: flex;\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"
        : p.theme.borderRadius;
}, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.background; }, function (p) { return p.theme.backgroundSecondary; });
var DropdownWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: ", ";\n"], ["\n  display: ", ";\n"])), function (p) { return (p.visible ? 'block' : 'none'); });
var StyledForm = styled('form')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledInput = styled('input')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  background: transparent;\n  border: 0;\n  outline: none;\n\n  font-size: ", ";\n  width: 100%;\n  height: 40px;\n  line-height: 40px;\n  padding: 0 0 0 ", ";\n\n  &::placeholder {\n    color: ", ";\n  }\n  &:focus {\n    border-color: ", ";\n    border-bottom-right-radius: 0;\n  }\n\n  .show-sidebar & {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background: transparent;\n  border: 0;\n  outline: none;\n\n  font-size: ", ";\n  width: 100%;\n  height: 40px;\n  line-height: 40px;\n  padding: 0 0 0 ", ";\n\n  &::placeholder {\n    color: ", ";\n  }\n  &:focus {\n    border-color: ", ";\n    border-bottom-right-radius: 0;\n  }\n\n  .show-sidebar & {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; }, space(1), function (p) { return p.theme.formPlaceholder; }, function (p) { return p.theme.border; }, function (p) { return p.theme.disabled; });
var InputButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getInputButtonStyles);
var SearchBuilderButton = styled(InputButton)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space(0.25), space(0.5));
var StyledDropdownLink = styled(DropdownLink)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: none;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"], ["\n  display: none;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var DropdownElement = styled('a')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getDropdownElementStyles);
var StyledButtonBar = styled(ButtonBar)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var EllipsisButton = styled(InputButton)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  /*\n   * this is necessary because DropdownLink wraps the button in an unstyled\n   * span\n   */\n  margin: 6px 0 0 0;\n"], ["\n  /*\n   * this is necessary because DropdownLink wraps the button in an unstyled\n   * span\n   */\n  margin: 6px 0 0 0;\n"])));
var VerticalEllipsisIcon = styled(IconEllipsis)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  transform: rotate(90deg);\n"], ["\n  transform: rotate(90deg);\n"])));
var SearchLabel = styled('label')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  padding-left: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  padding-left: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=index.jsx.map