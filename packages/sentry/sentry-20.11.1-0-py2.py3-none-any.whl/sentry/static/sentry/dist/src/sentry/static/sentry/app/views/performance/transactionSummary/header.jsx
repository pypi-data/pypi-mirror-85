import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import FeatureBadge from 'app/components/featureBadge';
import CreateAlertButton from 'app/components/createAlertButton';
import * as Layout from 'app/components/layouts/thirds';
import ButtonBar from 'app/components/buttonBar';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { decodeScalar } from 'app/utils/queryString';
import KeyTransactionButton from './keyTransactionButton';
import { transactionSummaryRouteWithQuery } from './utils';
import { vitalsRouteWithQuery } from '../transactionVitals/utils';
export var Tab;
(function (Tab) {
    Tab[Tab["TransactionSummary"] = 0] = "TransactionSummary";
    Tab[Tab["RealUserMonitoring"] = 1] = "RealUserMonitoring";
})(Tab || (Tab = {}));
var TransactionHeader = /** @class */ (function (_super) {
    __extends(TransactionHeader, _super);
    function TransactionHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.trackVitalsTabClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.vitals_tab_clicked',
                eventName: 'Performance Views: Vitals tab clicked',
                organization_id: organization.id,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            var _a, _b;
            _this.trackAlertClick(errors);
            (_b = (_a = _this.props).handleIncompatibleQuery) === null || _b === void 0 ? void 0 : _b.call(_a, incompatibleAlertNoticeFn, errors);
        };
        _this.handleCreateAlertSuccess = function () {
            _this.trackAlertClick();
        };
        return _this;
    }
    TransactionHeader.prototype.trackAlertClick = function (errors) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.summary.create_alert_clicked',
            eventName: 'Performance Views: Create alert clicked',
            organization_id: organization.id,
            status: errors ? 'error' : 'success',
            errors: errors,
            url: window.location.href,
        });
    };
    TransactionHeader.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<CreateAlertButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={this.handleCreateAlertSuccess} referrer="performance"/>);
    };
    TransactionHeader.prototype.renderKeyTransactionButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, transactionName = _a.transactionName;
        return (<KeyTransactionButton transactionName={transactionName} eventView={eventView} organization={organization}/>);
    };
    TransactionHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, currentTab = _a.currentTab, hasWebVitals = _a.hasWebVitals;
        var summaryTarget = transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        var vitalsTarget = vitalsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        return (<Layout.Header>
        <Layout.HeaderContent>
          <Breadcrumb organization={organization} location={location} transactionName={transactionName} realUserMonitoring={currentTab === Tab.RealUserMonitoring}/>
          <Layout.Title>{transactionName}</Layout.Title>
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          <ButtonBar gap={1}>
            <Feature organization={organization} features={['incidents']}>
              {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderCreateAlertButton();
        }}
            </Feature>
            {this.renderKeyTransactionButton()}
          </ButtonBar>
        </Layout.HeaderActions>
        <React.Fragment>
          <StyledNavTabs>
            <ListLink to={summaryTarget} isActive={function () { return currentTab === Tab.TransactionSummary; }}>
              {t('Overview')}
            </ListLink>
            {hasWebVitals && (<ListLink to={vitalsTarget} isActive={function () { return currentTab === Tab.RealUserMonitoring; }}>
                {t('Web Vitals')}
                <FeatureBadge type="new"/>
              </ListLink>)}
          </StyledNavTabs>
        </React.Fragment>
      </Layout.Header>);
    };
    return TransactionHeader;
}(React.Component));
var StyledNavTabs = styled(NavTabs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
export default TransactionHeader;
var templateObject_1;
//# sourceMappingURL=header.jsx.map