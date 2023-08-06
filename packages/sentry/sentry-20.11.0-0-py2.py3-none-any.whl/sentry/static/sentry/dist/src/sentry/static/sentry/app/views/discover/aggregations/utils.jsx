import { __read } from "tslib";
/**
 * Returns true if an aggregation is valid and false if not
 *
 * @param aggregation Aggregation in external Snuba format
 * @param cols List of column objects
 * @param cols.name Column name
 * @param cols.type Type of column
 * @returns True if valid aggregation, false if not
 */
export function isValidAggregation(aggregation, cols) {
    var columns = new Set(cols.map(function (_a) {
        var name = _a.name;
        return name;
    }));
    var _a = __read(aggregation, 2), func = _a[0], col = _a[1];
    if (!func) {
        return false;
    }
    if (func === 'count()') {
        return !col;
    }
    if (func === 'uniq') {
        return columns.has(col || '');
    }
    if (func === 'avg' || func === 'sum') {
        var validCols = new Set(cols.filter(function (_a) {
            var type = _a.type;
            return type === 'number';
        }).map(function (_a) {
            var name = _a.name;
            return name;
        }));
        return validCols.has(col || '');
    }
    return false;
}
/**
 * Converts aggregation from external Snuba format to internal format for dropdown
 *
 * @param external Aggregation in external Snuba format
 * @return Aggregation in internal format
 */
export function getInternal(external) {
    var _a = __read(external, 2), func = _a[0], col = _a[1];
    if (!func) {
        return '';
    }
    if (func === 'count()') {
        return 'count';
    }
    if (func === 'uniq') {
        return "uniq(" + col + ")";
    }
    if (func === 'avg') {
        return "avg(" + col + ")";
    }
    if (func === 'sum') {
        return "sum(" + col + ")";
    }
    return func;
}
/**
 * Returns an alias for a given column name, which is either just the column name
 * or a string with an underscore instead of square brackets for tags. We'll also
 * replace the characters `.`, `:` and `-` from aliases.
 *
 * @param columnName Name of column
 * @return Alias
 */
function getAlias(columnName) {
    var tagMatch = columnName.match(/^tags\[(.+)]$/);
    return tagMatch
        ? "tags_" + tagMatch[1].replace(/[.:-]/, '_')
        : columnName.replace('.', '_');
}
/**
 * Converts aggregation internal string format to external Snuba representation
 *
 * @param internal Aggregation in internal format
 * @return Aggregation in external Snuba format
 */
export function getExternal(internal) {
    var uniqRegex = /^uniq\((.+)\)$/;
    var avgRegex = /^avg\((.+)\)$/;
    var sumRegex = /^sum\((.+)\)$/;
    var match = internal.match(uniqRegex);
    if (match && match[1]) {
        var column = match[1];
        return ['uniq', column, "uniq_" + getAlias(column)];
    }
    match = internal.match(avgRegex);
    if (match && match[1]) {
        var column = match[1];
        return ['avg', column, "avg_" + getAlias(column)];
    }
    match = internal.match(sumRegex);
    if (match && match[1]) {
        var column = match[1];
        return ['sum', column, "sum_" + getAlias(column)];
    }
    return ['count()', null, 'count'];
}
//# sourceMappingURL=utils.jsx.map