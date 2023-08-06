import { __assign, __read, __rest } from "tslib";
import moment from 'moment';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { defined } from 'app/utils';
var STATS_PERIOD_PATTERN = '^(\\d+)([hdmsw])?$';
export function parseStatsPeriod(input) {
    var result = input.match(STATS_PERIOD_PATTERN);
    if (!result) {
        return undefined;
    }
    var period = result[1];
    var periodLength = result[2];
    if (!periodLength) {
        // default to seconds.
        // this behaviour is based on src/sentry/utils/dates.py
        periodLength = 's';
    }
    return {
        period: period,
        periodLength: periodLength,
    };
}
function coerceStatsPeriod(input) {
    var result = parseStatsPeriod(input);
    if (!result) {
        return undefined;
    }
    var period = result.period, periodLength = result.periodLength;
    return "" + period + periodLength;
}
function getStatsPeriodValue(maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        var result = maybe.find(coerceStatsPeriod);
        if (!result) {
            return undefined;
        }
        return coerceStatsPeriod(result);
    }
    if (typeof maybe === 'string') {
        return coerceStatsPeriod(maybe);
    }
    return undefined;
}
// We normalize potential datetime strings into the form that would be valid
// if it were to be parsed by datetime.strptime using the format %Y-%m-%dT%H:%M:%S.%f
// This format was transformed to the form that moment.js understands using
// https://gist.github.com/asafge/0b13c5066d06ae9a4446
var normalizeDateTimeString = function (input) {
    if (!input) {
        return undefined;
    }
    var parsed = moment.utc(input);
    if (!parsed.isValid()) {
        return undefined;
    }
    return parsed.format('YYYY-MM-DDTHH:mm:ss.SSS');
};
var getDateTimeString = function (maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        var result = maybe.find(function (needle) { return moment.utc(needle).isValid(); });
        return normalizeDateTimeString(result);
    }
    return normalizeDateTimeString(maybe);
};
var parseUtcValue = function (utc) {
    if (defined(utc)) {
        return utc === true || utc === 'true' ? 'true' : 'false';
    }
    return undefined;
};
var getUtcValue = function (maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        return maybe.find(function (needle) { return !!parseUtcValue(needle); });
    }
    return parseUtcValue(maybe);
};
export function getParams(params, _a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.allowEmptyPeriod, allowEmptyPeriod = _c === void 0 ? false : _c, _d = _b.allowAbsoluteDatetime, allowAbsoluteDatetime = _d === void 0 ? true : _d;
    var start = params.start, end = params.end, period = params.period, statsPeriod = params.statsPeriod, utc = params.utc, otherParams = __rest(params, ["start", "end", "period", "statsPeriod", "utc"]);
    // `statsPeriod` takes precedence for now
    var coercedPeriod = getStatsPeriodValue(statsPeriod) || getStatsPeriodValue(period);
    var dateTimeStart = allowAbsoluteDatetime ? getDateTimeString(start) : null;
    var dateTimeEnd = allowAbsoluteDatetime ? getDateTimeString(end) : null;
    if (!(dateTimeStart && dateTimeEnd)) {
        if (!coercedPeriod && !allowEmptyPeriod) {
            coercedPeriod = DEFAULT_STATS_PERIOD;
        }
    }
    return Object.fromEntries(Object.entries(__assign({ statsPeriod: coercedPeriod, start: coercedPeriod ? null : dateTimeStart, end: coercedPeriod ? null : dateTimeEnd, 
        // coerce utc into a string (it can be both: a string representation from router,
        // or a boolean from time range picker)
        utc: getUtcValue(utc) }, otherParams))
        // Filter null values
        .filter(function (_a) {
        var _b = __read(_a, 2), _key = _b[0], value = _b[1];
        return defined(value);
    }));
}
//# sourceMappingURL=getParams.jsx.map