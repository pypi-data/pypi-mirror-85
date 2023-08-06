import { __extends } from "tslib";
import React from 'react';
import SentryTypes from 'app/sentryTypes';
var withOrganizationMock = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(WithOrganizationMockWrapper, _super);
        function WithOrganizationMockWrapper() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        WithOrganizationMockWrapper.prototype.render = function () {
            return (<WrappedComponent organization={this.context.organization || TestStubs.Organization()} {...this.props}/>);
        };
        return WithOrganizationMockWrapper;
    }(React.Component)),
    _a.contextTypes = {
        organization: SentryTypes.Organization,
    },
    _a; };
var isLightweightOrganization = function () { };
export default withOrganizationMock;
export { isLightweightOrganization };
//# sourceMappingURL=withOrganization.jsx.map