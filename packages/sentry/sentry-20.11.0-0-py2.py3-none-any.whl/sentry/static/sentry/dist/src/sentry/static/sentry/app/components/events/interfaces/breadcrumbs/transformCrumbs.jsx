import { __assign } from "tslib";
import convertCrumbType from './convertCrumbType';
import getCrumbDetails from './getCrumbDetails';
import { BreadcrumbLevelType } from './types';
var transformCrumbs = function (breadcrumbs) {
    return breadcrumbs.map(function (breadcrumb, index) {
        var _a;
        var convertedCrumbType = convertCrumbType(breadcrumb);
        var crumbDetails = getCrumbDetails(convertedCrumbType.type);
        return __assign(__assign(__assign({ id: index }, convertedCrumbType), crumbDetails), { level: (_a = convertedCrumbType === null || convertedCrumbType === void 0 ? void 0 : convertedCrumbType.level) !== null && _a !== void 0 ? _a : BreadcrumbLevelType.UNDEFINED });
    });
};
export default transformCrumbs;
//# sourceMappingURL=transformCrumbs.jsx.map