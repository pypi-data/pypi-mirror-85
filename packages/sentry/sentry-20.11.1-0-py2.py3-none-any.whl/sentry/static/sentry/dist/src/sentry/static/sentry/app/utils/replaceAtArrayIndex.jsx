import { __read, __spread } from "tslib";
/**
 * Replace item at `index` in `array` with `obj`
 */
export function replaceAtArrayIndex(array, index, obj) {
    var newArray = __spread(array);
    newArray.splice(index, 1, obj);
    return newArray;
}
//# sourceMappingURL=replaceAtArrayIndex.jsx.map