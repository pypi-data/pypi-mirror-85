import { __read } from "tslib";
import { NEGATION_OPERATORS, NULL_OPERATORS, WILDCARD_OPERATORS, } from 'app/views/discover/data';
import { defined } from 'app/utils';
var checkIsNegation = function (operator) { return NEGATION_OPERATORS.includes(operator); };
var checkIsNull = function (operator) { return NULL_OPERATORS.includes(operator); };
var checkIsWildcard = function (operator) { return WILDCARD_OPERATORS.includes(operator); };
function getDiscoverConditionToSearchString(condition) {
    var _a = __read(condition, 3), field = _a[0], operator = _a[1], value = _a[2];
    var isNegation = checkIsNegation(operator);
    var negationStr = isNegation ? '!' : '';
    if (checkIsNull(operator)) {
        return "" + negationStr + field + ":\"\"";
    }
    var coercedValue = value;
    if (!defined(coercedValue)) {
        coercedValue = '';
    }
    if (checkIsWildcard(operator)) {
        // Do we support both?
        coercedValue = ("" + coercedValue).replace(/%/g, '*');
    }
    // TODO(billy): Handle number operators on server
    return "" + negationStr + field + ":" + coercedValue;
}
export function getDiscoverConditionsToSearchString(conditions) {
    if (conditions === void 0) { conditions = []; }
    return conditions.map(getDiscoverConditionToSearchString).join(' ').trim();
}
//# sourceMappingURL=getDiscoverConditionsToSearchString.jsx.map