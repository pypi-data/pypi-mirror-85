import { __assign, __read } from "tslib";
import { defined } from 'app/utils';
import { BreadcrumbType } from './types';
function convertCrumbType(breadcrumb) {
    if (breadcrumb.type === BreadcrumbType.EXCEPTION) {
        return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.ERROR });
    }
    // special case for 'ui.' and `sentry.` category breadcrumbs
    // TODO: find a better way to customize UI around non-schema data
    if (breadcrumb.type === BreadcrumbType.DEFAULT && defined(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category)) {
        var _a = __read(breadcrumb.category.split('.'), 2), category = _a[0], subcategory = _a[1];
        if (category === 'ui') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.UI });
        }
        if (category === 'console') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.DEBUG });
        }
        if (category === 'navigation') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.NAVIGATION });
        }
        if (category === 'sentry' &&
            (subcategory === 'transaction' || subcategory === 'event')) {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.TRANSACTION });
        }
    }
    if (!Object.values(BreadcrumbType).includes(breadcrumb.type)) {
        return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.DEFAULT });
    }
    return breadcrumb;
}
export default convertCrumbType;
//# sourceMappingURL=convertCrumbType.jsx.map