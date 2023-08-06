import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import * as Layout from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { decodeScalar } from 'app/utils/queryString';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import SearchBar from 'app/views/events/searchBar';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import VitalsPanel from './vitalsPanel';
import TransactionHeader, { Tab } from '../transactionSummary/header';
import { FILTER_OPTIONS, ZOOM_KEYS } from './constants';
var VitalsContent = /** @class */ (function (_super) {
    __extends(VitalsContent, _super);
    function VitalsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            delete queryParams.cursor;
            browserHistory.push({
                pathname: location.pathname,
                query: queryParams,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.handleResetView = function () {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.reset_view',
                eventName: 'Performance Views: Reset vitals view',
                organization_id: organization.id,
            });
            var query = __assign({}, location.query);
            // reset all zoom parameters when resetting the view
            ZOOM_KEYS.forEach(function (key) { return delete query[key]; });
            browserHistory.push({
                pathname: location.pathname,
                query: query,
            });
        };
        _this.handleFilterChange = function (value) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.filter_changed',
                eventName: 'Performance Views: Change vitals filter',
                organization_id: organization.id,
                value: value,
            });
            var query = __assign(__assign({}, location.query), { cursor: undefined, dataFilter: value });
            // reset all zoom parameters when changing the filter
            ZOOM_KEYS.forEach(function (key) { return delete query[key]; });
            browserHistory.push({
                pathname: location.pathname,
                query: query,
            });
        };
        return _this;
    }
    VitalsContent.prototype.getActiveFilter = function () {
        var location = this.props.location;
        var dataFilter = location.query.dataFilter
            ? decodeScalar(location.query.dataFilter)
            : FILTER_OPTIONS[0].value;
        return FILTER_OPTIONS.find(function (item) { return item.value === dataFilter; }) || FILTER_OPTIONS[0];
    };
    VitalsContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, projects = _a.projects, organization = _a.organization;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query) || '';
        var activeFilter = this.getActiveFilter();
        var isZoomed = ZOOM_KEYS.map(function (key) { return location.query[key]; }).some(function (value) { return value !== undefined; });
        return (<React.Fragment>
        <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.RealUserMonitoring} hasWebVitals handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            <StyledActions>
              <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
              <DropdownControl buttonProps={{ prefix: t('Filter') }} label={activeFilter.label}>
                {FILTER_OPTIONS.map(function (_a) {
            var label = _a.label, value = _a.value;
            return (<DropdownItem key={value} onSelect={_this.handleFilterChange} eventKey={value} isActive={value === activeFilter.value}>
                    {label}
                  </DropdownItem>);
        })}
              </DropdownControl>
              <Button onClick={this.handleResetView} disabled={!isZoomed} data-test-id="reset-view">
                {t('Reset View')}
              </Button>
            </StyledActions>
            <VitalsPanel organization={organization} location={location} eventView={eventView} dataFilter={activeFilter.value}/>
          </Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return VitalsContent;
}(React.Component));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2), space(3));
export default VitalsContent;
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map