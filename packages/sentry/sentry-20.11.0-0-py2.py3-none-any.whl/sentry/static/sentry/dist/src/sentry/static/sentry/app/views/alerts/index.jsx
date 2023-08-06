import { __extends } from "tslib";
import React from 'react';
import withOrganization from 'app/utils/withOrganization';
import Feature from 'app/components/acl/feature';
var AlertsContainer = /** @class */ (function (_super) {
    __extends(AlertsContainer, _super);
    function AlertsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertsContainer.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization;
        return (<Feature organization={organization} features={['incidents']}>
        {function (_a) {
            var hasMetricAlerts = _a.hasFeature;
            return (<React.Fragment>
            {children && React.isValidElement(children)
                ? React.cloneElement(children, {
                    organization: organization,
                    hasMetricAlerts: hasMetricAlerts,
                })
                : children}
          </React.Fragment>);
        }}
      </Feature>);
    };
    return AlertsContainer;
}(React.Component));
export default withOrganization(AlertsContainer);
//# sourceMappingURL=index.jsx.map