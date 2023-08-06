import moment from 'moment';
import { CONDITION_OPERATORS } from '../data';
var specialConditions = new Set(['IS NULL', 'IS NOT NULL']);
/**
 * Returns true if a condition is valid and false if not
 *
 * @param condition Condition in external Snuba format
 * @param cols List of column objects
 * @param cols.name Column name
 * @param cols.type Type of column
 * @returns True if valid condition, false if not
 */
export function isValidCondition(condition, cols) {
    var allOperators = new Set(CONDITION_OPERATORS);
    var columns = new Set(cols.map(function (_a) {
        var name = _a.name;
        return name;
    }));
    var isColValid = columns.has(condition[0] || '');
    var isOperatorValid = allOperators.has("" + condition[1]);
    var foundCol = cols.find(function (col) { return col.name === condition[0]; });
    var colType = (foundCol && foundCol.type) || {};
    var isValueValid = specialConditions.has("" + condition[1]) ||
        (colType === 'datetime' && condition[2] !== null) ||
        colType === typeof condition[2];
    return isColValid && isOperatorValid && isValueValid;
}
/***
 * Converts external Snuba format to internal format for dropdown
 *
 * @param external Condition in external Snuba format
 */
export function getInternal(external) {
    return external.join(' ').trim();
}
/***
 * Converts internal dropdown format to external Snuba format
 *
 * @param internal Condition in internal format
 * @param cols List of columns with name and type e.g. {name: 'message', type: 'string}
 * @returns {Array} condition Condition in external Snuba format
 */
export function getExternal(internal, columns) {
    if (internal === void 0) { internal = ''; }
    var external = [null, null, null];
    // Validate column
    var colValue = internal.split(' ')[0];
    if (new Set(columns.map(function (_a) {
        var name = _a.name;
        return name;
    })).has(colValue)) {
        external[0] = colValue;
    }
    // Validate operator
    var remaining = (external[0] !== null
        ? internal.replace(external[0], '')
        : internal).trim();
    // Check IS NULL and IS NOT NULL first
    if (specialConditions.has(remaining)) {
        external[1] = remaining;
    }
    else {
        CONDITION_OPERATORS.forEach(function (operator) {
            if (remaining.startsWith(operator)) {
                external[1] = operator;
            }
        });
    }
    // Validate value and convert to correct type
    if (external[0] && external[1] && !specialConditions.has("" + external[1])) {
        var strStart = external[0] + " " + external[1] + " ";
        if (internal.startsWith(strStart)) {
            external[2] = internal.replace(strStart, '');
        }
        var foundCol = columns.find(function (_a) {
            var name = _a.name;
            return name === colValue;
        });
        var type = foundCol && foundCol.type;
        if (type === 'number') {
            var num = parseInt("" + external[2], 10);
            external[2] = !isNaN(num) ? num : null;
        }
        if (type === 'boolean') {
            if (external[2] === 'true') {
                external[2] = true;
            }
            if (external[2] === 'false') {
                external[2] = false;
            }
        }
        if (type === 'datetime') {
            var date = moment.utc("" + external[2]);
            external[2] = date.isValid() ? date.format('YYYY-MM-DDTHH:mm:ss') : null;
        }
    }
    return external;
}
/**
 * Transform casing of condition operators to uppercase. Applies to the operators
 * IS NULL, IS NOT NULL, LIKE and NOT LIKE
 *
 * @param input Condition string as input by user
 */
export function ignoreCase(input) {
    if (input === void 0) { input = ''; }
    var colName = input.split(' ')[0];
    // Strip column name from the start
    var match = input.match(/^[\w._]+\s(.*)/);
    var remaining = match ? match[1] : null;
    if (!remaining) {
        return input;
    }
    for (var i = 0; i < CONDITION_OPERATORS.length; i++) {
        var operator = CONDITION_OPERATORS[i];
        if (operator.startsWith(remaining.toUpperCase())) {
            return colName + " " + remaining.toUpperCase();
        }
        else if (remaining.toUpperCase().startsWith(operator)) {
            return colName + " " + operator + " " + remaining.slice(operator.length + 1);
        }
    }
    return input;
}
//# sourceMappingURL=utils.jsx.map