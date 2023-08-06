import { __assign, __extends, __read } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import moment from 'moment';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { getUtcDateString } from 'app/utils/dates';
import { t, tct } from 'app/locale';
import { updateProjects, updateDateTime } from 'app/actionCreators/globalSelection';
import ConfigStore from 'app/stores/configStore';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import PageHeading from 'app/components/pageHeading';
import localStorage from 'app/utils/localStorage';
import { DiscoverContainer, DiscoverGlobalSelectionHeader, Body, BodyContent, HeadingContainer, Sidebar, SidebarTabs, SavedQueryWrapper, } from './styles';
import { getQueryStringFromQuery, getQueryFromQueryString, deleteSavedQuery, updateSavedQuery, queryHasChanged, } from './utils';
import { isValidAggregation } from './aggregations/utils';
import { isValidCondition } from './conditions/utils';
import { trackQuery } from './analytics';
import EditSavedQuery from './sidebar/editSavedQuery';
import Intro from './intro';
import NewQuery from './sidebar/newQuery';
import QueryPanel from './sidebar/queryPanel';
import Result from './result';
import ResultLoading from './result/loading';
import SavedQueryList from './sidebar/savedQueryList';
import createResultManager from './resultManager';
var Discover = /** @class */ (function (_super) {
    __extends(Discover, _super);
    function Discover(props) {
        var _this = _super.call(this, props) || this;
        _this.updateProjects = function (val) {
            _this.updateField('projects', val);
            updateProjects(val);
        };
        _this.getDateTimeFields = function (_a) {
            var period = _a.period, start = _a.start, end = _a.end, utc = _a.utc;
            return ({
                range: period || null,
                utc: typeof utc !== 'undefined' ? utc : null,
                start: (start && getUtcDateString(start)) || null,
                end: (end && getUtcDateString(end)) || null,
            });
        };
        _this.changeTime = function (datetime) {
            _this.updateFields(_this.getDateTimeFields(datetime));
        };
        _this.updateDateTime = function (datetime) {
            var _a = _this.getDateTimeFields(datetime), start = _a.start, end = _a.end, range = _a.range, utc = _a.utc;
            updateDateTime({
                start: start,
                end: end,
                period: range,
                utc: utc,
            });
            _this.updateFields({ start: start, end: end, range: range, utc: utc });
        };
        // Called when global selection header changes dates
        _this.updateDateTimeAndRun = function (datetime) {
            _this.updateDateTime(datetime);
            _this.runQuery();
        };
        _this.updateField = function (field, value) {
            _this.props.queryBuilder.updateField(field, value);
            _this.forceUpdate();
        };
        _this.updateFields = function (query) {
            Object.entries(query).forEach(function (_a) {
                var _b = __read(_a, 2), field = _b[0], value = _b[1];
                _this.updateField(field, value);
            });
        };
        _this.updateAndRunQuery = function (query) {
            _this.updateFields(query);
            _this.runQuery();
        };
        _this.runQuery = function () {
            var _a = _this.props, queryBuilder = _a.queryBuilder, organization = _a.organization, location = _a.location;
            var resultManager = _this.state.resultManager;
            // Track query for analytics
            trackQuery(organization, queryBuilder.getExternal());
            // Strip any invalid conditions and aggregations
            var _b = queryBuilder.getInternal(), conditions = _b.conditions, aggregations = _b.aggregations;
            var filteredConditions = conditions.filter(function (condition) {
                return isValidCondition(condition, queryBuilder.getColumns());
            });
            var filteredAggregations = aggregations.filter(function (aggregation) {
                return isValidAggregation(aggregation, queryBuilder.getColumns());
            });
            if (filteredConditions.length !== conditions.length) {
                _this.updateField('conditions', filteredConditions);
            }
            if (filteredAggregations.length !== aggregations.length) {
                _this.updateField('aggregations', filteredAggregations);
            }
            _this.setState({ isFetchingQuery: true });
            resultManager
                .fetchAll()
                .then(function (data) {
                var shouldRedirect = !_this.props.params.savedQueryId;
                if (shouldRedirect) {
                    browserHistory.push({
                        pathname: "/organizations/" + organization.slug + "/discover/",
                        // This is kind of a hack, but this causes a re-render in result where this.props === nextProps after
                        // a query has completed... we don't preserve `state` when we update browser history, so
                        // if this is present in `Result.shouldComponentUpdate` then should perform a render
                        state: 'fetching',
                        // Don't drop "visualization" from querystring
                        search: getQueryStringFromQuery(queryBuilder.getInternal(), __assign({}, (location.query.visualization && {
                            visualization: location.query.visualization,
                        }))),
                    });
                }
                _this.setState({
                    data: data,
                    isFetchingQuery: false,
                });
            })
                .catch(function (err) {
                var message = (err && err.message) || t('An error occurred');
                addErrorMessage(message);
                _this.setState({ isFetchingQuery: false });
            });
        };
        _this.onFetchPage = function (nextOrPrev) {
            _this.setState({ isFetchingQuery: true });
            return _this.state.resultManager
                .fetchPage(nextOrPrev)
                .then(function (data) {
                _this.setState({ data: data, isFetchingQuery: false });
            })
                .catch(function (err) {
                var message = (err && err.message) || t('An error occurred');
                addErrorMessage(message);
                _this.setState({ isFetchingQuery: false });
            });
        };
        _this.toggleSidebar = function (view) {
            if (view !== _this.state.view) {
                _this.setState({ view: view });
                browserHistory.replace({
                    pathname: "/organizations/" + _this.props.organization.slug + "/discover/",
                    query: __assign(__assign({}, _this.props.location.query), { view: view }),
                });
            }
        };
        _this.loadSavedQueries = function () {
            browserHistory.push({
                pathname: "/organizations/" + _this.props.organization.slug + "/discover/",
                query: { view: 'saved' },
            });
        };
        _this.reset = function () {
            var _a = _this.props, savedQuery = _a.savedQuery, queryBuilder = _a.queryBuilder, organization = _a.organization;
            if (savedQuery) {
                queryBuilder.reset(savedQuery);
                _this.setState({
                    isEditingSavedQuery: false,
                });
            }
            else {
                browserHistory.push({
                    pathname: "/organizations/" + organization.slug + "/discover/",
                });
            }
        };
        _this.deleteSavedQuery = function () {
            var _a = _this.props, organization = _a.organization, savedQuery = _a.savedQuery;
            var resultManager = _this.state.resultManager;
            deleteSavedQuery(organization, savedQuery.id)
                .then(function () {
                addSuccessMessage(tct('Successfully deleted query [name]', {
                    name: savedQuery.name,
                }));
                resultManager.reset();
                _this.loadSavedQueries();
            })
                .catch(function () {
                addErrorMessage(t('Could not delete query'));
                _this.setState({ isFetchingQuery: false });
            });
        };
        _this.updateSavedQuery = function (name) {
            var _a = _this.props, queryBuilder = _a.queryBuilder, savedQuery = _a.savedQuery, organization = _a.organization, toggleEditMode = _a.toggleEditMode;
            var query = queryBuilder.getInternal();
            var data = __assign(__assign({}, query), { name: name });
            updateSavedQuery(organization, savedQuery.id, data)
                .then(function (resp) {
                addSuccessMessage(t('Updated query'));
                toggleEditMode(); // Return to read-only mode
                _this.props.updateSavedQueryData(resp);
            })
                .catch(function () {
                addErrorMessage(t('Could not update query'));
            });
        };
        _this.onGoLegacyDiscover = function () {
            localStorage.setItem('discover:version', '2');
            var user = ConfigStore.get('user');
            trackAnalyticsEvent({
                eventKey: 'discover_v2.opt_in',
                eventName: 'Discoverv2: Go to discover2',
                organization_id: parseInt(_this.props.organization.id, 10),
                user_id: parseInt(user.id, 10),
            });
        };
        var resultManager = createResultManager(props.queryBuilder);
        _this.state = {
            resultManager: resultManager,
            data: resultManager.getAll(),
            isFetchingQuery: false,
            isEditingSavedQuery: props.isEditingSavedQuery,
            savedQueryName: null,
            view: props.view || 'query',
        };
        return _this;
    }
    Discover.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        var queryBuilder = nextProps.queryBuilder, search = nextProps.location.search, savedQuery = nextProps.savedQuery, isEditingSavedQuery = nextProps.isEditingSavedQuery, params = nextProps.params, isLoading = nextProps.isLoading;
        var resultManager = this.state.resultManager;
        // Run query on isLoading change if there is a querystring or saved search
        var loadingStatusChanged = isLoading !== this.props.isLoading;
        if (loadingStatusChanged && (savedQuery || !!search)) {
            this.runQuery();
            return;
        }
        if (savedQuery && savedQuery !== this.props.savedQuery) {
            this.setState({ view: 'saved' });
            this.runQuery();
        }
        if (isEditingSavedQuery !== this.props.isEditingSavedQuery) {
            this.setState({ isEditingSavedQuery: isEditingSavedQuery });
            return;
        }
        if (!queryHasChanged(this.props.location.search, nextProps.location.search)) {
            return;
        }
        var newQuery = getQueryFromQueryString(search);
        // Clear data only if location.search is empty (reset has been called)
        if (!search && !params.savedQueryId) {
            queryBuilder.reset(newQuery);
            resultManager.reset();
            this.setState({
                data: resultManager.getAll(),
            });
        }
        else if (search) {
            // This indicates navigation changes (e.g. back button on browser)
            // We need to update our search store and probably runQuery
            var projects = newQuery.projects, range = newQuery.range, start = newQuery.start, end = newQuery.end, utc = newQuery.utc;
            if (projects) {
                this.updateProjects(projects);
            }
            this.updateDateTime({
                period: range || null,
                start: start || null,
                end: end || null,
                utc: typeof utc !== 'undefined' ? utc : null,
            });
            // These props come from URL string, so will always be in UTC
            updateDateTime({
                start: (start && new Date(moment.utc(start).local())) || null,
                end: (end && new Date(moment.utc(end).local())) || null,
                period: range || null,
                utc: typeof utc !== 'undefined' ? utc : null,
            });
            this.runQuery();
        }
    };
    Discover.prototype.renderSidebarNav = function () {
        var _this = this;
        var view = this.state.view;
        var views = [
            { id: 'query', title: t('New query') },
            { id: 'saved', title: t('Saved queries') },
        ];
        return (<React.Fragment>
        <SidebarTabs underlined>
          {views.map(function (_a) {
            var id = _a.id, title = _a.title;
            return (<li key={id} className={view === id ? 'active' : ''}>
              <a onClick={function () { return _this.toggleSidebar(id); }}>{title}</a>
            </li>);
        })}
        </SidebarTabs>
      </React.Fragment>);
    };
    Discover.prototype.render = function () {
        var _a = this.state, data = _a.data, isFetchingQuery = _a.isFetchingQuery, view = _a.view, resultManager = _a.resultManager, isEditingSavedQuery = _a.isEditingSavedQuery;
        var _b = this.props, queryBuilder = _b.queryBuilder, organization = _b.organization, savedQuery = _b.savedQuery, toggleEditMode = _b.toggleEditMode, isLoading = _b.isLoading, location = _b.location, utc = _b.utc;
        var shouldDisplayResult = resultManager.shouldDisplayResult();
        return (<DiscoverContainer>
        <Sidebar>
          {this.renderSidebarNav()}
          {view === 'saved' && (<SavedQueryWrapper>
              <SavedQueryList organization={organization} savedQuery={savedQuery}/>
            </SavedQueryWrapper>)}
          {view === 'query' && (<NewQuery organization={organization} queryBuilder={queryBuilder} isFetchingQuery={isFetchingQuery || isLoading} onUpdateField={this.updateField} onRunQuery={this.runQuery} onReset={this.reset} isLoading={isLoading}/>)}
          {isEditingSavedQuery && savedQuery && (<QueryPanel title={t('Edit Query')} onClose={toggleEditMode}>
              <EditSavedQuery savedQuery={savedQuery} queryBuilder={queryBuilder} isFetchingQuery={isFetchingQuery} onUpdateField={this.updateField} onRunQuery={this.runQuery} onDeleteQuery={this.deleteSavedQuery} onSaveQuery={this.updateSavedQuery} isLoading={isLoading}/>
            </QueryPanel>)}
        </Sidebar>

        <DiscoverGlobalSelectionHeader organization={organization} hasCustomRouting showEnvironmentSelector={false} onChangeProjects={this.updateProjects} onUpdateProjects={this.runQuery} onChangeTime={this.changeTime} onUpdateTime={this.updateDateTimeAndRun}/>
        <Body>
          <BodyContent>
            {shouldDisplayResult && (<Result location={location} utc={utc} data={data} savedQuery={savedQuery} onToggleEdit={toggleEditMode} onFetchPage={this.onFetchPage}/>)}
            {!shouldDisplayResult && (<React.Fragment>
                <div>
                  <HeadingContainer>
                    <PageHeading>{t('Discover')}</PageHeading>
                  </HeadingContainer>
                </div>
                <Intro updateQuery={this.updateAndRunQuery}/>
              </React.Fragment>)}
            {isFetchingQuery && <ResultLoading />}
          </BodyContent>
        </Body>
      </DiscoverContainer>);
    };
    Discover.defaultProps = {
        utc: true,
    };
    return Discover;
}(React.Component));
export default Discover;
//# sourceMappingURL=discover.jsx.map