import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import Cookies from 'js-cookie';
import React from 'react';
import isEqual from 'lodash/isEqual';
import pickBy from 'lodash/pickBy';
import * as qs from 'query-string';
import { withProfiler } from '@sentry/react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { DEFAULT_QUERY, DEFAULT_STATS_PERIOD } from 'app/constants';
import { tct } from 'app/locale';
import { Panel, PanelBody } from 'app/components/panels';
import { analytics, metric } from 'app/utils/analytics';
import { defined } from 'app/utils';
import { deleteSavedSearch, fetchSavedSearches, resetSavedSearches, } from 'app/actionCreators/savedSearches';
import { extractSelectionParameters } from 'app/components/organizations/globalSelectionHeader/utils';
import { fetchOrgMembers, indexMembersByProject } from 'app/actionCreators/members';
import { loadOrganizationTags, fetchTagValues } from 'app/actionCreators/tags';
import { getUtcDateString } from 'app/utils/dates';
import CursorPoller from 'app/utils/cursorPoller';
import GroupStore from 'app/stores/groupStore';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import ProcessingIssueList from 'app/components/stream/processingIssueList';
import QueryCount from 'app/components/queryCount';
import StreamGroup from 'app/components/stream/group';
import StreamManager from 'app/utils/streamManager';
import parseApiError from 'app/utils/parseApiError';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withSavedSearches from 'app/utils/withSavedSearches';
import withIssueTags from 'app/utils/withIssueTags';
import { callIfFunction } from 'app/utils/callIfFunction';
import space from 'app/styles/space';
import { PageContent } from 'app/styles/organization';
import Feature from 'app/components/acl/feature';
import IssueListActions from './actions';
import IssueListFilters from './filters';
import IssueListHeader from './header';
import IssueListSidebar from './sidebar';
import NoGroupsHandler from './noGroupsHandler';
var MAX_ITEMS = 25;
var DEFAULT_SORT = 'date';
// the default period for the graph in each issue row
var DEFAULT_GRAPH_STATS_PERIOD = '24h';
// the allowed period choices for graph in each issue row
var DYNAMIC_COUNTS_STATS_PERIODS = new Set(['14d', '24h', 'auto']);
var IssueListOverview = /** @class */ (function (_super) {
    __extends(IssueListOverview, _super);
    function IssueListOverview(props) {
        var _this = _super.call(this, props) || this;
        _this._streamManager = new StreamManager(GroupStore);
        _this.getEndpointParams = function () {
            var selection = _this.props.selection;
            var params = __assign({ project: selection.projects, environment: selection.environments, query: _this.getQuery() }, selection.datetime);
            if (selection.datetime.period) {
                delete params.period;
                params.statsPeriod = selection.datetime.period;
            }
            if (params.end) {
                params.end = getUtcDateString(params.end);
            }
            if (params.start) {
                params.start = getUtcDateString(params.start);
            }
            var sort = _this.getSort();
            if (sort !== DEFAULT_SORT) {
                params.sort = sort;
            }
            var groupStatsPeriod = _this.getGroupStatsPeriod();
            if (groupStatsPeriod !== DEFAULT_GRAPH_STATS_PERIOD) {
                params.groupStatsPeriod = groupStatsPeriod;
            }
            // only include defined values.
            return pickBy(params, function (v) { return defined(v); });
        };
        _this.getGlobalSearchProjectIds = function () {
            return _this.props.selection.projects;
        };
        _this.fetchData = function () {
            GroupStore.loadInitialData([]);
            _this.setState({
                issuesLoading: true,
                queryCount: 0,
                error: null,
            });
            var requestParams = __assign(__assign({}, _this.getEndpointParams()), { limit: MAX_ITEMS, shortIdLookup: 1 });
            var currentQuery = _this.props.location.query || {};
            if ('cursor' in currentQuery) {
                requestParams.cursor = currentQuery.cursor;
            }
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = DEFAULT_STATS_PERIOD;
            }
            var orgFeatures = new Set(_this.props.organization.features);
            if (orgFeatures.has('inbox')) {
                requestParams.expand = 'inbox';
            }
            if (_this._lastRequest) {
                _this._lastRequest.cancel();
            }
            _this._poller.disable();
            _this._lastRequest = _this.props.api.request(_this.getGroupListEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: function (data, _, jqXHR) {
                    if (!jqXHR) {
                        return;
                    }
                    var orgId = _this.props.params.orgId;
                    // If this is a direct hit, we redirect to the intended result directly.
                    if (jqXHR.getResponseHeader('X-Sentry-Direct-Hit') === '1') {
                        var redirect = void 0;
                        if (data[0] && data[0].matchingEventId) {
                            var _a = data[0], id = _a.id, matchingEventId = _a.matchingEventId;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/events/" + matchingEventId + "/";
                        }
                        else {
                            var id = data[0].id;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/";
                        }
                        browserHistory.replace({
                            pathname: redirect,
                            query: extractSelectionParameters(_this.props.location.query),
                        });
                        return;
                    }
                    _this._streamManager.push(data);
                    var queryCount = jqXHR.getResponseHeader('X-Hits');
                    var queryMaxCount = jqXHR.getResponseHeader('X-Max-Hits');
                    var pageLinks = jqXHR.getResponseHeader('Link');
                    _this.setState({
                        error: null,
                        issuesLoading: false,
                        queryCount: typeof queryCount !== 'undefined' && queryCount
                            ? parseInt(queryCount, 10) || 0
                            : 0,
                        queryMaxCount: typeof queryMaxCount !== 'undefined' && queryMaxCount
                            ? parseInt(queryMaxCount, 10) || 0
                            : 0,
                        pageLinks: pageLinks !== null ? pageLinks : '',
                    });
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError(err),
                        issuesLoading: false,
                    });
                },
                complete: function () {
                    _this._lastRequest = null;
                    _this.resumePolling();
                },
            });
        };
        _this.resumePolling = function () {
            if (!_this.state.pageLinks) {
                return;
            }
            // Only resume polling if we're on the first page of results
            var links = parseLinkHeader(_this.state.pageLinks);
            if (links && !links.previous.results && _this.state.realtimeActive) {
                _this._poller.setEndpoint(links.previous.href);
                _this._poller.enable();
            }
        };
        _this.onRealtimeChange = function (realtime) {
            Cookies.set('realtimeActive', realtime.toString());
            _this.setState({
                realtimeActive: realtime,
            });
        };
        _this.onSelectStatsPeriod = function (period) {
            if (period !== _this.getGroupStatsPeriod()) {
                _this.transitionTo({ groupStatsPeriod: period });
            }
        };
        _this.onRealtimePoll = function (data, _links) {
            // Note: We do not update state with cursors from polling,
            // `CursorPoller` updates itself with new cursors
            _this._streamManager.unshift(data);
        };
        _this.listener = GroupStore.listen(function () { return _this.onGroupChange(); }, undefined);
        _this.onIssueListSidebarSearch = function (query) {
            analytics('search.searched', {
                org_id: _this.props.organization.id,
                query: query,
                search_type: 'issues',
                search_source: 'search_builder',
            });
            _this.onSearch(query);
        };
        _this.onSearch = function (query) {
            if (query === _this.state.query) {
                // if query is the same, just re-fetch data
                _this.fetchData();
            }
            else {
                // Clear the saved search as the user wants something else.
                _this.transitionTo({ query: query }, null);
            }
        };
        _this.onSortChange = function (sort) {
            _this.transitionTo({ sort: sort });
        };
        _this.onCursorChange = function (cursor, _path, query, pageDiff) {
            var queryPageInt = parseInt(query.page, 10);
            var nextPage = isNaN(queryPageInt)
                ? pageDiff
                : queryPageInt + pageDiff;
            // unset cursor and page when we navigate back to the first page
            // also reset cursor if somehow the previous button is enabled on
            // first page and user attempts to go backwards
            if (nextPage <= 0) {
                cursor = undefined;
                nextPage = undefined;
            }
            _this.transitionTo({ cursor: cursor, page: nextPage });
        };
        _this.onSidebarToggle = function () {
            var organization = _this.props.organization;
            _this.setState({
                isSidebarVisible: !_this.state.isSidebarVisible,
                renderSidebar: true,
            });
            analytics('issue.search_sidebar_clicked', {
                org_id: parseInt(organization.id, 10),
            });
        };
        _this.transitionTo = function (newParams, savedSearch) {
            if (newParams === void 0) { newParams = {}; }
            if (savedSearch === void 0) { savedSearch = _this.props.savedSearch; }
            var query = __assign(__assign({}, _this.getEndpointParams()), newParams);
            var organization = _this.props.organization;
            var path;
            if (savedSearch && savedSearch.id) {
                path = "/organizations/" + organization.slug + "/issues/searches/" + savedSearch.id + "/";
                // Remove the query as saved searches bring their own query string.
                delete query.query;
                // If we aren't going to another page in the same search
                // drop the query and replace the current project, with the saved search search project
                // if available.
                if (!query.cursor && savedSearch.projectId) {
                    query.project = [savedSearch.projectId];
                }
            }
            else {
                path = "/organizations/" + organization.slug + "/issues/";
            }
            if (path !== _this.props.location.pathname ||
                !isEqual(query, _this.props.location.query)) {
                browserHistory.push({
                    pathname: path,
                    query: query,
                });
                _this.setState({ issuesLoading: true });
            }
        };
        _this.renderGroupNodes = function (ids, groupStatsPeriod) {
            var topIssue = ids[0];
            var memberList = _this.state.memberList;
            var hasInboxReason = ids.some(function (id) { var _a; return !!((_a = GroupStore.get(id)) === null || _a === void 0 ? void 0 : _a.inbox); });
            var groupNodes = ids.map(function (id) {
                var hasGuideAnchor = id === topIssue;
                var group = GroupStore.get(id);
                var members;
                if (group && group.project) {
                    members = memberList[group.project.slug];
                }
                return (<StreamGroup key={id} id={id} statsPeriod={groupStatsPeriod} query={_this.getQuery()} hasGuideAnchor={hasGuideAnchor} memberList={members} hasInboxReason={hasInboxReason} useFilteredStats/>);
            });
            return <PanelBody>{groupNodes}</PanelBody>;
        };
        _this.fetchSavedSearches = function () {
            var organization = _this.props.organization;
            fetchSavedSearches(_this.props.api, organization.slug);
        };
        _this.onSavedSearchSelect = function (savedSearch) {
            _this.setState({ issuesLoading: true }, function () { return _this.transitionTo(undefined, savedSearch); });
        };
        _this.onSavedSearchDelete = function (search) {
            var orgId = _this.props.params.orgId;
            deleteSavedSearch(_this.props.api, orgId, search).then(function () {
                _this.setState({
                    issuesLoading: true,
                }, function () { return _this.transitionTo({}, null); });
            });
        };
        _this.handleTabClick = function (query) {
            _this.transitionTo({ query: query }, null);
        };
        _this.tagValueLoader = function (key, search) {
            var orgId = _this.props.params.orgId;
            var projectIds = _this.getGlobalSearchProjectIds().map(function (id) { return id.toString(); });
            var endpointParams = _this.getEndpointParams();
            return fetchTagValues(_this.props.api, orgId, key, search, projectIds, endpointParams);
        };
        var realtimeActiveCookie = Cookies.get('realtimeActive');
        var realtimeActive = typeof realtimeActiveCookie === 'undefined'
            ? false
            : realtimeActiveCookie === 'true';
        _this.state = {
            groupIds: [],
            selectAllActive: false,
            realtimeActive: realtimeActive,
            pageLinks: '',
            queryCount: 0,
            queryMaxCount: 0,
            error: null,
            isSidebarVisible: false,
            renderSidebar: false,
            issuesLoading: true,
            tagsLoading: true,
            memberList: {},
        };
        return _this;
    }
    IssueListOverview.prototype.componentDidMount = function () {
        var _a;
        var links = parseLinkHeader(this.state.pageLinks);
        this._poller = new CursorPoller({
            endpoint: ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.href) || '',
            success: this.onRealtimePoll,
        });
        // Start by getting searches first so if the user is on a saved search
        // or they have a pinned search we load the correct data the first time.
        this.fetchSavedSearches();
        this.fetchTags();
        this.fetchMemberList();
    };
    IssueListOverview.prototype.componentDidUpdate = function (prevProps, prevState) {
        // Fire off profiling/metrics first
        if (prevState.issuesLoading && !this.state.issuesLoading) {
            // First Meaningful Paint for /organizations/:orgId/issues/
            if (prevState.queryCount === null) {
                metric.measure({
                    name: 'app.page.perf.issue-list',
                    start: 'page-issue-list-start',
                    data: {
                        // start_type is set on 'page-issue-list-start'
                        org_id: parseInt(this.props.organization.id, 10),
                        group: this.props.organization.features.includes('enterprise-perf')
                            ? 'enterprise-perf'
                            : 'control',
                        milestone: 'first-meaningful-paint',
                        is_enterprise: this.props.organization.features
                            .includes('enterprise-orgs')
                            .toString(),
                        is_outlier: this.props.organization.features
                            .includes('enterprise-orgs-outliers')
                            .toString(),
                    },
                });
                metric.endTransaction({ name: '/organizations/:orgId/issues/' });
            }
        }
        if (prevState.realtimeActive !== this.state.realtimeActive) {
            // User toggled realtime button
            if (this.state.realtimeActive) {
                this.resumePolling();
            }
            else {
                this._poller.disable();
            }
        }
        // If the project selection has changed reload the member list and tag keys
        // allowing autocomplete and tag sidebar to be more accurate.
        if (!isEqual(prevProps.selection.projects, this.props.selection.projects)) {
            this.fetchMemberList();
            this.fetchTags();
        }
        // Wait for saved searches to load before we attempt to fetch stream data
        if (this.props.savedSearchLoading) {
            return;
        }
        else if (prevProps.savedSearchLoading) {
            this.fetchData();
            return;
        }
        var prevQuery = prevProps.location.query;
        var newQuery = this.props.location.query;
        // If any important url parameter changed or saved search changed
        // reload data.
        if (!isEqual(prevProps.selection, this.props.selection) ||
            prevQuery.cursor !== newQuery.cursor ||
            prevQuery.sort !== newQuery.sort ||
            prevQuery.query !== newQuery.query ||
            prevQuery.statsPeriod !== newQuery.statsPeriod ||
            prevQuery.groupStatsPeriod !== newQuery.groupStatsPeriod ||
            prevProps.savedSearch !== this.props.savedSearch) {
            this.fetchData();
        }
        else if (!this._lastRequest &&
            prevState.issuesLoading === false &&
            this.state.issuesLoading) {
            // Reload if we issues are loading or their loading state changed.
            // This can happen when transitionTo is called
            this.fetchData();
        }
    };
    IssueListOverview.prototype.componentWillUnmount = function () {
        this._poller.disable();
        GroupStore.reset();
        this.props.api.clear();
        callIfFunction(this.listener);
        // Reset store when unmounting because we always fetch on mount
        // This means if you navigate away from stream and then back to stream,
        // this component will go from:
        // "ready" ->
        // "loading" (because fetching saved searches) ->
        // "ready"
        //
        // We don't render anything until saved searches is ready, so this can
        // cause weird side effects (e.g. ProcessingIssueList mounting and making
        // a request, but immediately unmounting when fetching saved searches)
        resetSavedSearches();
    };
    IssueListOverview.prototype.getQuery = function () {
        if (this.props.savedSearch) {
            return this.props.savedSearch.query;
        }
        var query = this.props.location.query.query;
        if (query !== undefined) {
            return query;
        }
        // TODO(workflow): set inbox as new default query
        if (this.props.organization.features.includes('inbox')) {
            return 'is:inbox';
        }
        return DEFAULT_QUERY;
    };
    IssueListOverview.prototype.getSort = function () {
        return this.props.location.query.sort || DEFAULT_SORT;
    };
    IssueListOverview.prototype.getGroupStatsPeriod = function () {
        var _a, _b;
        var currentPeriod = typeof ((_a = this.props.location.query) === null || _a === void 0 ? void 0 : _a.groupStatsPeriod) === 'string'
            ? (_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.groupStatsPeriod : DEFAULT_GRAPH_STATS_PERIOD;
        return DYNAMIC_COUNTS_STATS_PERIODS.has(currentPeriod)
            ? currentPeriod
            : DEFAULT_GRAPH_STATS_PERIOD;
    };
    IssueListOverview.prototype.fetchMemberList = function () {
        var _this = this;
        var projectIds = this.getGlobalSearchProjectIds();
        fetchOrgMembers(this.props.api, this.props.organization.slug, projectIds).then(function (members) {
            _this.setState({ memberList: indexMembersByProject(members) });
        });
    };
    IssueListOverview.prototype.fetchTags = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection;
        this.setState({ tagsLoading: true });
        loadOrganizationTags(this.props.api, organization.slug, selection).then(function () {
            return _this.setState({ tagsLoading: false });
        });
    };
    IssueListOverview.prototype.getGroupListEndpoint = function () {
        var params = this.props.params;
        return "/organizations/" + params.orgId + "/issues/";
    };
    IssueListOverview.prototype.onGroupChange = function () {
        var groupIds = this._streamManager.getAllItems().map(function (item) { return item.id; });
        if (!isEqual(groupIds, this.state.groupIds)) {
            this.setState({ groupIds: groupIds });
        }
    };
    /**
     * Returns true if all results in the current query are visible/on this page
     */
    IssueListOverview.prototype.allResultsVisible = function () {
        if (!this.state.pageLinks) {
            return false;
        }
        var links = parseLinkHeader(this.state.pageLinks);
        return links && !links.previous.results && !links.next.results;
    };
    IssueListOverview.prototype.renderLoading = function () {
        return <LoadingIndicator />;
    };
    IssueListOverview.prototype.renderStreamBody = function () {
        var body;
        if (this.state.issuesLoading) {
            body = this.renderLoading();
        }
        else if (this.state.error) {
            body = <LoadingError message={this.state.error} onRetry={this.fetchData}/>;
        }
        else if (this.state.groupIds.length > 0) {
            body = this.renderGroupNodes(this.state.groupIds, this.getGroupStatsPeriod());
        }
        else {
            body = (<NoGroupsHandler api={this.props.api} organization={this.props.organization} query={this.getQuery()} selectedProjectIds={this.props.selection.projects} groupIds={this.state.groupIds}/>);
        }
        return body;
    };
    IssueListOverview.prototype.render = function () {
        var _this = this;
        var _a, _b, _c, _d;
        if (this.props.savedSearchLoading) {
            return this.renderLoading();
        }
        var _e = this.state, renderSidebar = _e.renderSidebar, isSidebarVisible = _e.isSidebarVisible, tagsLoading = _e.tagsLoading, pageLinks = _e.pageLinks, queryCount = _e.queryCount, realtimeActive = _e.realtimeActive, groupIds = _e.groupIds, queryMaxCount = _e.queryMaxCount, issuesLoading = _e.issuesLoading;
        var _f = this.props, organization = _f.organization, savedSearch = _f.savedSearch, savedSearches = _f.savedSearches, tags = _f.tags, selection = _f.selection, location = _f.location;
        var query = this.getQuery();
        var queryPageInt = parseInt(location.query.page, 10);
        var page = isNaN(queryPageInt) ? 0 : queryPageInt;
        var pageCount = page * MAX_ITEMS + (groupIds === null || groupIds === void 0 ? void 0 : groupIds.length);
        // TODO(workflow): When organization:inbox flag is removed add 'inbox' to tagStore
        if (organization.features.includes('inbox') && !((_b = (_a = tags === null || tags === void 0 ? void 0 : tags.is) === null || _a === void 0 ? void 0 : _a.values) === null || _b === void 0 ? void 0 : _b.includes('inbox'))) {
            (_d = (_c = tags === null || tags === void 0 ? void 0 : tags.is) === null || _c === void 0 ? void 0 : _c.values) === null || _d === void 0 ? void 0 : _d.push('inbox');
        }
        return (<Feature organization={organization} features={['organizations:inbox']}>
        {function (_a) {
            var _b;
            var hasFeature = _a.hasFeature;
            return (<React.Fragment>
            {hasFeature && (<IssueListHeader query={query} queryCount={queryCount} queryMaxCount={queryMaxCount} onTabChange={_this.handleTabClick}/>)}
            <StyledPageContent isInbox={hasFeature}>
              <StreamContent showSidebar={isSidebarVisible}>
                <IssueListFilters organization={organization} query={query} savedSearch={savedSearch} sort={_this.getSort()} queryCount={queryCount} queryMaxCount={queryMaxCount} onSortChange={_this.onSortChange} onSearch={_this.onSearch} onSavedSearchSelect={_this.onSavedSearchSelect} onSavedSearchDelete={_this.onSavedSearchDelete} onSidebarToggle={_this.onSidebarToggle} isSearchDisabled={isSidebarVisible} savedSearchList={savedSearches} tagValueLoader={_this.tagValueLoader} tags={tags}/>

                <Panel>
                  <IssueListActions orgId={organization.slug} organization={organization} selection={selection} query={query} queryCount={queryCount} onSelectStatsPeriod={_this.onSelectStatsPeriod} onRealtimeChange={_this.onRealtimeChange} realtimeActive={realtimeActive} statsPeriod={_this.getGroupStatsPeriod()} groupIds={groupIds} issuesLoading={issuesLoading} allResultsVisible={_this.allResultsVisible()}/>
                  <PanelBody>
                    <ProcessingIssueList organization={organization} projectIds={(_b = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _b === void 0 ? void 0 : _b.map(function (p) { return p.toString(); })} showProject/>
                    {_this.renderStreamBody()}
                  </PanelBody>
                </Panel>
                <PaginationWrapper>
                  {hasFeature && (groupIds === null || groupIds === void 0 ? void 0 : groupIds.length) > 0 && (<div>
                      
                      {tct('Showing [count] of[total] issues', {
                count: <React.Fragment>{pageCount}</React.Fragment>,
                total: (<QueryCount hideParens count={queryCount} max={queryMaxCount}/>),
            })}
                    </div>)}
                  <StyledPagination pageLinks={pageLinks} onCursor={_this.onCursorChange}/>
                </PaginationWrapper>
              </StreamContent>

              <SidebarContainer showSidebar={isSidebarVisible}>
                
                {renderSidebar && (<IssueListSidebar loading={tagsLoading} tags={tags} query={query} onQueryChange={_this.onIssueListSidebarSearch} orgId={organization.slug} tagValueLoader={_this.tagValueLoader}/>)}
              </SidebarContainer>
            </StyledPageContent>
          </React.Fragment>);
        }}
      </Feature>);
    };
    return IssueListOverview;
}(React.Component));
export default withApi(withGlobalSelection(withSavedSearches(withOrganization(withIssueTags(withProfiler(IssueListOverview))))));
export { IssueListOverview };
// TODO(workflow): Replace PageContent with thirds body
var StyledPageContent = styled(PageContent)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  ", "\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  ",
    "\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"])), function (p) {
    return p.isInbox && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      background-color: ", ";\n    "], ["\n      background-color: ", ";\n    "])), p.theme.background);
}, function (p) { return p.theme.breakpoints[0]; }, space(2), space(2), space(2));
var StreamContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"], ["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"])), function (p) { return (p.showSidebar ? '75%' : '100%'); }, function (p) { return p.theme.breakpoints[0]; });
var SidebarContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return (p.showSidebar ? 'block' : 'none'); }, function (p) { return (p.showSidebar ? 'visible' : 'hidden'); }, function (p) { return (p.showSidebar ? 'auto' : 0); }, function (p) { return (p.showSidebar ? '25%' : 0); }, function (p) { return p.theme.breakpoints[0]; });
var PaginationWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledPagination = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-top: 0;\n  margin-left: ", ";\n"], ["\n  margin-top: 0;\n  margin-left: ", ";\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=overview.jsx.map