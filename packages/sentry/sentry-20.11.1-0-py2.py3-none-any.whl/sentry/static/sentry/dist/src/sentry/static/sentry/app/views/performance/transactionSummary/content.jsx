import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import space from 'app/styles/space';
import { generateQueryWithTag } from 'app/utils';
import { getAggregateAlias } from 'app/utils/discover/fields';
import * as Layout from 'app/components/layouts/thirds';
import Tags from 'app/views/eventsV2/tags';
import SearchBar from 'app/views/events/searchBar';
import { decodeScalar } from 'app/utils/queryString';
import withProjects from 'app/utils/withProjects';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, } from 'app/views/performance/transactionVitals/constants';
import TransactionHeader, { Tab } from './header';
import TransactionList from './transactionList';
import UserStats from './userStats';
import TransactionSummaryCharts from './charts';
import RelatedIssues from './relatedIssues';
import SidebarCharts from './sidebarCharts';
import StatusBreakdown from './statusBreakdown';
var SummaryContent = /** @class */ (function (_super) {
    __extends(SummaryContent, _super);
    function SummaryContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = generateQueryWithTag(location.query, { key: key, value: value });
            return __assign(__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        return _this;
    }
    SummaryContent.prototype.render = function () {
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, totalValues = _a.totalValues;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query) || '';
        var totalCount = totalValues.count;
        var slowDuration = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95;
        // NOTE: This is not a robust check for whether or not a transaction is a front end
        // transaction, however it will suffice for now.
        var hasWebVitals = VITAL_GROUPS.some(function (group) {
            return group.vitals.some(function (vital) {
                var alias = getAggregateAlias("percentile(" + vital + ", " + VITAL_PERCENTILE + ")");
                return Number.isFinite(totalValues[alias]);
            });
        });
        return (<React.Fragment>
        <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.TransactionSummary} hasWebVitals={hasWebVitals} handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main>
            <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <TransactionSummaryCharts organization={organization} location={location} eventView={eventView} totalValues={totalCount}/>
            <TransactionList organization={organization} transactionName={transactionName} location={location} eventView={eventView} slowDuration={slowDuration}/>
            <RelatedIssues organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
          </Layout.Main>
          <Layout.Side>
            <UserStats organization={organization} location={location} totals={totalValues} transactionName={transactionName}/>
            <SidebarCharts organization={organization} eventView={eventView}/>
            <StatusBreakdown eventView={eventView} organization={organization} location={location}/>
            <Tags generateUrl={this.generateTagUrl} totalValues={totalCount} eventView={eventView} organization={organization} location={location}/>
          </Layout.Side>
        </Layout.Body>
      </React.Fragment>);
    };
    return SummaryContent;
}(React.Component));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default withProjects(SummaryContent);
var templateObject_1;
//# sourceMappingURL=content.jsx.map