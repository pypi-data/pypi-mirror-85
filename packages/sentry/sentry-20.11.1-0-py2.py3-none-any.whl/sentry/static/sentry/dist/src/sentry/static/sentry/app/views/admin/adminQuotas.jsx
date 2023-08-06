import { __assign, __extends } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import { TextField } from 'app/components/forms';
import InternalStatChart from 'app/components/internalStatChart';
var AdminQuotas = /** @class */ (function (_super) {
    __extends(AdminQuotas, _super);
    function AdminQuotas() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminQuotas.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h' });
    };
    AdminQuotas.prototype.getEndpoints = function () {
        return [['config', '/internal/quotas/']];
    };
    AdminQuotas.prototype.renderBody = function () {
        var config = this.state.config;
        return (<div>
        <h3>Quotas</h3>

        <div className="box">
          <div className="box-header">
            <h4>Config</h4>
          </div>

          <div className="box-content with-padding">
            <TextField name="backend" value={config.backend} label="Backend" disabled/>
            <TextField name="rateLimit" value={config.options['system.rate-limit']} label="Rate Limit" disabled/>
          </div>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Total Events</h4>
          </div>
          <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat="events.total" label="Events"/>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Dropped Events</h4>
          </div>
          <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat="events.dropped" label="Events"/>
        </div>
      </div>);
    };
    return AdminQuotas;
}(AsyncView));
export default AdminQuotas;
//# sourceMappingURL=adminQuotas.jsx.map