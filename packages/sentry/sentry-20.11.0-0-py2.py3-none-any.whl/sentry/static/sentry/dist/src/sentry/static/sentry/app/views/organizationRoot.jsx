import { __extends } from "tslib";
import { withRouter } from 'react-router';
import React from 'react';
import { setActiveProject } from 'app/actionCreators/projects';
import { setLastRoute } from 'app/actionCreators/navigation';
/**
 * This is the parent container for organization-level views such
 * as the Dashboard, Stats, Activity, etc...
 *
 * Currently is just used to unset active project
 */
var OrganizationRoot = /** @class */ (function (_super) {
    __extends(OrganizationRoot, _super);
    function OrganizationRoot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationRoot.prototype.componentDidMount = function () {
        setActiveProject(null);
    };
    OrganizationRoot.prototype.componentWillUnmount = function () {
        var location = this.props.location;
        var pathname = location.pathname, search = location.search;
        // Save last route so that we can jump back to view from settings
        setLastRoute("" + pathname + (search || ''));
    };
    OrganizationRoot.prototype.render = function () {
        return this.props.children;
    };
    return OrganizationRoot;
}(React.Component));
export { OrganizationRoot };
export default withRouter(OrganizationRoot);
//# sourceMappingURL=organizationRoot.jsx.map