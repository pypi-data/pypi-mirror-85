import findLastIndex from 'lodash/findLastIndex';
import replaceRouterParams from 'app/utils/replaceRouterParams';
/**
 * Given a route object or a string and a list of routes + params from router, this will attempt to recreate a location string while replacing url params.
 * Can additionally specify the number of routes to move back
 *
 * See tests for examples
 */
export default function recreateRoute(to, options) {
    var _a, _b;
    var routes = options.routes, params = options.params, location = options.location, stepBack = options.stepBack;
    var paths = routes.map(function (_a) {
        var path = _a.path;
        return path || '';
    });
    var lastRootIndex;
    var routeIndex;
    // TODO(ts): typescript things
    if (typeof to !== 'string') {
        routeIndex = routes.indexOf(to) + 1;
        lastRootIndex = findLastIndex(paths.slice(0, routeIndex), function (path) { return path[0] === '/'; });
    }
    else {
        lastRootIndex = findLastIndex(paths, function (path) { return path[0] === '/'; });
    }
    var baseRoute = paths.slice(lastRootIndex, routeIndex);
    if (typeof stepBack !== 'undefined') {
        baseRoute = baseRoute.slice(0, stepBack);
    }
    var search = (_a = location === null || location === void 0 ? void 0 : location.search) !== null && _a !== void 0 ? _a : '';
    var hash = (_b = location === null || location === void 0 ? void 0 : location.hash) !== null && _b !== void 0 ? _b : '';
    var fullRoute = "" + baseRoute.join('') + (typeof to !== 'string' ? '' : to) + search + hash;
    return replaceRouterParams(fullRoute, params);
}
//# sourceMappingURL=recreateRoute.jsx.map