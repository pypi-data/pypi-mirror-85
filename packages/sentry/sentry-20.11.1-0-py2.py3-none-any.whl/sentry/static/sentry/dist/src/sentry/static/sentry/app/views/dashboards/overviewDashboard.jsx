import { __extends, __rest } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Dashboard from './dashboard';
import overviewDashboard from './data/dashboards/overviewDashboard';
var OverviewDashboard = /** @class */ (function (_super) {
    __extends(OverviewDashboard, _super);
    function OverviewDashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OverviewDashboard.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return [['releases', "/organizations/" + orgId + "/releases/"]];
    };
    OverviewDashboard.prototype.getTitle = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return t('Dashboard') + " - " + orgId;
    };
    OverviewDashboard.prototype.renderLoading = function () {
        // We don't want a loading state
        return this.renderBody();
    };
    OverviewDashboard.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases;
        if (!releases) {
            return null;
        }
        // Passing the rest of `this.props` to `<Dashboard>` for tests
        var _b = this.props, router = _b.router, props = __rest(_b, ["router"]);
        return (<Dashboard releases={releases} releasesLoading={loading} router={router} {...overviewDashboard} {...props}/>);
    };
    return OverviewDashboard;
}(AsyncView));
export default OverviewDashboard;
//# sourceMappingURL=overviewDashboard.jsx.map