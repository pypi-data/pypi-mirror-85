import moment from 'moment';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { t } from 'app/locale';
var DATE_TIME_FORMAT = 'YYYY-MM-DDTHH:mm:ss';
/**
 * Converts a relative stats period, e.g. `1h` to an object containing a start
 * and end date, with the end date as the current time and the start date as the
 * time that is the current time less the statsPeriod.
 *
 * @param statsPeriod Relative stats period
 * @param outputFormat Format of outputed start/end date
 * @return Object containing start and end date as YYYY-MM-DDTHH:mm:ss
 *
 */
export function parseStatsPeriod(statsPeriod, outputFormat) {
    if (outputFormat === void 0) { outputFormat = DATE_TIME_FORMAT; }
    var statsPeriodRegex = /^(\d+)([smhd]{1})$/;
    var result = statsPeriodRegex.exec(statsPeriod);
    if (result === null) {
        throw new Error('Invalid stats period');
    }
    var value = parseInt(result[1], 10);
    var unit = {
        d: 'days',
        h: 'hours',
        s: 'seconds',
        m: 'minutes',
    }[result[2]];
    var format = outputFormat === null ? undefined : outputFormat;
    return {
        start: moment().subtract(value, unit).format(format),
        end: moment().format(format),
    };
}
/**
 * Given a relative stats period, e.g. `1h`, return a pretty string if it
 * is a default stats period. Otherwise if it's a valid period (can be any number
 * followed by a single character s|m|h|d) display "Other" or "Invalid period" if invalid
 *
 * @param relative Relative stats period
 * @return either one of the default "Last x days" string, "Other" if period is valid on the backend, or "Invalid period" otherwise
 */
export function getRelativeSummary(relative) {
    var defaultRelativePeriodString = DEFAULT_RELATIVE_PERIODS[relative];
    if (!defaultRelativePeriodString) {
        try {
            parseStatsPeriod(relative);
            return t('Other');
        }
        catch (err) {
            return 'Invalid period';
        }
    }
    return defaultRelativePeriodString;
}
//# sourceMappingURL=utils.jsx.map