import { __assign, __rest } from "tslib";
import { getFormattedDate, getTimeFormat } from 'app/utils/dates';
import { truncationFormatter, useShortInterval } from '../utils';
export default function XAxis(_a) {
    var isGroupedByDate = _a.isGroupedByDate, useShortDate = _a.useShortDate, axisLabel = _a.axisLabel, axisTick = _a.axisTick, axisLine = _a.axisLine, theme = _a.theme, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc, props = __rest(_a, ["isGroupedByDate", "useShortDate", "axisLabel", "axisTick", "axisLine", "theme", "start", "end", "period", "utc"]);
    var axisLabelFormatter = function (value, index) {
        if (isGroupedByDate) {
            var timeFormat = getTimeFormat();
            var dateFormat = useShortDate ? 'MMM Do' : "MMM D " + timeFormat;
            var firstItem = index === 0;
            var format = useShortInterval({ start: start, end: end, period: period }) && !firstItem ? timeFormat : dateFormat;
            return getFormattedDate(value, format, { local: !utc });
        }
        else if (props.truncate) {
            return truncationFormatter(value, props.truncate);
        }
        else {
            return undefined;
        }
    };
    return __assign({ type: isGroupedByDate ? 'time' : 'category', boundaryGap: false, axisLine: __assign({ lineStyle: {
                color: theme.chartLabel,
            } }, (axisLine || {})), axisTick: __assign({ lineStyle: {
                color: theme.chartLabel,
            } }, (axisTick || {})), splitLine: {
            show: false,
        }, axisLabel: __assign({ color: theme.chartLabel, margin: 12, 
            // This was default with ChartZoom, we are making it default for all charts now
            // Otherwise the xAxis can look congested when there is always a min/max label
            showMaxLabel: false, showMinLabel: false, formatter: axisLabelFormatter }, (axisLabel || {})), axisPointer: {
            show: true,
            type: 'line',
            label: {
                show: false,
            },
            lineStyle: {
                width: 0.5,
            },
        } }, props);
}
//# sourceMappingURL=xAxis.jsx.map