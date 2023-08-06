import findLastIndex from 'lodash/findLastIndex';
/**
 * Creates a route string from an array of `routes` from react-router
 *
 * It will look for the last route path that begins with a `/` and
 * concatenate all of the following routes. Skips any routes without a path
 *
 * @param {Array<{}>} routes An array of route objects from react-router
 * @return String Returns a route path
 */
export default function getRouteStringFromRoutes(routes) {
    if (!Array.isArray(routes)) {
        return '';
    }
    var routesWithPaths = routes.filter(function (route) { return !!route.path; });
    var lastAbsolutePathIndex = findLastIndex(routesWithPaths, function (_a) {
        var path = _a.path;
        return path.startsWith('/');
    });
    return routesWithPaths
        .slice(lastAbsolutePathIndex)
        .filter(function (_a) {
        var path = _a.path;
        return !!path;
    })
        .map(function (_a) {
        var path = _a.path;
        return path;
    })
        .join('');
}
//# sourceMappingURL=getRouteStringFromRoutes.jsx.map