import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import * as ReactRouter from 'react-router';
import { stringify } from 'query-string';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import styled from '@emotion/styled';
import { PageContent } from 'app/styles/organization';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import ConfigStore from 'app/stores/configStore';
import Feature from 'app/components/acl/feature';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SearchBar from 'app/components/searchBar';
import Switch from 'app/components/switch';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { DEFAULT_EVENT_VIEW } from './data';
import { getPrebuiltQueries, isBannerHidden, setBannerHidden, shouldRenderPrebuilt, setRenderPrebuilt, } from './utils';
import QueryList from './queryList';
import Banner from './banner';
var SORT_OPTIONS = [
    { label: t('My Queries'), value: 'myqueries' },
    { label: t('Recently Edited'), value: '-dateUpdated' },
    { label: t('Query Name (A-Z)'), value: 'name' },
    { label: t('Date Created (Newest)'), value: '-dateCreated' },
    { label: t('Date Created (Oldest)'), value: 'dateCreated' },
    { label: t('Most Outdated'), value: 'dateUpdated' },
];
var DiscoverLanding = /** @class */ (function (_super) {
    __extends(DiscoverLanding, _super);
    function DiscoverLanding() {
        var _a, _b;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.mq = (_a = window.matchMedia) === null || _a === void 0 ? void 0 : _a.call(window, "(max-width: " + theme.breakpoints[1] + ")");
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            // local component state
            isBannerHidden: isBannerHidden(),
            renderPrebuilt: shouldRenderPrebuilt(),
            isSmallBanner: (_b = _this.mq) === null || _b === void 0 ? void 0 : _b.matches,
            savedQueries: null,
            savedQueriesPageLinks: '',
        };
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                isSmallBanner: changed.matches,
            });
        };
        _this.shouldReload = true;
        _this.handleQueryChange = function () {
            _this.fetchData({ reloading: true });
        };
        _this.handleBannerClick = function () {
            setBannerHidden(true);
            _this.setState({ isBannerHidden: true });
        };
        _this.handleSearchQuery = function (searchQuery) {
            var location = _this.props.location;
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        _this.handleSortChange = function (value) {
            var location = _this.props.location;
            trackAnalyticsEvent({
                eventKey: 'discover_v2.change_sort',
                eventName: 'Discoverv2: Sort By Changed',
                organization_id: parseInt(_this.props.organization.id, 10),
                sort: value,
            });
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        _this.togglePrebuilt = function () {
            var renderPrebuilt = _this.state.renderPrebuilt;
            _this.setState({ renderPrebuilt: !renderPrebuilt }, function () {
                setRenderPrebuilt(!renderPrebuilt);
            });
            _this.fetchData();
        };
        _this.onGoLegacyDiscover = function () {
            localStorage.setItem('discover:version', '1');
            var user = ConfigStore.get('user');
            trackAnalyticsEvent({
                eventKey: 'discover_v2.opt_out',
                eventName: 'Discoverv2: Go to discover',
                organization_id: parseInt(_this.props.organization.id, 10),
                user_id: parseInt(user.id, 10),
            });
        };
        return _this;
    }
    DiscoverLanding.prototype.componentDidMount = function () {
        if (this.mq) {
            this.mq.addListener(this.handleMediaQueryChange);
        }
    };
    DiscoverLanding.prototype.componentWillUnmount = function () {
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
        }
    };
    DiscoverLanding.prototype.getSavedQuerySearchQuery = function () {
        var location = this.props.location;
        return String(decodeScalar(location.query.query) || '').trim();
    };
    DiscoverLanding.prototype.getActiveSort = function () {
        var location = this.props.location;
        var urlSort = location.query.sort ? decodeScalar(location.query.sort) : 'myqueries';
        return SORT_OPTIONS.find(function (item) { return item.value === urlSort; }) || SORT_OPTIONS[0];
    };
    DiscoverLanding.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var views = getPrebuiltQueries(organization);
        var searchQuery = this.getSavedQuerySearchQuery();
        var cursor = decodeScalar(location.query.cursor);
        var perPage = 9;
        if (!cursor && shouldRenderPrebuilt()) {
            // invariant: we're on the first page
            if (searchQuery && searchQuery.length > 0) {
                var needleSearch_1 = searchQuery.toLowerCase();
                var numOfPrebuiltQueries = views.reduce(function (sum, view) {
                    var eventView = EventView.fromNewQueryWithLocation(view, location);
                    // if a search is performed on the list of queries, we filter
                    // on the pre-built queries
                    if (eventView.name && eventView.name.toLowerCase().includes(needleSearch_1)) {
                        return sum + 1;
                    }
                    return sum;
                }, 0);
                perPage = Math.max(1, perPage - numOfPrebuiltQueries);
            }
            else {
                perPage = Math.max(1, perPage - views.length);
            }
        }
        var queryParams = {
            cursor: cursor,
            query: "version:2 name:\"" + searchQuery + "\"",
            per_page: perPage,
            sortBy: this.getActiveSort().value,
        };
        if (!cursor) {
            delete queryParams.cursor;
        }
        return [
            [
                'savedQueries',
                "/organizations/" + organization.slug + "/discover/saved/",
                {
                    query: queryParams,
                },
            ],
        ];
    };
    DiscoverLanding.prototype.componentDidUpdate = function (prevProps) {
        var isHidden = isBannerHidden();
        if (isHidden !== this.state.isBannerHidden) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({
                isBannerHidden: isHidden,
            });
        }
        var PAYLOAD_KEYS = ['sort', 'cursor', 'query'];
        var payloadKeysChanged = !isEqual(pick(prevProps.location.query, PAYLOAD_KEYS), pick(this.props.location.query, PAYLOAD_KEYS));
        // if any of the query strings relevant for the payload has changed,
        // we re-fetch data
        if (payloadKeysChanged) {
            this.fetchData();
        }
    };
    DiscoverLanding.prototype.renderBanner = function () {
        var bannerDismissed = this.state.isBannerHidden;
        if (bannerDismissed) {
            return null;
        }
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        var resultsUrl = to.pathname + "?" + stringify(to.query);
        return (<Banner organization={organization} resultsUrl={resultsUrl} isSmallBanner={this.state.isSmallBanner} onHideBanner={this.handleBannerClick}/>);
    };
    DiscoverLanding.prototype.renderActions = function () {
        var _this = this;
        var activeSort = this.getActiveSort();
        var _a = this.state, renderPrebuilt = _a.renderPrebuilt, savedQueries = _a.savedQueries;
        return (<StyledActions>
        <StyledSearchBar defaultQuery="" query={this.getSavedQuerySearchQuery()} placeholder={t('Search saved queries')} onSearch={this.handleSearchQuery}/>
        <PrebuiltSwitch>
          <SwitchLabel>Show Prebuilt</SwitchLabel>
          <Switch isActive={renderPrebuilt} isDisabled={renderPrebuilt && (savedQueries !== null && savedQueries !== void 0 ? savedQueries : []).length === 0} size="lg" toggle={this.togglePrebuilt}/>
        </PrebuiltSwitch>
        <DropdownControl buttonProps={{ prefix: t('Sort By') }} label={activeSort.label}>
          {SORT_OPTIONS.map(function (_a) {
            var label = _a.label, value = _a.value;
            return (<DropdownItem key={value} onSelect={_this.handleSortChange} eventKey={value} isActive={value === activeSort.value}>
              {label}
            </DropdownItem>);
        })}
        </DropdownControl>
      </StyledActions>);
    };
    DiscoverLanding.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    DiscoverLanding.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var _b = this.state, savedQueries = _b.savedQueries, savedQueriesPageLinks = _b.savedQueriesPageLinks, renderPrebuilt = _b.renderPrebuilt;
        return (<QueryList pageLinks={savedQueriesPageLinks} savedQueries={savedQueries !== null && savedQueries !== void 0 ? savedQueries : []} savedQuerySearchQuery={this.getSavedQuerySearchQuery()} renderPrebuilt={renderPrebuilt} location={location} organization={organization} onQueryChange={this.handleQueryChange}/>);
    };
    DiscoverLanding.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        return (<Feature organization={organization} features={['discover-query']} renderDisabled={this.renderNoAccess}>
        <SentryDocumentTitle title={t('Discover')} objSlug={organization.slug}>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <PageContent>
                <StyledPageHeader>
                  {t('Discover')}
                  <StyledButton data-test-id="build-new-query" to={to} priority="primary" onClick={function () {
            trackAnalyticsEvent({
                eventKey: 'discover_v2.build_new_query',
                eventName: 'Discoverv2: Build a new Discover Query',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
        }}>
                    {t('Build a new query')}
                  </StyledButton>
                </StyledPageHeader>
                {this.renderBanner()}
                {this.renderActions()}
                {this.renderComponent()}
              </PageContent>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </SentryDocumentTitle>
      </Feature>);
    };
    DiscoverLanding.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        location: PropTypes.object.isRequired,
        router: PropTypes.object.isRequired,
    };
    return DiscoverLanding;
}(AsyncComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var PrebuiltSwitch = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var SwitchLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-right: 8px;\n"], ["\n  padding-right: 8px;\n"])));
export var StyledPageHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(2));
var StyledSearchBar = styled(SearchBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content min-content;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content min-content;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, space(3));
var StyledButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
export default withOrganization(DiscoverLanding);
export { DiscoverLanding };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=landing.jsx.map