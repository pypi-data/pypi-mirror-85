import { __extends } from "tslib";
import React from 'react';
import ConfigStore from 'app/stores/configStore';
import withOrganization from 'app/utils/withOrganization';
import { isRenderFunc } from 'app/utils/isRenderFunc';
var Role = /** @class */ (function (_super) {
    __extends(Role, _super);
    function Role() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Role.prototype.hasRole = function () {
        var _a;
        var user = ConfigStore.get('user');
        var _b = this.props, organization = _b.organization, role = _b.role;
        var availableRoles = organization.availableRoles;
        var currentRole = (_a = organization.role) !== null && _a !== void 0 ? _a : '';
        if (!user) {
            return false;
        }
        if (user.isSuperuser) {
            return true;
        }
        if (!Array.isArray(availableRoles)) {
            return false;
        }
        var roleIds = availableRoles.map(function (r) { return r.id; });
        if (!roleIds.includes(role) || !roleIds.includes(currentRole)) {
            return false;
        }
        var requiredIndex = roleIds.indexOf(role);
        var currentIndex = roleIds.indexOf(currentRole);
        return currentIndex >= requiredIndex;
    };
    Role.prototype.render = function () {
        var children = this.props.children;
        var hasRole = this.hasRole();
        if (isRenderFunc(children)) {
            return children({ hasRole: hasRole });
        }
        return hasRole && children ? children : null;
    };
    return Role;
}(React.Component));
export default withOrganization(Role);
//# sourceMappingURL=role.jsx.map