import { __assign, __values } from "tslib";
import isArray from 'lodash/isArray';
import isObject from 'lodash/isObject';
import isString from 'lodash/isString';
import isUndefined from 'lodash/isUndefined';
import { appendTagCondition } from 'app/utils/queryString';
function arrayIsEqual(arr, other, deep) {
    // if the other array is a falsy value, return
    if (!arr && !other) {
        return true;
    }
    if (!arr || !other) {
        return false;
    }
    // compare lengths - can save a lot of time
    if (arr.length !== other.length) {
        return false;
    }
    return arr.every(function (val, idx) { return valueIsEqual(val, other[idx], deep); });
}
export function valueIsEqual(value, other, deep) {
    if (value === other) {
        return true;
    }
    else if (isArray(value) || isArray(other)) {
        if (arrayIsEqual(value, other, deep)) {
            return true;
        }
    }
    else if (isObject(value) || isObject(other)) {
        if (objectMatchesSubset(value, other, deep)) {
            return true;
        }
    }
    return false;
}
function objectMatchesSubset(obj, other, deep) {
    var k;
    if (obj === other) {
        return true;
    }
    if (!obj || !other) {
        return false;
    }
    if (deep !== true) {
        for (k in other) {
            if (obj[k] !== other[k]) {
                return false;
            }
        }
        return true;
    }
    for (k in other) {
        if (!valueIsEqual(obj[k], other[k], deep)) {
            return false;
        }
    }
    return true;
}
export function intcomma(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
export function sortArray(arr, score_fn) {
    arr.sort(function (a, b) {
        var a_score = score_fn(a), b_score = score_fn(b);
        for (var i = 0; i < a_score.length; i++) {
            if (a_score[i] > b_score[i]) {
                return 1;
            }
            if (a_score[i] < b_score[i]) {
                return -1;
            }
        }
        return 0;
    });
    return arr;
}
export function objectIsEmpty(obj) {
    if (obj === void 0) { obj = {}; }
    for (var prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            return false;
        }
    }
    return true;
}
export function trim(str) {
    return str.replace(/^\s+|\s+$/g, '');
}
/**
 * Replaces slug special chars with a space
 */
export function explodeSlug(slug) {
    return trim(slug.replace(/[-_]+/g, ' '));
}
export function defined(item) {
    return !isUndefined(item) && item !== null;
}
export function nl2br(str) {
    return str.replace(/(?:\r\n|\r|\n)/g, '<br />');
}
/**
 * This function has a critical security impact, make sure to check all usages before changing this function.
 * In some parts of our code we rely on that this only really is a string starting with http(s).
 */
export function isUrl(str) {
    return (!!str &&
        isString(str) &&
        (str.indexOf('http://') === 0 || str.indexOf('https://') === 0));
}
export function escape(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
export function percent(value, totalValue) {
    // prevent division by zero
    if (totalValue === 0) {
        return 0;
    }
    return (value / totalValue) * 100;
}
export function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}
export function formatBytes(bytes) {
    var units = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    var thresh = 1024;
    if (bytes < thresh) {
        return bytes + ' B';
    }
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while (bytes >= thresh);
    return bytes.toFixed(1) + ' ' + units[u];
}
export function getShortCommitHash(hash) {
    if (hash.match(/^[a-f0-9]{40}$/)) {
        hash = hash.substr(0, 7);
    }
    return hash;
}
export function parseRepo(repo) {
    if (typeof repo === 'string') {
        var re = /(?:github\.com|bitbucket\.org)\/([^\/]+\/[^\/]+)/i;
        var match = repo.match(re);
        var parsedRepo = match ? match[1] : repo;
        return parsedRepo;
    }
    return repo;
}
/**
 * Converts a multi-line textarea input value into an array,
 * eliminating empty lines
 */
export function extractMultilineFields(value) {
    return value
        .split('\n')
        .map(function (f) { return trim(f); })
        .filter(function (f) { return f !== ''; });
}
/**
 * If the value is of type Array, converts it to type string, keeping the line breaks, if there is any
 */
export function convertMultilineFieldValue(value) {
    if (Array.isArray(value)) {
        return value.join('\n');
    }
    if (typeof value === 'string') {
        return value.split('\n').join('\n');
    }
    return '';
}
function projectDisplayCompare(a, b) {
    if (a.isBookmarked !== b.isBookmarked) {
        return a.isBookmarked ? -1 : 1;
    }
    return a.slug.localeCompare(b.slug);
}
// Sort a list of projects by bookmarkedness, then by id
export function sortProjects(projects) {
    return projects.sort(projectDisplayCompare);
}
//build actorIds
export var buildUserId = function (id) { return "user:" + id; };
export var buildTeamId = function (id) { return "team:" + id; };
/**
 * Removes the organization / project scope prefix on feature names.
 */
export function descopeFeatureName(feature) {
    if (typeof feature !== 'string') {
        return feature;
    }
    var results = feature.match(/(?:^(?:projects|organizations):)?(.*)/);
    if (results && results.length > 0) {
        return results.pop();
    }
    return feature;
}
export function isWebpackChunkLoadingError(error) {
    return (error &&
        typeof error.message === 'string' &&
        error.message.toLowerCase().includes('loading chunk'));
}
export function deepFreeze(object) {
    var e_1, _a;
    // Retrieve the property names defined on object
    var propNames = Object.getOwnPropertyNames(object);
    try {
        // Freeze properties before freezing self
        for (var propNames_1 = __values(propNames), propNames_1_1 = propNames_1.next(); !propNames_1_1.done; propNames_1_1 = propNames_1.next()) {
            var name_1 = propNames_1_1.value;
            var value = object[name_1];
            object[name_1] = value && typeof value === 'object' ? deepFreeze(value) : value;
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (propNames_1_1 && !propNames_1_1.done && (_a = propNames_1.return)) _a.call(propNames_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return Object.freeze(object);
}
export function generateQueryWithTag(prevQuery, tag) {
    var query = __assign({}, prevQuery);
    // some tags are dedicated query strings since other parts of the app consumes this,
    // for example, the global selection header.
    switch (tag.key) {
        case 'environment':
            query.environment = tag.value;
            break;
        case 'project':
            query.project = tag.value;
            break;
        default:
            query.query = appendTagCondition(query.query, tag.key, tag.value);
    }
    return query;
}
export var isFunction = function (value) { return typeof value === 'function'; };
// NOTE: only escapes a " if it's not already escaped
export function escapeDoubleQuotes(str) {
    return str.replace(/\\([\s\S])|(")/g, '\\$1$2');
}
//# sourceMappingURL=utils.jsx.map