/**
 * Given a route string, replace path parameters (e.g. `:id`) with value from `params`
 *
 * e.g. {id: 'test'}
 */
export default function replaceRouterParams(route, params) {
    // parse route params from route
    var matches = route.match(/:\w+/g);
    if (!matches || !matches.length) {
        return route;
    }
    // replace with current params
    matches.forEach(function (param) {
        var paramName = param.slice(1);
        if (typeof params[paramName] === 'undefined') {
            return;
        }
        route = route.replace(param, params[paramName]);
    });
    return route;
}
//# sourceMappingURL=replaceRouterParams.jsx.map