var _a;
import { __assign, __read, __spread } from "tslib";
import { t } from 'app/locale';
import { WebVital, measurementType } from 'app/utils/discover/fields';
import theme from 'app/utils/theme';
export var NUM_BUCKETS = 100;
export var PERCENTILE = 0.75;
export var WEB_VITAL_DETAILS = (_a = {},
    _a[WebVital.FP] = {
        slug: 'fp',
        name: t('First Paint'),
        acronym: 'FP',
        description: t('Render time of the first pixel loaded in the viewport (may overlap with FCP).'),
        failureThreshold: 3000,
        type: measurementType(WebVital.FP),
    },
    _a[WebVital.FCP] = {
        slug: 'fcp',
        name: t('First Contentful Paint'),
        acronym: 'FCP',
        description: t('Render time of the first image, text or other DOM node in the viewport.'),
        failureThreshold: 3000,
        type: measurementType(WebVital.FCP),
    },
    _a[WebVital.LCP] = {
        slug: 'lcp',
        name: t('Largest Contentful Paint'),
        acronym: 'LCP',
        description: t('Render time of the largest image, text or other DOM node in the viewport.'),
        failureThreshold: 4000,
        type: measurementType(WebVital.LCP),
    },
    _a[WebVital.FID] = {
        slug: 'fid',
        name: t('First Input Delay'),
        acronym: 'FID',
        description: t('Response time of the browser to a user interaction (clicking, tapping, etc).'),
        failureThreshold: 300,
        type: measurementType(WebVital.FID),
    },
    _a[WebVital.CLS] = {
        slug: 'cls',
        name: t('Cumulative Layout Shift'),
        acronym: 'CLS',
        description: t('Sum of layout shift scores that measure the visual stability of the page.'),
        failureThreshold: 0.25,
        type: measurementType(WebVital.CLS),
    },
    _a[WebVital.TTFB] = {
        slug: 'ttfb',
        name: t('Time to First Byte'),
        acronym: 'TTFB',
        description: t("The time that it takes for a user's browser to receive the first byte of page content."),
        failureThreshold: 600,
        type: measurementType(WebVital.TTFB),
    },
    _a[WebVital.RequestTime] = {
        slug: 'ttfb.requesttime',
        name: t('Request Time'),
        acronym: 'RT',
        description: t('Captures the time spent making the request and receiving the first byte of the response.'),
        failureThreshold: 600,
        type: measurementType(WebVital.RequestTime),
    },
    _a);
// translate known short form names into their long forms
export var LONG_WEB_VITAL_NAMES = Object.fromEntries(Object.values(WEB_VITAL_DETAILS).map(function (value) {
    return [value.slug, value.name];
}));
export var WEB_VITAL_ACRONYMS = Object.fromEntries(Object.values(WEB_VITAL_DETAILS).map(function (value) {
    return [value.slug, value.acronym];
}));
export var FILTER_OPTIONS = [
    { label: t('Exclude Outliers'), value: 'exclude_outliers' },
    { label: t('View All'), value: 'all' },
];
/**
 * This defines the grouping for histograms. Histograms that are in the same group
 * will be queried together on initial load for alignment. However, the zoom controls
 * are defined for each measurement independently.
 */
var _VITAL_GROUPS = [
    {
        vitals: [WebVital.FP, WebVital.FCP, WebVital.LCP],
        min: 0,
    },
    {
        vitals: [WebVital.FID],
        min: 0,
        precision: 2,
    },
    {
        vitals: [WebVital.CLS],
        min: 0,
        precision: 2,
    },
];
var _COLORS = __spread(theme.charts.getColorPalette(_VITAL_GROUPS.reduce(function (count, _a) {
    var vitals = _a.vitals;
    return count + vitals.length;
}, 0) - 1)).reverse();
export var VITAL_GROUPS = _VITAL_GROUPS.map(function (group) { return (__assign(__assign({}, group), { colors: _COLORS.splice(0, group.vitals.length) })); });
export var ZOOM_KEYS = _VITAL_GROUPS.reduce(function (keys, _a) {
    var vitals = _a.vitals;
    vitals.forEach(function (vital) {
        var vitalSlug = WEB_VITAL_DETAILS[vital].slug;
        keys.push(vitalSlug + "Start");
        keys.push(vitalSlug + "End");
    });
    return keys;
}, []);
//# sourceMappingURL=constants.jsx.map