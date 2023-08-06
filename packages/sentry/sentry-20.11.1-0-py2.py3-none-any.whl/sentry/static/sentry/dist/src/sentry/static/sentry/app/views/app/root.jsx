import { __extends } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import { DEFAULT_APP_ROUTE } from 'app/constants';
import replaceRouterParams from 'app/utils/replaceRouterParams';
import withConfig from 'app/utils/withConfig';
/**
 * This view is used when a user lands on the route `/` which historically
 * is a server-rendered route which redirects the user to their last selected organization
 *
 * However, this does not work when in the experimental SPA mode (e.g. developing against a remote API,
 * or a deploy preview), so we must replicate the functionality and redirect
 * the user to the proper organization.
 *
 * TODO: There might be an edge case where user does not have `lastOrganization` set,
 * in which case we should load their list of organizations and make a decision
 */
var AppRoot = /** @class */ (function (_super) {
    __extends(AppRoot, _super);
    function AppRoot() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AppRoot.prototype.componentDidMount = function () {
        var config = this.props.config;
        if (config.lastOrganization) {
            browserHistory.replace(replaceRouterParams(DEFAULT_APP_ROUTE, { orgSlug: config.lastOrganization }));
        }
    };
    AppRoot.prototype.render = function () {
        return null;
    };
    return AppRoot;
}(React.Component));
export default withConfig(AppRoot);
//# sourceMappingURL=root.jsx.map