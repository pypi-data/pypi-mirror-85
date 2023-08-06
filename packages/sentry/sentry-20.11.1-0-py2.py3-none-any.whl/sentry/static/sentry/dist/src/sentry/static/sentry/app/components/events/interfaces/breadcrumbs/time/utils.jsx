import moment from 'moment';
import { use24Hours } from 'app/utils/dates';
import { defined } from 'app/utils';
import { t } from 'app/locale';
import { getDuration } from 'app/utils/formatters';
var timeFormat = 'HH:mm:ss';
var timeDateFormat = "ll " + timeFormat;
var getRelativeTime = function (parsedTime, parsedTimeToCompareWith, displayRelativeTime) {
    // ll is necessary here, otherwise moment(x).from will throw an error
    var formattedTime = moment(parsedTime.format(timeDateFormat));
    var formattedTimeToCompareWith = parsedTimeToCompareWith.format(timeDateFormat);
    var timeDiff = Math.abs(formattedTime.diff(formattedTimeToCompareWith));
    var shortRelativeTime = getDuration(Math.round(timeDiff / 1000), 0, true).replace(/\s/g, '');
    if (timeDiff !== 0) {
        return displayRelativeTime
            ? "-" + shortRelativeTime
            : t('%s before', shortRelativeTime);
    }
    return "\u00A0" + shortRelativeTime;
};
var getAbsoluteTimeFormat = function (format) {
    if (use24Hours()) {
        return format;
    }
    return format + " A";
};
var getFormattedTimestamp = function (timestamp, relativeTimestamp, displayRelativeTime) {
    var parsedTimestamp = moment(timestamp);
    var date = parsedTimestamp.format('ll');
    var displayMilliSeconds = defined(parsedTimestamp.milliseconds());
    var relativeTime = getRelativeTime(parsedTimestamp, moment(relativeTimestamp), displayRelativeTime);
    if (!displayRelativeTime) {
        return {
            date: date + " " + parsedTimestamp.format(getAbsoluteTimeFormat('HH:mm')),
            time: relativeTime,
            displayTime: parsedTimestamp.format(timeFormat),
        };
    }
    return {
        date: date,
        time: parsedTimestamp.format(getAbsoluteTimeFormat(displayMilliSeconds ? timeFormat + ".SSS" : timeFormat)),
        displayTime: relativeTime,
    };
};
export { getFormattedTimestamp };
//# sourceMappingURL=utils.jsx.map