import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as ReactRouter from 'react-router';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import * as Sentry from '@sentry/react';
import { t, tct } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { fetchTotalCount } from 'app/actionCreators/events';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import { fetchProjectsCount } from 'app/actionCreators/projects';
import Alert from 'app/components/alert';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { IconFlag } from 'app/icons';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import Confirm from 'app/components/confirm';
import space from 'app/styles/space';
import SearchBar from 'app/views/events/searchBar';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { generateAggregateFields } from 'app/utils/discover/fields';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import EventView, { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
import { generateQueryWithTag } from 'app/utils';
import localStorage from 'app/utils/localStorage';
import { decodeScalar } from 'app/utils/queryString';
import * as Layout from 'app/components/layouts/thirds';
import { DEFAULT_EVENT_VIEW } from './data';
import Table from './table';
import Tags from './tags';
import ResultsHeader from './resultsHeader';
import ResultsChart from './resultsChart';
import { generateTitle } from './utils';
import { addRoutePerformanceContext } from '../performance/utils';
var SHOW_TAGS_STORAGE_KEY = 'discover2:show-tags';
function readShowTagsState() {
    var value = localStorage.getItem(SHOW_TAGS_STORAGE_KEY);
    return value === '1';
}
var Results = /** @class */ (function (_super) {
    __extends(Results, _super);
    function Results() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: EventView.fromLocation(_this.props.location),
            error: '',
            errorCode: 200,
            totalValues: null,
            showTags: readShowTagsState(),
            needConfirmation: false,
            confirmedQuery: false,
            incompatibleAlertNotice: null,
        };
        _this.canLoadEvents = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, location, organization, eventView, needConfirmation, confirmedQuery, currentQuery, duration, projectLength, results, err_1;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, location = _a.location, organization = _a.organization;
                        eventView = this.state.eventView;
                        needConfirmation = false;
                        confirmedQuery = true;
                        currentQuery = eventView.getEventsAPIPayload(location);
                        duration = eventView.getDays();
                        if (!(duration > 30 && currentQuery.project)) return [3 /*break*/, 5];
                        projectLength = currentQuery.project.length;
                        if (!(projectLength === 0 ||
                            (projectLength === 1 && currentQuery.project[0] === '-1'))) return [3 /*break*/, 4];
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchProjectsCount(api, organization.slug)];
                    case 2:
                        results = _b.sent();
                        if (projectLength === 0)
                            projectLength = results.myProjects;
                        else
                            projectLength = results.allProjects;
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        return [3 /*break*/, 4];
                    case 4:
                        if (projectLength > 10) {
                            needConfirmation = true;
                            confirmedQuery = false;
                        }
                        _b.label = 5;
                    case 5:
                        // Once confirmed, a change of project or datetime will happen before this can set it to false,
                        // this means a query will still happen even if the new conditions need confirmation
                        // using a state callback to return this to false
                        this.setState({ needConfirmation: needConfirmation, confirmedQuery: confirmedQuery }, function () {
                            _this.setState({ confirmedQuery: false });
                        });
                        if (needConfirmation) {
                            this.openConfirm();
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        _this.openConfirm = function () { };
        _this.setOpenFunction = function (_a) {
            var open = _a.open;
            _this.openConfirm = open;
            return null;
        };
        _this.handleConfirmed = function () { return __awaiter(_this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                this.setState({ needConfirmation: false, confirmedQuery: true }, function () {
                    _this.setState({ confirmedQuery: false });
                });
                return [2 /*return*/];
            });
        }); };
        _this.handleCancelled = function () {
            _this.setState({ needConfirmation: false, confirmedQuery: false });
        };
        _this.handleChangeShowTags = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'discover_v2.results.toggle_tag_facets',
                eventName: 'Discoverv2: Toggle Tag Facets',
                organization_id: parseInt(organization.id, 10),
            });
            _this.setState(function (state) {
                var newValue = !state.showTags;
                localStorage.setItem(SHOW_TAGS_STORAGE_KEY, newValue ? '1' : '0');
                return __assign(__assign({}, state), { showTags: newValue });
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            router.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.handleYAxisChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = __assign(__assign({}, location.query), { yAxis: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat axis changing like the user already confirmed the query
            if (!_this.state.needConfirmation) {
                _this.handleConfirmed();
            }
            trackAnalyticsEvent({
                eventKey: 'discover_v2.y_axis_change',
                eventName: "Discoverv2: Change chart's y axis",
                organization_id: parseInt(_this.props.organization.id, 10),
                y_axis_value: value,
            });
        };
        _this.handleDisplayChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = __assign(__assign({}, location.query), { display: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            // Treat display changing like the user already confirmed the query
            if (!_this.state.needConfirmation) {
                _this.handleConfirmed();
            }
        };
        _this.generateTagUrl = function (key, value) {
            var organization = _this.props.organization;
            var eventView = _this.state.eventView;
            var url = eventView.getResultsViewUrlTarget(organization.slug);
            url.query = generateQueryWithTag(url.query, {
                key: key,
                value: value,
            });
            return url;
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'error',
                errors: errors,
                organization_id: organization.id,
                url: window.location.href,
            });
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error, errorCode) {
            _this.setState({ error: error, errorCode: errorCode });
        };
        return _this;
    }
    Results.getDerivedStateFromProps = function (nextProps, prevState) {
        var eventView = EventView.fromLocation(nextProps.location);
        return __assign(__assign({}, prevState), { eventView: eventView });
    };
    Results.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
        this.checkEventView();
        this.canLoadEvents();
    };
    Results.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, api = _a.api, location = _a.location, organization = _a.organization, selection = _a.selection;
        var _b = this.state, eventView = _b.eventView, confirmedQuery = _b.confirmedQuery;
        this.checkEventView();
        var currentQuery = eventView.getEventsAPIPayload(location);
        var prevQuery = prevState.eventView.getEventsAPIPayload(prevProps.location);
        if (!isAPIPayloadSimilar(currentQuery, prevQuery)) {
            api.clear();
            this.canLoadEvents();
        }
        if (!isEqual(prevProps.selection.datetime, selection.datetime) ||
            !isEqual(prevProps.selection.projects, selection.projects)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
        if (prevState.confirmedQuery !== confirmedQuery)
            this.fetchTotalCount();
    };
    Results.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, _b, eventView, confirmedQuery, totals, err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location;
                        _b = this.state, eventView = _b.eventView, confirmedQuery = _b.confirmedQuery;
                        if (confirmedQuery === false || !eventView.isValid()) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, eventView.getEventsAPIPayload(location))];
                    case 2:
                        totals = _c.sent();
                        this.setState({ totalValues: totals });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        Sentry.captureException(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Results.prototype.checkEventView = function () {
        var _a;
        var eventView = this.state.eventView;
        if (eventView.isValid()) {
            return;
        }
        // If the view is not valid, redirect to a known valid state.
        var _b = this.props, location = _b.location, organization = _b.organization, selection = _b.selection;
        var nextEventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        if (nextEventView.project.length === 0 && selection.projects) {
            nextEventView.project = selection.projects;
        }
        if ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) {
            nextEventView.query = decodeScalar(location.query.query) || '';
        }
        ReactRouter.browserHistory.replace(nextEventView.getResultsViewUrlTarget(organization.slug));
    };
    Results.prototype.getDocumentTitle = function () {
        var organization = this.props.organization;
        var eventView = this.state.eventView;
        if (!eventView) {
            return '';
        }
        return generateTitle({ eventView: eventView, organization: organization });
    };
    Results.prototype.renderTagsTable = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var _b = this.state, eventView = _b.eventView, totalValues = _b.totalValues, confirmedQuery = _b.confirmedQuery;
        return (<Layout.Side>
        <Tags generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location} confirmedQuery={confirmedQuery}/>
      </Layout.Side>);
    };
    Results.prototype.renderError = function (error) {
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon={<IconFlag size="md"/>}>
        {error}
      </Alert>);
    };
    Results.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router;
        var _b = this.state, eventView = _b.eventView, error = _b.error, errorCode = _b.errorCode, totalValues = _b.totalValues, showTags = _b.showTags, incompatibleAlertNotice = _b.incompatibleAlertNotice, confirmedQuery = _b.confirmedQuery;
        var fields = eventView.hasAggregateField()
            ? generateAggregateFields(organization, eventView.fields)
            : eventView.fields;
        var query = decodeScalar(location.query.query) || '';
        var title = this.getDocumentTitle();
        return (<SentryDocumentTitle title={title} objSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <ResultsHeader errorCode={errorCode} organization={organization} location={location} eventView={eventView} onIncompatibleAlertQuery={this.handleIncompatibleQuery}/>
            <Layout.Body>
              {incompatibleAlertNotice && <Top fullWidth>{incompatibleAlertNotice}</Top>}
              <Top fullWidth>
                {this.renderError(error)}
                <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={fields} onSearch={this.handleSearch}/>
                <ResultsChart router={router} organization={organization} eventView={eventView} location={location} onAxisChange={this.handleYAxisChange} onDisplayChange={this.handleDisplayChange} total={totalValues} confirmedQuery={confirmedQuery}/>
              </Top>
              <Layout.Main fullWidth={!showTags}>
                <Table organization={organization} eventView={eventView} location={location} title={title} setError={this.setError} onChangeShowTags={this.handleChangeShowTags} showTags={showTags} confirmedQuery={confirmedQuery}/>
              </Layout.Main>
              {showTags ? this.renderTagsTable() : null}
              <Confirm priority="primary" header={<strong>{t('May lead to thumb twiddling')}</strong>} confirmText={t('Do it')} cancelText={t('Nevermind')} onConfirm={this.handleConfirmed} onCancel={this.handleCancelled} message={<p>
                    {tct("You've created a query that will search for events made\n                      [dayLimit:over more than 30 days] for [projectLimit:more than 10 projects].\n                      A lot has happened during that time, so this might take awhile.\n                      Are you sure you want to do this?", {
            dayLimit: <strong />,
            projectLimit: <strong />,
        })}
                  </p>}>
                {this.setOpenFunction}
              </Confirm>
            </Layout.Body>
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return Results;
}(React.Component));
export var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export var Top = styled(Layout.Main)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 0;\n"], ["\n  flex-grow: 0;\n"])));
function ResultsContainer(props) {
    /**
     * Block `<Results>` from mounting until GSH is ready since there are API
     * requests being performed on mount.
     *
     * Also, we skip loading last used projects if you have multiple projects feature as
     * you no longer need to enforce a project if it is empty. We assume an empty project is
     * the desired behavior because saved queries can contain a project filter.
     */
    return (<GlobalSelectionHeader skipLoadLastUsed={props.organization.features.includes('global-views')}>
      <Results {...props}/>
    </GlobalSelectionHeader>);
}
export default withApi(withOrganization(withGlobalSelection(ResultsContainer)));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=results.jsx.map