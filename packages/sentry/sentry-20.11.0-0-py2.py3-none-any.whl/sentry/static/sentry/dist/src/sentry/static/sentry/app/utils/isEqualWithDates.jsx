import isDate from 'lodash/isDate';
import isEqualWith from 'lodash/isEqualWith';
// `lodash.isEqual` does not compare date objects
function dateComparator(value, other) {
    if (isDate(value) && isDate(other)) {
        return +value === +other;
    }
    // Loose checking
    if (!value && !other) {
        return true;
    }
    // returning undefined will use default comparator
    return undefined;
}
export var isEqualWithDates = function (a, b) { return isEqualWith(a, b, dateComparator); };
//# sourceMappingURL=isEqualWithDates.jsx.map