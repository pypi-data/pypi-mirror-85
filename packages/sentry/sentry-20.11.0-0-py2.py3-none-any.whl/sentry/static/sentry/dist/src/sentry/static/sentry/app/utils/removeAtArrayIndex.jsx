import { __read, __spread } from "tslib";
/**
 * Remove item at `index` in `array` without mutating `array`
 */
export function removeAtArrayIndex(array, index) {
    var newArray = __spread(array);
    newArray.splice(index, 1);
    return newArray;
}
//# sourceMappingURL=removeAtArrayIndex.jsx.map