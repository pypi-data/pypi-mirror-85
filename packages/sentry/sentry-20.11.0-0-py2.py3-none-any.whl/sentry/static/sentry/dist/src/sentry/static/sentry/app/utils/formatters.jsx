import { __read } from "tslib";
import { Release } from '@sentry/release-parser';
import round from 'lodash/round';
import { t, tn } from 'app/locale';
export function userDisplayName(user, includeEmail) {
    var _a, _b;
    if (includeEmail === void 0) { includeEmail = true; }
    var displayName = String((_a = user === null || user === void 0 ? void 0 : user.name) !== null && _a !== void 0 ? _a : t('Unknown author')).trim();
    if (displayName.length <= 0) {
        displayName = t('Unknown author');
    }
    var email = String((_b = user === null || user === void 0 ? void 0 : user.email) !== null && _b !== void 0 ? _b : '').trim();
    if (email.length > 0 && email !== displayName && includeEmail) {
        displayName += ' (' + email + ')';
    }
    return displayName;
}
export var formatVersion = function (rawVersion, withPackage) {
    if (withPackage === void 0) { withPackage = false; }
    try {
        var parsedVersion = new Release(rawVersion);
        var versionToDisplay = parsedVersion.describe();
        if (versionToDisplay.length) {
            return "" + versionToDisplay + (withPackage && parsedVersion.package ? ", " + parsedVersion.package : '');
        }
        return rawVersion;
    }
    catch (_a) {
        return rawVersion;
    }
};
function roundWithFixed(value, fixedDigits) {
    var label = value.toFixed(fixedDigits);
    var result = fixedDigits <= 0 ? Math.round(value) : value;
    return { label: label, result: result };
}
// in milliseconds
export var WEEK = 604800000;
export var DAY = 86400000;
export var HOUR = 3600000;
export var MINUTE = 60000;
export var SECOND = 1000;
export function getDuration(seconds, fixedDigits, abbreviation) {
    if (fixedDigits === void 0) { fixedDigits = 0; }
    if (abbreviation === void 0) { abbreviation = false; }
    var value = Math.abs(seconds * 1000);
    if (value >= WEEK) {
        var _a = roundWithFixed(value / WEEK, fixedDigits), label_1 = _a.label, result = _a.result;
        return "" + label_1 + (abbreviation ? t('wk') : " " + tn('week', 'weeks', result));
    }
    if (value >= 172800000) {
        var _b = roundWithFixed(value / DAY, fixedDigits), label_2 = _b.label, result = _b.result;
        return "" + label_2 + (abbreviation ? t('d') : " " + tn('day', 'days', result));
    }
    if (value >= 7200000) {
        var _c = roundWithFixed(value / HOUR, fixedDigits), label_3 = _c.label, result = _c.result;
        return "" + label_3 + (abbreviation ? t('hr') : " " + tn('hour', 'hours', result));
    }
    if (value >= 120000) {
        var _d = roundWithFixed(value / MINUTE, fixedDigits), label_4 = _d.label, result = _d.result;
        return "" + label_4 + (abbreviation ? t('min') : " " + tn('minute', 'minutes', result));
    }
    if (value >= SECOND) {
        var _e = roundWithFixed(value / SECOND, fixedDigits), label_5 = _e.label, result = _e.result;
        return "" + label_5 + (abbreviation ? t('s') : " " + tn('second', 'seconds', result));
    }
    var label = roundWithFixed(value, fixedDigits).label;
    return label + t('ms');
}
export function getExactDuration(seconds, abbreviation) {
    if (abbreviation === void 0) { abbreviation = false; }
    var convertDuration = function (secs, abbr) {
        var value = round(Math.abs(secs * 1000));
        var divideBy = function (time) {
            return { quotient: Math.floor(value / time), remainder: value % time };
        };
        if (value >= WEEK) {
            var _a = divideBy(WEEK), quotient = _a.quotient, remainder = _a.remainder;
            return "" + quotient + (abbr ? t('wk') : " " + tn('week', 'weeks', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= DAY) {
            var _b = divideBy(DAY), quotient = _b.quotient, remainder = _b.remainder;
            return "" + quotient + (abbr ? t('d') : " " + tn('day', 'days', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= HOUR) {
            var _c = divideBy(HOUR), quotient = _c.quotient, remainder = _c.remainder;
            return "" + quotient + (abbr ? t('hr') : " " + tn('hour', 'hours', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= MINUTE) {
            var _d = divideBy(MINUTE), quotient = _d.quotient, remainder = _d.remainder;
            return "" + quotient + (abbr ? t('min') : " " + tn('minute', 'minutes', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= SECOND) {
            var _e = divideBy(SECOND), quotient = _e.quotient, remainder = _e.remainder;
            return "" + quotient + (abbr ? t('s') : " " + tn('second', 'seconds', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value === 0) {
            return '';
        }
        return "" + value + (abbr ? t('ms') : " " + tn('millisecond', 'milliseconds', value));
    };
    var result = convertDuration(seconds, abbreviation).trim();
    if (result.length) {
        return result;
    }
    return "0" + (abbreviation ? t('ms') : " " + t('milliseconds'));
}
export function formatFloat(number, places) {
    var multi = Math.pow(10, places);
    return parseInt((number * multi).toString(), 10) / multi;
}
/**
 * Format a value between 0 and 1 as a percentage
 */
export function formatPercentage(value, places) {
    if (places === void 0) { places = 2; }
    if (value === 0) {
        return '0%';
    }
    return (value * 100).toFixed(places) + '%';
}
var numberFormats = [
    [1000000000, 'b'],
    [1000000, 'm'],
    [1000, 'k'],
];
export function formatAbbreviatedNumber(number) {
    number = Number(number);
    var lookup;
    // eslint-disable-next-line no-cond-assign
    for (var i = 0; (lookup = numberFormats[i]); i++) {
        var _a = __read(lookup, 2), suffixNum = _a[0], suffix = _a[1];
        var shortValue = Math.floor(number / suffixNum);
        var fitsBound = number % suffixNum;
        if (shortValue <= 0) {
            continue;
        }
        return shortValue / 10 > 1 || !fitsBound
            ? "" + shortValue + suffix
            : "" + formatFloat(number / suffixNum, 1) + suffix;
    }
    return number.toLocaleString();
}
//# sourceMappingURL=formatters.jsx.map