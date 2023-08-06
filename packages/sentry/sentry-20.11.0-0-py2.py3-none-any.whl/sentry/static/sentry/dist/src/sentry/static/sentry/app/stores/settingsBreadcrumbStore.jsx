import Reflux from 'reflux';
import SettingsBreadcrumbActions from 'app/actions/settingsBreadcrumbActions';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
var storeConfig = {
    pathMap: {},
    init: function () {
        this.reset();
        this.listenTo(SettingsBreadcrumbActions.mapTitle, this.onUpdateRouteMap);
        this.listenTo(SettingsBreadcrumbActions.trimMappings, this.onTrimMappings);
    },
    reset: function () {
        this.pathMap = {};
    },
    onUpdateRouteMap: function (_a) {
        var routes = _a.routes, title = _a.title;
        this.pathMap[getRouteStringFromRoutes(routes)] = title;
        this.trigger(this.pathMap);
    },
    onTrimMappings: function (routes) {
        var routePath = getRouteStringFromRoutes(routes);
        for (var fullPath in this.pathMap) {
            if (!routePath.startsWith(fullPath)) {
                delete this.pathMap[fullPath];
            }
        }
        this.trigger(this.pathMap);
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=settingsBreadcrumbStore.jsx.map