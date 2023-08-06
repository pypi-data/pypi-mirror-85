import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import { updateDateTime } from 'app/actionCreators/globalSelection';
import SearchBar from 'app/views/events/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { PageContent } from 'app/styles/organization';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import Alert from 'app/components/alert';
import FeatureBadge from 'app/components/featureBadge';
import { generateAggregateFields } from 'app/utils/discover/fields';
import space from 'app/styles/space';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconFlag } from 'app/icons';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { tokenizeSearch, stringifyQueryObject, QueryResults, } from 'app/utils/tokenizeSearch';
import { decodeScalar } from 'app/utils/queryString';
import { generatePerformanceEventView, DEFAULT_STATS_PERIOD } from './data';
import Table from './table';
import Charts from './charts/index';
import Onboarding from './onboarding';
import { addRoutePerformanceContext, getTransactionSearchQuery } from './utils';
import TrendsContent from './trends/content';
import { modifyTrendsViewDefaultPeriod, DEFAULT_TRENDS_STATS_PERIOD, DEFAULT_MAX_DURATION, } from './trends/utils';
export var FilterViews;
(function (FilterViews) {
    FilterViews["ALL_TRANSACTIONS"] = "ALL_TRANSACTIONS";
    FilterViews["TRENDS"] = "TRENDS";
})(FilterViews || (FilterViews = {}));
function isStatsPeriodDefault(statsPeriod, defaultPeriod) {
    return !statsPeriod || defaultPeriod === statsPeriod;
}
var PerformanceLanding = /** @class */ (function (_super) {
    __extends(PerformanceLanding, _super);
    function PerformanceLanding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generatePerformanceEventView(_this.props.organization, _this.props.location),
            error: undefined,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        _this.handleSearch = function (searchQuery) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.search',
                eventName: 'Performance Views: Transaction overview search',
                organization_id: parseInt(organization.id, 10),
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        return _this;
    }
    PerformanceLanding.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generatePerformanceEventView(nextProps.organization, nextProps.location) });
    };
    PerformanceLanding.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
        trackAnalyticsEvent({
            eventKey: 'performance_views.overview.view',
            eventName: 'Performance Views: Transaction overview view',
            organization_id: parseInt(organization.id, 10),
        });
    };
    PerformanceLanding.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    PerformanceLanding.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon={<IconFlag size="md"/>}>
        {error}
      </Alert>);
    };
    PerformanceLanding.prototype.getViewLabel = function (currentView) {
        switch (currentView) {
            case FilterViews.ALL_TRANSACTIONS:
                return t('By Transaction');
            case FilterViews.TRENDS:
                return t('By Trend');
            default:
                throw Error("Unknown view: " + currentView);
        }
    };
    /**
     * Generate conditions to forward to the summary views.
     *
     * We drop the bare text string as in this view we apply it to
     * the transaction name, and that condition is redundant in the
     * summary view.
     */
    PerformanceLanding.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch(query);
        parsed.query = [];
        return stringifyQueryObject(parsed);
    };
    PerformanceLanding.prototype.getCurrentView = function () {
        var location = this.props.location;
        var currentView = location.query.view;
        if (Object.values(FilterViews).includes(currentView)) {
            return currentView;
        }
        return FilterViews.ALL_TRANSACTIONS;
    };
    PerformanceLanding.prototype.handleViewChange = function (viewKey) {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var newQuery = __assign({}, location.query);
        var query = decodeScalar(location.query.query) || '';
        var statsPeriod = decodeScalar(location.query.statsPeriod);
        var conditions = tokenizeSearch(query);
        var currentView = location.query.view;
        var newDefaultPeriod = viewKey === FilterViews.TRENDS ? DEFAULT_TRENDS_STATS_PERIOD : DEFAULT_STATS_PERIOD;
        var hasStartAndEnd = newQuery.start && newQuery.end;
        if (!hasStartAndEnd && isStatsPeriodDefault(statsPeriod, newDefaultPeriod)) {
            /**
             * Resets stats period to default of the tab you are navigating to
             * on tab change as tabs have different default periods.
             */
            updateDateTime({
                start: null,
                end: null,
                utc: false,
                period: newDefaultPeriod,
            });
        }
        trackAnalyticsEvent({
            eventKey: 'performance_views.change_view',
            eventName: 'Performance Views: Change View',
            organization_id: parseInt(organization.id, 10),
            view_name: viewKey,
        });
        if (viewKey === FilterViews.TRENDS) {
            var modifiedConditions = new QueryResults([]);
            if (conditions.hasTag('tpm()')) {
                modifiedConditions.setTagValues('tpm()', conditions.getTagValues('tpm()'));
            }
            else {
                modifiedConditions.setTagValues('tpm()', ['>0.01']);
            }
            if (conditions.hasTag('transaction.duration')) {
                modifiedConditions.setTagValues('transaction.duration', conditions.getTagValues('transaction.duration'));
            }
            else {
                modifiedConditions.setTagValues('transaction.duration', [
                    '>0',
                    "<" + DEFAULT_MAX_DURATION,
                ]);
            }
            newQuery.query = stringifyQueryObject(modifiedConditions);
        }
        var isNavigatingAwayFromTrends = viewKey !== FilterViews.TRENDS && currentView;
        if (isNavigatingAwayFromTrends) {
            // This stops errors from occurring when navigating to other views since we are appending aggregates to the trends view
            conditions.removeTag('tpm()');
            conditions.removeTag('transaction.duration');
            newQuery.query = stringifyQueryObject(conditions);
        }
        browserHistory.push({
            pathname: location.pathname,
            query: __assign(__assign({}, newQuery), { view: viewKey }),
        });
    };
    PerformanceLanding.prototype.renderHeaderButtons = function () {
        var _this = this;
        var views = [FilterViews.ALL_TRANSACTIONS, FilterViews.TRENDS];
        return (<ButtonBar merged active={this.getCurrentView()}>
        {views.map(function (viewKey) { return (<Button key={viewKey} barId={viewKey} size="small" data-test-id={'landing-header-' + viewKey.toLowerCase()} onClick={function () { return _this.handleViewChange(viewKey); }}>
            {_this.getViewLabel(viewKey)}
            {viewKey === FilterViews.TRENDS && <StyledFeatureBadge type="new"/>}
          </Button>); })}
      </ButtonBar>);
    };
    PerformanceLanding.prototype.shouldShowOnboarding = function () {
        var _a = this.props, projects = _a.projects, demoMode = _a.demoMode;
        var eventView = this.state.eventView;
        // XXX used by getsentry to bypass onboarding for the upsell demo state.
        if (demoMode) {
            return false;
        }
        if (projects.length === 0) {
            return false;
        }
        // Current selection is 'my projects' or 'all projects'
        if (eventView.project.length === 0 || eventView.project === [ALL_ACCESS_PROJECTS]) {
            return (projects.filter(function (p) { return p.firstTransactionEvent === false; }).length === projects.length);
        }
        // Any other subset of projects.
        return (projects.filter(function (p) {
            return eventView.project.includes(parseInt(p.id, 10)) &&
                p.firstTransactionEvent === false;
        }).length === eventView.project.length);
    };
    PerformanceLanding.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects;
        var currentView = this.getCurrentView();
        var isTrendsView = currentView === FilterViews.TRENDS;
        var eventView = isTrendsView
            ? modifyTrendsViewDefaultPeriod(this.state.eventView, location)
            : this.state.eventView;
        var showOnboarding = this.shouldShowOnboarding();
        var filterString = getTransactionSearchQuery(location);
        var summaryConditions = this.getSummaryConditions(filterString);
        return (<SentryDocumentTitle title={t('Performance')} objSlug={organization.slug}>
        <GlobalSelectionHeader defaultSelection={{
            datetime: {
                start: null,
                end: null,
                utc: false,
                period: isTrendsView ? DEFAULT_TRENDS_STATS_PERIOD : DEFAULT_STATS_PERIOD,
            },
        }}>
          <PageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <StyledPageHeader>
                <div>{t('Performance')}</div>
                {!showOnboarding && <div>{this.renderHeaderButtons()}</div>}
              </StyledPageHeader>
              {this.renderError()}
              {showOnboarding ? (<Onboarding organization={organization}/>) : currentView === FilterViews.TRENDS ? (<TrendsContent organization={organization} location={location} eventView={eventView} setError={this.setError}/>) : (<div>
                  <StyledSearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={generateAggregateFields(organization, __spread(eventView.fields, [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={this.handleSearch}/>
                  <Charts eventView={eventView} organization={organization} location={location} router={router}/>
                  <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={this.setError} summaryConditions={summaryConditions}/>
                </div>)}
            </LightWeightNoProjectMessage>
          </PageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return PerformanceLanding;
}(React.Component));
export var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n\n  margin-bottom: ", ";\n"])), space(2));
var StyledFeatureBadge = styled(FeatureBadge)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  height: 12px;\n"], ["\n  height: 12px;\n"])));
export default withApi(withOrganization(withProjects(withGlobalSelection(PerformanceLanding))));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=landing.jsx.map