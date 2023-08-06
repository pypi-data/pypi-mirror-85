/**
 * Converts a stream query to an object representation, with
 * keys representing tag names, and the magic __text key
 * representing the text component of the search.
 *
 * Example:
 *
 * "python is:unresolved assigned:foo@bar.com"
 * => {
 *      __text: "python",
 *      is: "unresolved",
 *      assigned: "foo@bar.com"
 *    }
 */
import { __read, __rest } from "tslib";
export function queryToObj(queryStr) {
    if (queryStr === void 0) { queryStr = ''; }
    var text = [];
    var queryItems = queryStr.match(/\S+:"[^"]*"?|\S+/g);
    var queryObj = (queryItems || []).reduce(function (obj, item) {
        var index = item.indexOf(':');
        if (index === -1) {
            text.push(item);
        }
        else {
            var tagKey = item.slice(0, index);
            var value = item.slice(index + 1).replace(/^"|"$/g, '');
            obj[tagKey] = value;
        }
        return obj;
    }, {});
    queryObj.__text = '';
    if (text.length) {
        queryObj.__text = text.join(' ');
    }
    return queryObj;
}
/**
 * Converts an object representation of a stream query to a string
 * (consumable by the Sentry stream HTTP API).
 */
export function objToQuery(queryObj) {
    var __text = queryObj.__text, tags = __rest(queryObj, ["__text"]);
    var parts = Object.entries(tags).map(function (_a) {
        var _b = __read(_a, 2), tagKey = _b[0], value = _b[1];
        if (value.indexOf(' ') > -1) {
            value = "\"" + value + "\"";
        }
        return tagKey + ":" + value;
    });
    if (queryObj.__text) {
        parts.push(queryObj.__text);
    }
    return parts.join(' ');
}
//# sourceMappingURL=stream.jsx.map