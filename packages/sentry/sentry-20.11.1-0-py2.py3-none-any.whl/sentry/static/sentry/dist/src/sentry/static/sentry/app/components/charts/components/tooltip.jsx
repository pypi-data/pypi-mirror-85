import { __assign, __rest } from "tslib";
import 'echarts/lib/component/tooltip';
import moment from 'moment';
import { getFormattedDate, getTimeFormat } from 'app/utils/dates';
import { truncationFormatter } from '../utils';
function defaultFormatAxisLabel(value, isTimestamp, utc, showTimeInTooltip, bucketSize) {
    if (!isTimestamp) {
        return value;
    }
    if (!bucketSize) {
        var format = ("MMM D, YYYY " + (showTimeInTooltip ? getTimeFormat() : '')).trim();
        return getFormattedDate(value, format, { local: !utc });
    }
    var now = moment();
    var bucketStart = moment(value);
    var bucketEnd = moment(value + bucketSize);
    var showYear = now.year() !== bucketStart.year() || now.year() !== bucketEnd.year();
    var showEndDate = bucketStart.date() !== bucketEnd.date();
    var formatStart = ("MMM D" + (showYear ? ', YYYY' : '') + " " + (showTimeInTooltip ? getTimeFormat() : '')).trim();
    var formatEnd = ("" + (showEndDate ? "MMM D" + (showYear ? ', YYYY' : '') + " " : '') + (showTimeInTooltip ? getTimeFormat() : '')).trim();
    return getFormattedDate(bucketStart, formatStart, {
        local: !utc,
    }) + " \u2014 " + getFormattedDate(bucketEnd, formatEnd, { local: !utc });
}
function defaultValueFormatter(value) {
    if (typeof value === 'number') {
        return value.toLocaleString();
    }
    return value;
}
function defaultNameFormatter(value) {
    return value;
}
function getSeriesValue(series, offset) {
    if (!series.data) {
        return undefined;
    }
    if (Array.isArray(series.data)) {
        return series.data[offset];
    }
    if (Array.isArray(series.data.value)) {
        return series.data.value[offset];
    }
    return undefined;
}
function getFormatter(_a) {
    var filter = _a.filter, isGroupedByDate = _a.isGroupedByDate, showTimeInTooltip = _a.showTimeInTooltip, truncate = _a.truncate, formatAxisLabel = _a.formatAxisLabel, utc = _a.utc, bucketSize = _a.bucketSize, _b = _a.valueFormatter, valueFormatter = _b === void 0 ? defaultValueFormatter : _b, _c = _a.nameFormatter, nameFormatter = _c === void 0 ? defaultNameFormatter : _c;
    var getFilter = function (seriesParam) {
        // Series do not necessarily have `data` defined, e.g. releases don't have `data`, but rather
        // has a series using strictly `markLine`s.
        // However, real series will have `data` as a tuple of (label, value) or be
        // an object with value/label keys.
        var value = getSeriesValue(seriesParam, 0);
        if (typeof filter === 'function') {
            return filter(value);
        }
        return true;
    };
    var formatter = function (seriesParamsOrParam) {
        // If this is a tooltip for the axis, it will include all series for that axis item.
        // In this case seriesParamsOrParam will be of type `Object[]`
        //
        // Otherwise, it will be an `Object`, and is a tooltip for a single item
        var axisFormatterOrDefault = formatAxisLabel || defaultFormatAxisLabel;
        // Special tooltip if component is a `markPoint`
        if (!Array.isArray(seriesParamsOrParam) &&
            // TODO(ts): The EChart types suggest that this can _only_ be `series`,
            //           but assuming this code is correct (which I have not
            //           verified) their types may be wrong.
            seriesParamsOrParam.componentType === 'markPoint') {
            var timestamp_1 = seriesParamsOrParam.data.coord[0];
            var label_1 = axisFormatterOrDefault(timestamp_1, !!isGroupedByDate, !!utc, !!showTimeInTooltip, bucketSize);
            // eCharts sets seriesName as null when `componentType` !== 'series'
            var truncatedName = truncationFormatter(seriesParamsOrParam.data.labelForValue, truncate);
            var formattedValue = valueFormatter(seriesParamsOrParam.data.coord[1], seriesParamsOrParam.name);
            return [
                '<div class="tooltip-series">',
                "<div>\n          <span class=\"tooltip-label\"><strong>" + seriesParamsOrParam.name + "</strong></span>\n          " + truncatedName + ": " + formattedValue + "\n        </div>",
                '</div>',
                "<div class=\"tooltip-date\">" + label_1 + "</div>",
                '</div>',
            ].join('');
        }
        var seriesParams = Array.isArray(seriesParamsOrParam)
            ? seriesParamsOrParam
            : [seriesParamsOrParam];
        // If axis, timestamp comes from axis, otherwise for a single item it is defined in the data attribute.
        // The data attribute is usually a list of [name, value] but can also be an object of {name, value} when
        // there is item specific formatting being used.
        var timestamp = Array.isArray(seriesParamsOrParam)
            ? seriesParams[0].axisValue
            : getSeriesValue(seriesParams[0], 0);
        var label = seriesParams.length &&
            axisFormatterOrDefault(timestamp, !!isGroupedByDate, !!utc, !!showTimeInTooltip, bucketSize);
        return [
            '<div class="tooltip-series">',
            seriesParams
                .filter(getFilter)
                .map(function (s) {
                var _a;
                var formattedLabel = nameFormatter(truncationFormatter((_a = s.seriesName) !== null && _a !== void 0 ? _a : '', truncate));
                var value = valueFormatter(getSeriesValue(s, 1), s.seriesName);
                return "<div><span class=\"tooltip-label\">" + s.marker + " <strong>" + formattedLabel + "</strong></span> " + value + "</div>";
            })
                .join(''),
            '</div>',
            "<div class=\"tooltip-date\">" + label + "</div>",
            "<div class=\"tooltip-arrow\"></div>",
        ].join('');
    };
    return formatter;
}
export default function Tooltip(_a) {
    if (_a === void 0) { _a = {}; }
    var filter = _a.filter, isGroupedByDate = _a.isGroupedByDate, showTimeInTooltip = _a.showTimeInTooltip, formatter = _a.formatter, truncate = _a.truncate, utc = _a.utc, bucketSize = _a.bucketSize, formatAxisLabel = _a.formatAxisLabel, valueFormatter = _a.valueFormatter, nameFormatter = _a.nameFormatter, props = __rest(_a, ["filter", "isGroupedByDate", "showTimeInTooltip", "formatter", "truncate", "utc", "bucketSize", "formatAxisLabel", "valueFormatter", "nameFormatter"]);
    formatter =
        formatter ||
            getFormatter({
                filter: filter,
                isGroupedByDate: isGroupedByDate,
                showTimeInTooltip: showTimeInTooltip,
                truncate: truncate,
                utc: utc,
                bucketSize: bucketSize,
                formatAxisLabel: formatAxisLabel,
                valueFormatter: valueFormatter,
                nameFormatter: nameFormatter,
            });
    return __assign({ show: true, trigger: 'item', backgroundColor: 'transparent', transitionDuration: 0, padding: 0, position: function (pos, _params, dom, _rec, _size) {
            // Center the tooltip slightly above the cursor.
            var tipWidth = dom.clientWidth;
            var tipHeight = dom.clientHeight;
            // Get the left offset of the tip container (the chart)
            // so that we can estimate overflows
            var chartLeft = dom.parentNode instanceof Element
                ? dom.parentNode.getBoundingClientRect().left
                : 0;
            // Determine the new left edge.
            var leftPos = Number(pos[0]) - tipWidth / 2;
            var arrowPosition = '50%';
            // And the right edge taking into account the chart left offset
            var rightEdge = chartLeft + Number(pos[0]) + tipWidth / 2;
            // If the tooltip would leave viewport on the right, pin it.
            // and adjust the arrow position.
            if (rightEdge >= window.innerWidth - 20) {
                leftPos -= rightEdge - window.innerWidth + 20;
                arrowPosition = Number(pos[0]) - leftPos + "px";
            }
            // If the tooltip would leave viewport on the left, pin it.
            if (leftPos + chartLeft - 20 <= 0) {
                leftPos = chartLeft * -1 + 20;
                arrowPosition = Number(pos[0]) - leftPos + "px";
            }
            // Reposition the arrow.
            var arrow = dom.querySelector('.tooltip-arrow');
            if (arrow) {
                arrow.style.left = arrowPosition;
            }
            return { left: leftPos, top: Number(pos[1]) - tipHeight - 20 };
        },
        formatter: formatter }, props);
}
//# sourceMappingURL=tooltip.jsx.map