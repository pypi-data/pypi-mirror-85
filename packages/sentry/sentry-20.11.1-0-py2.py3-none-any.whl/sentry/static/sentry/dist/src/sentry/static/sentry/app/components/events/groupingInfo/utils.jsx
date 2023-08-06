import { __values } from "tslib";
import isObject from 'lodash/isObject';
export function hasNonContributingComponent(component) {
    var e_1, _a;
    if (!(component === null || component === void 0 ? void 0 : component.contributes)) {
        return true;
    }
    try {
        for (var _b = __values(component.values), _c = _b.next(); !_c.done; _c = _b.next()) {
            var value = _c.value;
            if (isObject(value) && hasNonContributingComponent(value)) {
                return true;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return false;
}
export function shouldInlineComponentValue(component) {
    return component.values.every(function (value) { return !isObject(value); });
}
export function groupingComponentFilter(value, showNonContributing) {
    if (isObject(value)) {
        // no point rendering such nodes at all, we never show them
        if (!value.contributes && !value.hint && value.values.length === 0) {
            return false;
        }
        // non contributing values are otherwise optional
        if (!showNonContributing && !value.contributes) {
            return false;
        }
    }
    return true;
}
//# sourceMappingURL=utils.jsx.map