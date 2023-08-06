import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import SentryTypes from 'app/sentryTypes';
import getDisplayName from 'app/utils/getDisplayName';
var withOrganization = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _a = this.props, organization = _a.organization, props = __rest(_a, ["organization"]);
            return (<WrappedComponent {...__assign({ organization: organization !== null && organization !== void 0 ? organization : this.context.organization }, props)}/>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withOrganization(" + getDisplayName(WrappedComponent) + ")",
    _a.contextTypes = {
        organization: SentryTypes.Organization,
    },
    _a; };
export function isLightweightOrganization(organization) {
    var castedOrg = organization;
    return !(castedOrg.projects && castedOrg.teams);
}
export default withOrganization;
//# sourceMappingURL=withOrganization.jsx.map