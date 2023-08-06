import { __read } from "tslib";
import React from 'react';
/**
 * Parses matches from fuse.js library
 *
 * Example `match` would be
 *
 *   {
 *    value: 'Authentication tokens allow you to perform actions',
 *    indices: [[4, 6], [12, 13], [15, 16]],
 *   }
 *
 * So:
 *
 *   00-03 -> not highlighted,
 *   04-06 -> highlighted,
 *   07-11 -> not highlighted,
 *   12-13 -> highlighted,
 *   ...etc
 *
 * @param match The match object from fuse
 * @param match.value The entire string that has matches
 * @param match.indices Array of indices that represent matches
 */
var getFuseMatches = function (_a) {
    var value = _a.value, indices = _a.indices;
    if (indices.length === 0) {
        return [{ highlight: false, text: value }];
    }
    var strLength = value.length;
    var result = [];
    var prev = [0, -1];
    indices.forEach(function (_a) {
        var _b = __read(_a, 2), start = _b[0], end = _b[1];
        // Unhighlighted string before the match
        var stringBeforeMatch = value.substring(prev[1] + 1, start);
        // Only add to result if non-empty string
        if (!!stringBeforeMatch) {
            result.push({
                highlight: false,
                text: stringBeforeMatch,
            });
        }
        // This is the matched string, which should be highlighted
        var matchedString = value.substring(start, end + 1);
        result.push({
            highlight: true,
            text: matchedString,
        });
        prev = [start, end];
    });
    // The rest of the string starting from the last match index
    var restOfString = value.substring(prev[1] + 1, strLength);
    // Only add to result if non-empty string
    if (!!restOfString) {
        result.push({ highlight: false, text: restOfString });
    }
    return result;
};
/**
 * Given a match object from fuse.js, returns an array of components with
 * "highlighted" (bold) substrings.
 */
var highlightFuseMatches = function (matchObj, Marker) {
    if (Marker === void 0) { Marker = 'mark'; }
    return getFuseMatches(matchObj).map(function (_a, index) {
        var highlight = _a.highlight, text = _a.text;
        if (!text) {
            return null;
        }
        if (highlight) {
            return <Marker key={index}>{text}</Marker>;
        }
        return <span key={index}>{text}</span>;
    });
};
export { getFuseMatches };
export default highlightFuseMatches;
//# sourceMappingURL=highlightFuseMatches.jsx.map