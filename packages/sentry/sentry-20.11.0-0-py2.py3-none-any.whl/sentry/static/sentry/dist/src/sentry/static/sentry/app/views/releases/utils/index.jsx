import round from 'lodash/round';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
import { ReleaseStatus } from 'app/types';
export var roundDuration = function (seconds) {
    return round(seconds, seconds > 60 ? 0 : 3);
};
export var getCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    return round(percent, percent > decimalThreshold ? decimalPlaces : 0);
};
export var displayCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    if (isNaN(percent)) {
        return '\u2015';
    }
    if (percent < 1 && percent > 0) {
        return "<1%";
    }
    var rounded = getCrashFreePercent(percent, decimalThreshold, decimalPlaces);
    return rounded + "%";
};
export var convertAdoptionToProgress = function (percent, numberOfProgressUnits) {
    if (numberOfProgressUnits === void 0) { numberOfProgressUnits = 10; }
    return Math.ceil((percent * numberOfProgressUnits) / 100);
};
export var getReleaseNewIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            query: stringifyQueryObject(new QueryResults(["firstRelease:" + version])),
        },
    };
};
export var isReleaseArchived = function (release) {
    return release.status === ReleaseStatus.Archived;
};
//# sourceMappingURL=index.jsx.map