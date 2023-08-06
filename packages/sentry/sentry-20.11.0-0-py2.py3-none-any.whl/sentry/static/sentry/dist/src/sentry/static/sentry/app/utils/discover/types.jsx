var _a;
import { t } from 'app/locale';
export var TOP_N = 5;
export var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DEFAULT"] = "default";
    DisplayModes["PREVIOUS"] = "previous";
    DisplayModes["TOP5"] = "top5";
    DisplayModes["DAILY"] = "daily";
    DisplayModes["DAILYTOP5"] = "dailytop5";
})(DisplayModes || (DisplayModes = {}));
export var DISPLAY_MODE_OPTIONS = [
    { value: DisplayModes.DEFAULT, label: t('Total Period') },
    { value: DisplayModes.PREVIOUS, label: t('Previous Period') },
    { value: DisplayModes.TOP5, label: t('Top 5 Period') },
    { value: DisplayModes.DAILY, label: t('Total Daily') },
    { value: DisplayModes.DAILYTOP5, label: t('Top 5 Daily') },
];
/**
 * The chain of fallback display modes to try to use when one is disabled.
 *
 * Make sure that the chain always leads to a display mode that is enabled.
 * There is a fail safe to fall back to the default display mode, but it likely
 * won't be creating results you expect.
 */
export var DISPLAY_MODE_FALLBACK_OPTIONS = (_a = {},
    _a[DisplayModes.DEFAULT] = DisplayModes.DEFAULT,
    _a[DisplayModes.PREVIOUS] = DisplayModes.DEFAULT,
    _a[DisplayModes.TOP5] = DisplayModes.DEFAULT,
    _a[DisplayModes.DAILY] = DisplayModes.DEFAULT,
    _a[DisplayModes.DAILYTOP5] = DisplayModes.DAILY,
    _a);
// default list of yAxis options
export var CHART_AXIS_OPTIONS = [
    { label: 'count()', value: 'count()' },
    { label: 'count_unique(users)', value: 'count_unique(user)' },
];
//# sourceMappingURL=types.jsx.map