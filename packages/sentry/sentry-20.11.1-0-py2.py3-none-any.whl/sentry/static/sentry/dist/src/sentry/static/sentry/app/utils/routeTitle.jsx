function routeTitleGen(routeName, orgSlug, withSentry) {
    if (withSentry === void 0) { withSentry = true; }
    var tmpl = routeName + " - " + orgSlug;
    return withSentry ? tmpl + " - Sentry" : tmpl;
}
export default routeTitleGen;
//# sourceMappingURL=routeTitle.jsx.map