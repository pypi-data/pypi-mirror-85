import { __assign, __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import Breadcrumbs from 'app/components/breadcrumbs';
import { decodeScalar } from 'app/utils/queryString';
import { getPerformanceLandingUrl } from './utils';
import { transactionSummaryRouteWithQuery } from './transactionSummary/utils';
import { vitalsRouteWithQuery } from './transactionVitals/utils';
var Breadcrumb = /** @class */ (function (_super) {
    __extends(Breadcrumb, _super);
    function Breadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Breadcrumb.prototype.getCrumbs = function () {
        var crumbs = [];
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, eventSlug = _a.eventSlug, transactionComparison = _a.transactionComparison, realUserMonitoring = _a.realUserMonitoring;
        var performanceTarget = {
            pathname: getPerformanceLandingUrl(organization),
            query: __assign(__assign({}, location.query), { 
                // clear out the transaction name
                transaction: undefined }),
        };
        crumbs.push({
            to: performanceTarget,
            label: t('Performance'),
            preserveGlobalSelection: true,
        });
        if (transactionName) {
            if (realUserMonitoring) {
                var rumTarget = vitalsRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: rumTarget,
                    label: t('Web Vitals'),
                    preserveGlobalSelection: true,
                });
            }
            else {
                var summaryTarget = transactionSummaryRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: summaryTarget,
                    label: t('Transaction Summary'),
                    preserveGlobalSelection: true,
                });
            }
        }
        if (transactionName && eventSlug) {
            crumbs.push({
                to: '',
                label: t('Event Details'),
            });
        }
        else if (transactionComparison) {
            crumbs.push({
                to: '',
                label: t('Compare to Baseline'),
            });
        }
        return crumbs;
    };
    Breadcrumb.prototype.render = function () {
        return <Breadcrumbs crumbs={this.getCrumbs()}/>;
    };
    return Breadcrumb;
}(React.Component));
export default Breadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map