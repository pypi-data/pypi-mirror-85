import { __assign } from "tslib";
import * as queryString from 'query-string';
import parseurl from 'parseurl';
import isString from 'lodash/isString';
import { escapeDoubleQuotes } from 'app/utils';
// remove leading and trailing whitespace and remove double spaces
export function formatQueryString(qs) {
    return qs.trim().replace(/\s+/g, ' ');
}
export function addQueryParamsToExistingUrl(origUrl, queryParams) {
    var url = parseurl({ url: origUrl });
    if (!url) {
        return '';
    }
    // Order the query params alphabetically.
    // Otherwise ``queryString`` orders them randomly and it's impossible to test.
    var params = JSON.parse(JSON.stringify(queryParams));
    var query = url.query ? __assign(__assign({}, queryString.parse(url.query)), params) : params;
    return url.protocol + "//" + url.host + url.pathname + "?" + queryString.stringify(query);
}
/**
 * Append a tag key:value to a query string.
 *
 * Handles spacing and quoting if necessary.
 */
export function appendTagCondition(query, key, value) {
    var currentQuery = Array.isArray(query) ? query.pop() : isString(query) ? query : '';
    if (typeof value === 'string' && /[:\s\(\)\\"]/g.test(value)) {
        value = "\"" + escapeDoubleQuotes(value) + "\"";
    }
    if (currentQuery) {
        currentQuery += " " + key + ":" + value;
    }
    else {
        currentQuery = key + ":" + value;
    }
    return currentQuery;
}
export function decodeScalar(value) {
    if (!value) {
        return undefined;
    }
    var unwrapped = Array.isArray(value) && value.length > 0
        ? value[0]
        : isString(value)
            ? value
            : undefined;
    return isString(unwrapped) ? unwrapped : undefined;
}
export function decodeList(value) {
    if (!value) {
        return undefined;
    }
    return Array.isArray(value) ? value : isString(value) ? [value] : [];
}
export default {
    decodeList: decodeList,
    decodeScalar: decodeScalar,
    formatQueryString: formatQueryString,
    addQueryParamsToExistingUrl: addQueryParamsToExistingUrl,
    appendTagCondition: appendTagCondition,
};
//# sourceMappingURL=queryString.jsx.map