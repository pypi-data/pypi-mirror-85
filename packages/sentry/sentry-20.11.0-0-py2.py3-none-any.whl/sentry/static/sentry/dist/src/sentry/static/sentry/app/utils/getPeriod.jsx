import { __read } from "tslib";
import moment from 'moment';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { getUtcDateString } from 'app/utils/dates';
export var getPeriod = function (_a, _b) {
    var period = _a.period, start = _a.start, end = _a.end;
    var shouldDoublePeriod = (_b === void 0 ? {} : _b).shouldDoublePeriod;
    if (!period && !start && !end) {
        period = DEFAULT_STATS_PERIOD;
    }
    // you can not specify both relative and absolute periods
    // relative period takes precedence
    if (period) {
        if (!shouldDoublePeriod) {
            return { statsPeriod: period };
        }
        var _c = __read(period.match(/([0-9]+)([mhdw])/), 3), periodNumber = _c[1], periodLength = _c[2];
        return { statsPeriod: "" + parseInt(periodNumber, 10) * 2 + periodLength };
    }
    if (!start || !end) {
        throw new Error('start and end required');
    }
    var formattedStart = getUtcDateString(start);
    var formattedEnd = getUtcDateString(end);
    if (shouldDoublePeriod) {
        // get duration of end - start and double
        var diff = moment(end).diff(moment(start));
        var previousPeriodStart = moment(start).subtract(diff);
        // This is not as accurate as having 2 start/end objs
        return {
            start: getUtcDateString(previousPeriodStart),
            end: formattedEnd,
        };
    }
    return {
        start: formattedStart,
        end: formattedEnd,
    };
};
//# sourceMappingURL=getPeriod.jsx.map