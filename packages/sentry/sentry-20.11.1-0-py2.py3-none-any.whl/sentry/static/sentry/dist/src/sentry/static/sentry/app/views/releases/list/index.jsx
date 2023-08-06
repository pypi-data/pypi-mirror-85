import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { forceCheck } from 'react-lazyload';
import { t } from 'app/locale';
import space from 'app/styles/space';
import AsyncView from 'app/views/asyncView';
import { ReleaseStatus } from 'app/types';
import routeTitleGen from 'app/utils/routeTitle';
import SearchBar from 'app/components/searchBar';
import Pagination from 'app/components/pagination';
import PageHeading from 'app/components/pageHeading';
import withOrganization from 'app/utils/withOrganization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import LoadingIndicator from 'app/components/loadingIndicator';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { PageContent, PageHeader } from 'app/styles/organization';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { defined } from 'app/utils';
import ReleaseListSortOptions from './releaseListSortOptions';
import ReleaseLanding from './releaseLanding';
import IntroBanner from './introBanner';
import ReleaseCard from './releaseCard';
import ReleaseListDisplayOptions from './releaseListDisplayOptions';
import ReleaseArchivedNotice from '../detail/overview/releaseArchivedNotice';
var ReleasesList = /** @class */ (function (_super) {
    __extends(ReleasesList, _super);
    function ReleasesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleSort = function (sort) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, sort: sort }) }));
        };
        _this.handleDisplay = function (display) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, display: display }) }));
        };
        return _this;
    }
    ReleasesList.prototype.getTitle = function () {
        return routeTitleGen(t('Releases'), this.props.organization.slug, false);
    };
    ReleasesList.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var statsPeriod = location.query.statsPeriod;
        var sort = this.getSort();
        var display = this.getDisplay();
        var query = __assign(__assign({}, pick(location.query, [
            'project',
            'environment',
            'cursor',
            'query',
            'sort',
            'healthStatsPeriod',
            'healthStat',
        ])), { summaryStatsPeriod: statsPeriod, per_page: 25, health: 1, flatten: sort === 'date' ? 0 : 1, status: display === 'archived' ? ReleaseStatus.Archived : ReleaseStatus.Active });
        var endpoints = [
            ['releasesWithHealth', "/organizations/" + organization.slug + "/releases/", { query: query }],
        ];
        // when sorting by date we fetch releases without health and then fetch health lazily
        if (sort === 'date') {
            endpoints.push([
                'releasesWithoutHealth',
                "/organizations/" + organization.slug + "/releases/",
                { query: __assign(__assign({}, query), { health: 0 }) },
            ]);
        }
        return endpoints;
    };
    ReleasesList.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data, jqXHR = _a.jqXHR;
        var remainingRequests = this.state.remainingRequests;
        // make sure there's no withHealth/withoutHealth race condition and set proper loading state
        if (stateKey === 'releasesWithHealth' || remainingRequests === 1) {
            this.setState({
                reloading: false,
                loading: false,
                loadingHealth: stateKey === 'releasesWithoutHealth',
                releases: data,
                releasesPageLinks: jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link'),
            });
        }
    };
    ReleasesList.prototype.componentDidUpdate = function (prevProps, prevState) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
        if (prevState.releases !== this.state.releases) {
            /**
             * Manually trigger checking for elements in viewport.
             * Helpful when LazyLoad components enter the viewport without resize or scroll events,
             * https://github.com/twobin/react-lazyload#forcecheck
             *
             * HealthStatsCharts are being rendered only when they are scrolled into viewport.
             * This is how we re-check them without scrolling once releases change as this view
             * uses shouldReload=true and there is no reloading happening.
             */
            forceCheck();
        }
    };
    ReleasesList.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ReleasesList.prototype.getSort = function () {
        var sort = this.props.location.query.sort;
        return typeof sort === 'string' ? sort : 'date';
    };
    ReleasesList.prototype.getDisplay = function () {
        var display = this.props.location.query.display;
        return typeof display === 'string' ? display : 'active';
    };
    ReleasesList.prototype.shouldShowLoadingIndicator = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases, reloading = _a.reloading;
        return (loading && !reloading) || (loading && !(releases === null || releases === void 0 ? void 0 : releases.length));
    };
    ReleasesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderEmptyMessage = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var statsPeriod = location.query.statsPeriod;
        var searchQuery = this.getQuery();
        var activeSort = this.getSort();
        var display = this.getDisplay();
        if (searchQuery && searchQuery.length) {
            return (<EmptyStateWarning small>{t('There are no releases that match') + ": '" + searchQuery + "'."}</EmptyStateWarning>);
        }
        if (activeSort === 'users_24h') {
            return (<EmptyStateWarning small>
          {t('There are no releases with active user data (users in the last 24 hours).')}
        </EmptyStateWarning>);
        }
        if (activeSort !== 'date') {
            var relativePeriod = getRelativeSummary(statsPeriod || DEFAULT_STATS_PERIOD).toLowerCase();
            return (<EmptyStateWarning small>
          {t('There are no releases with data in the') + " " + relativePeriod + "."}
        </EmptyStateWarning>);
        }
        if (display === 'archived') {
            return (<EmptyStateWarning small>
          {t('There are no archived releases.')}
        </EmptyStateWarning>);
        }
        if (defined(statsPeriod) && statsPeriod !== '14d') {
            return <EmptyStateWarning small>{t('There are no releases.')}</EmptyStateWarning>;
        }
        return <ReleaseLanding organization={organization}/>;
    };
    ReleasesList.prototype.renderInnerBody = function () {
        var _a = this.props, location = _a.location, selection = _a.selection, organization = _a.organization;
        var _b = this.state, releases = _b.releases, reloading = _b.reloading, loadingHealth = _b.loadingHealth;
        if (this.shouldShowLoadingIndicator()) {
            return <LoadingIndicator />;
        }
        if (!(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return this.renderEmptyMessage();
        }
        return releases.map(function (release) { return (<ReleaseCard release={release} orgSlug={organization.slug} location={location} selection={selection} reloading={reloading} key={release.version + "-" + release.projects[0].slug} showHealthPlaceholders={loadingHealth}/>); });
    };
    ReleasesList.prototype.renderBody = function () {
        var organization = this.props.organization;
        var _a = this.state, releasesPageLinks = _a.releasesPageLinks, releases = _a.releases;
        return (<GlobalSelectionHeader showAbsolute={false} timeRangeHint={t('Changing this date range will recalculate the release metrics.')}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <StyledPageHeader>
              <PageHeading>{t('Releases')}</PageHeading>
              <SortAndFilterWrapper>
                <ReleaseListDisplayOptions selected={this.getDisplay()} onSelect={this.handleDisplay}/>
                <ReleaseListSortOptions selected={this.getSort()} onSelect={this.handleSort}/>
                <SearchBar placeholder={t('Search')} onSearch={this.handleSearch} query={this.getQuery()}/>
              </SortAndFilterWrapper>
            </StyledPageHeader>

            <IntroBanner />

            {this.getDisplay() === 'archived' && (releases === null || releases === void 0 ? void 0 : releases.length) > 0 && (<ReleaseArchivedNotice multi/>)}

            {this.renderInnerBody()}

            <Pagination pageLinks={releasesPageLinks}/>
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    return ReleasesList;
}(AsyncView));
var StyledPageHeader = styled(PageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-wrap: wrap;\n  margin-bottom: 0;\n  ", " {\n    margin-bottom: ", ";\n    margin-right: ", ";\n  }\n"], ["\n  flex-wrap: wrap;\n  margin-bottom: 0;\n  ", " {\n    margin-bottom: ", ";\n    margin-right: ", ";\n  }\n"])), PageHeading, space(2), space(2));
var SortAndFilterWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    width: 100%;\n    grid-template-columns: none;\n    grid-template-rows: 1fr 1fr 1fr;\n    margin-bottom: ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto auto 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    width: 100%;\n    grid-template-columns: none;\n    grid-template-rows: 1fr 1fr 1fr;\n    margin-bottom: ", ";\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[0]; }, space(4));
export default withOrganization(withGlobalSelection(ReleasesList));
export { ReleasesList };
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map