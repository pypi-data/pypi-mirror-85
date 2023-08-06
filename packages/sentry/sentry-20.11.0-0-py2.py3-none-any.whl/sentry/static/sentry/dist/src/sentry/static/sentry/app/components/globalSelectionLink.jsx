import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { Link as RouterLink } from 'react-router';
import * as qs from 'query-string';
import { extractSelectionParameters } from 'app/components/organizations/globalSelectionHeader/utils';
/**
 * A modified link used for navigating between organization level pages that
 * will keep the global selection values (projects, environments, time) in the
 * querystring when navigating if it's present
 *
 * Falls back to <a> if there is no router present.
 */
var GlobalSelectionLink = /** @class */ (function (_super) {
    __extends(GlobalSelectionLink, _super);
    function GlobalSelectionLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GlobalSelectionLink.prototype.render = function () {
        var location = this.context.location;
        var to = this.props.to;
        var globalQuery = extractSelectionParameters(location.query);
        var hasGlobalQuery = Object.keys(globalQuery).length > 0;
        var query = typeof to === 'object' && to.query ? __assign(__assign({}, globalQuery), to.query) : globalQuery;
        if (location) {
            var toWithGlobalQuery = void 0;
            if (hasGlobalQuery) {
                if (typeof to === 'string') {
                    toWithGlobalQuery = { pathname: to, query: query };
                }
                else {
                    toWithGlobalQuery = __assign(__assign({}, to), { query: query });
                }
            }
            var routerProps = hasGlobalQuery
                ? __assign(__assign({}, this.props), { to: toWithGlobalQuery }) : __assign(__assign({}, this.props), { to: to });
            return <RouterLink {...routerProps}>{this.props.children}</RouterLink>;
        }
        else {
            var queryStringObject = {};
            if (typeof to === 'object' && to.search) {
                queryStringObject = qs.parse(to.search);
            }
            queryStringObject = __assign(__assign({}, queryStringObject), globalQuery);
            if (typeof to === 'object' && to.query) {
                queryStringObject = __assign(__assign({}, queryStringObject), to.query);
            }
            var url = (typeof to === 'string' ? to : to.pathname) +
                '?' +
                qs.stringify(queryStringObject);
            return (<a {...this.props} href={url}>
          {this.props.children}
        </a>);
        }
    };
    GlobalSelectionLink.contextTypes = {
        location: PropTypes.object,
    };
    return GlobalSelectionLink;
}(React.Component));
export default GlobalSelectionLink;
//# sourceMappingURL=globalSelectionLink.jsx.map