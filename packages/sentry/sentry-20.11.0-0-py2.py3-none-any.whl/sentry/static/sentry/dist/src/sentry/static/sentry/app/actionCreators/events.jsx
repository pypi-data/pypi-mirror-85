import { __assign, __awaiter, __generator, __read } from "tslib";
import pick from 'lodash/pick';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { canIncludePreviousPeriod } from 'app/components/charts/utils';
import { getPeriod } from 'app/utils/getPeriod';
/**
 * Make requests to `events-stats` endpoint
 *
 * @param {Object} api API client instance
 * @param {Object} options Request parameters
 * @param {Object} options.organization Organization object
 * @param {Number[]} options.project List of project ids
 * @param {String[]} options.environment List of environments to query for
 * @param {String} options.period Time period to query for, in the format: <integer><units> where units are "d" or "h"
 * @param {String} options.interval Time interval to group results in, in the format: <integer><units> where units are "d", "h", "m", "s"
 * @param {Boolean} options.includePrevious Should request also return reqsults for previous period?
 * @param {Number} options.limit The number of rows to return
 * @param {String} options.query Search query
 */
export var doEventsRequest = function (api, _a) {
    var organization = _a.organization, project = _a.project, environment = _a.environment, period = _a.period, start = _a.start, end = _a.end, interval = _a.interval, includePrevious = _a.includePrevious, query = _a.query, yAxis = _a.yAxis, field = _a.field, topEvents = _a.topEvents, orderby = _a.orderby;
    var shouldDoublePeriod = canIncludePreviousPeriod(includePrevious, period);
    var urlQuery = Object.fromEntries(Object.entries({
        interval: interval,
        project: project,
        environment: environment,
        query: query,
        yAxis: yAxis,
        field: field,
        topEvents: topEvents,
        orderby: orderby,
    }).filter(function (_a) {
        var _b = __read(_a, 2), value = _b[1];
        return typeof value !== 'undefined';
    }));
    // Doubling period for absolute dates is not accurate unless starting and
    // ending times are the same (at least for daily intervals). This is
    // the tradeoff for now.
    var periodObj = getPeriod({ period: period, start: start, end: end }, { shouldDoublePeriod: shouldDoublePeriod });
    return api.requestPromise("/organizations/" + organization.slug + "/events-stats/", {
        query: __assign(__assign({}, urlQuery), periodObj),
    });
};
/**
 * Fetches tag facets for a query
 */
export function fetchTagFacets(api, orgSlug, query) {
    return __awaiter(this, void 0, void 0, function () {
        var urlParams, queryOption;
        return __generator(this, function (_a) {
            urlParams = pick(query, Object.values(URL_PARAM));
            queryOption = __assign(__assign({}, urlParams), { query: query.query });
            return [2 /*return*/, api.requestPromise("/organizations/" + orgSlug + "/events-facets/", {
                    query: queryOption,
                })];
        });
    });
}
/**
 * Fetches total count of events for a given query
 */
export function fetchTotalCount(api, orgSlug, query) {
    return __awaiter(this, void 0, void 0, function () {
        var urlParams, queryOption;
        return __generator(this, function (_a) {
            urlParams = pick(query, Object.values(URL_PARAM));
            queryOption = __assign(__assign({}, urlParams), { query: query.query });
            return [2 /*return*/, api
                    .requestPromise("/organizations/" + orgSlug + "/events-meta/", {
                    query: queryOption,
                })
                    .then(function (res) { return res.count; })];
        });
    });
}
//# sourceMappingURL=events.jsx.map