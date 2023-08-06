import { WEEK, DAY, HOUR, MINUTE, SECOND, getDuration, formatAbbreviatedNumber, formatPercentage, } from 'app/utils/formatters';
import { t } from 'app/locale';
import { aggregateOutputType } from 'app/utils/discover/fields';
/**
 * Formatter for chart tooltips that handle a variety of discover result values
 */
export function tooltipFormatter(value, seriesName) {
    switch (aggregateOutputType(seriesName)) {
        case 'integer':
        case 'number':
            return value.toLocaleString();
        case 'percentage':
            return formatPercentage(value, 2);
        case 'duration':
            return getDuration(value / 1000, 2, true);
        default:
            return value.toString();
    }
}
/**
 * Formatter for chart axis labels that handle a variety of discover result values
 * This function is *very similar* to tooltipFormatter but outputs data with less precision.
 */
export function axisLabelFormatter(value, seriesName, abbreviation) {
    if (abbreviation === void 0) { abbreviation = false; }
    switch (aggregateOutputType(seriesName)) {
        case 'integer':
        case 'number':
            return abbreviation ? formatAbbreviatedNumber(value) : value.toLocaleString();
        case 'percentage':
            return formatPercentage(value, 0);
        case 'duration':
            return axisDuration(value);
        default:
            return value.toString();
    }
}
/**
 * Specialized duration formatting for axis labels.
 * In that context we are ok sacrificing accuracy for more
 * consistent sizing.
 *
 * @param value Number of milliseconds to format.
 */
export function axisDuration(value) {
    if (value === 0) {
        return '0';
    }
    if (value >= WEEK) {
        var label_1 = (value / WEEK).toFixed(0);
        return t('%swk', label_1);
    }
    if (value >= DAY) {
        var label_2 = (value / DAY).toFixed(0);
        return t('%sd', label_2);
    }
    if (value >= HOUR) {
        var label_3 = (value / HOUR).toFixed(0);
        return t('%shr', label_3);
    }
    if (value >= MINUTE) {
        var label_4 = (value / MINUTE).toFixed(0);
        return t('%smin', label_4);
    }
    if (value >= SECOND) {
        var label_5 = (value / SECOND).toFixed(0);
        return t('%ss', label_5);
    }
    var label = (value / SECOND).toFixed(1);
    return t('%ss', label);
}
//# sourceMappingURL=charts.jsx.map