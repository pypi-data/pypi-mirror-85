import { __assign, __awaiter, __extends, __generator, __read, __spread } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import omitBy from 'lodash/omitBy';
import isEqual from 'lodash/isEqual';
import meanBy from 'lodash/meanBy';
import mean from 'lodash/mean';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { percent, defined } from 'app/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { getExactDuration } from 'app/utils/formatters';
import { fetchTotalCount } from 'app/actionCreators/events';
import CHART_PALETTE from 'app/constants/chartPalette';
import { YAxis } from './chart/releaseChartControls';
import { getInterval, getReleaseEventView } from './chart/utils';
import { displayCrashFreePercent, getCrashFreePercent, roundDuration } from '../../utils';
var omitIgnoredProps = function (props) {
    return omitBy(props, function (_, key) {
        return ['api', 'version', 'orgId', 'projectSlug', 'location', 'children'].includes(key);
    });
};
var ReleaseStatsRequest = /** @class */ (function (_super) {
    __extends(ReleaseStatsRequest, _super);
    function ReleaseStatsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            data: null,
        };
        _this.unmounting = false;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, _a, yAxis, hasHealthData, hasDiscover, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        data = null;
                        _a = this.props, yAxis = _a.yAxis, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover;
                        if (!hasHealthData && !hasDiscover) {
                            return [2 /*return*/];
                        }
                        this.setState(function (state) { return ({
                            reloading: state.data !== null,
                            errored: false,
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 8, , 9]);
                        if (!(yAxis === YAxis.CRASH_FREE)) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.fetchRateData()];
                    case 2:
                        data = _c.sent();
                        return [3 /*break*/, 7];
                    case 3:
                        if (!(yAxis === YAxis.EVENTS)) return [3 /*break*/, 5];
                        return [4 /*yield*/, this.fetchEventData()];
                    case 4:
                        data = _c.sent();
                        return [3 /*break*/, 7];
                    case 5: return [4 /*yield*/, this.fetchCountData(yAxis === YAxis.SESSION_DURATION ? YAxis.SESSIONS : yAxis)];
                    case 6:
                        // session duration uses same endpoint as sessions
                        data = _c.sent();
                        _c.label = 7;
                    case 7: return [3 /*break*/, 9];
                    case 8:
                        _b = _c.sent();
                        addErrorMessage(t('Error loading chart data'));
                        this.setState({
                            errored: true,
                            data: null,
                        });
                        return [3 /*break*/, 9];
                    case 9:
                        if (this.unmounting) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            reloading: false,
                            data: data,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.fetchCountData = function (type) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, yAxis, response, transformedData;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, yAxis = _a.yAxis;
                        return [4 /*yield*/, api.requestPromise(this.statsPath, {
                                query: __assign(__assign({}, this.baseQueryParams), { type: type }),
                            })];
                    case 1:
                        response = _b.sent();
                        transformedData = yAxis === YAxis.SESSION_DURATION
                            ? this.transformSessionDurationData(response.stats)
                            : this.transformCountData(response.stats, yAxis, response.statTotals);
                        return [2 /*return*/, __assign(__assign({}, transformedData), { crashFreeTimeBreakdown: response.usersBreakdown })];
                }
            });
        }); };
        _this.fetchRateData = function () { return __awaiter(_this, void 0, void 0, function () {
            var api, _a, userResponse, sessionResponse, transformedData;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = this.props.api;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.statsPath, {
                                    query: __assign(__assign({}, this.baseQueryParams), { type: YAxis.USERS }),
                                }),
                                api.requestPromise(this.statsPath, {
                                    query: __assign(__assign({}, this.baseQueryParams), { type: YAxis.SESSIONS }),
                                }),
                            ])];
                    case 1:
                        _a = __read.apply(void 0, [_b.sent(), 2]), userResponse = _a[0], sessionResponse = _a[1];
                        transformedData = this.transformRateData(userResponse.stats, sessionResponse.stats);
                        return [2 /*return*/, __assign(__assign({}, transformedData), { crashFreeTimeBreakdown: userResponse.usersBreakdown })];
                }
            });
        }); };
        _this.fetchEventData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, orgId, location, selection, version, hasHealthData, crashFreeTimeBreakdown, userResponse, eventsCountResponse, breakdown, chartSummary;
            var _b;
            var _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, location = _a.location, selection = _a.selection, version = _a.version, hasHealthData = _a.hasHealthData;
                        crashFreeTimeBreakdown = (this.state.data || {}).crashFreeTimeBreakdown;
                        if (!(crashFreeTimeBreakdown || !hasHealthData)) return [3 /*break*/, 2];
                        return [4 /*yield*/, fetchTotalCount(api, orgId, getReleaseEventView(selection, version).getEventsAPIPayload(location))];
                    case 1:
                        eventsCountResponse = _d.sent();
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, Promise.all([
                            api.requestPromise(this.statsPath, {
                                query: __assign(__assign({}, this.baseQueryParams), { type: YAxis.USERS }),
                            }),
                            fetchTotalCount(api, orgId, getReleaseEventView(selection, version).getEventsAPIPayload(location)),
                        ])];
                    case 3:
                        _b = __read.apply(void 0, [_d.sent(), 2]), userResponse = _b[0], eventsCountResponse = _b[1];
                        _d.label = 4;
                    case 4:
                        breakdown = (_c = userResponse === null || userResponse === void 0 ? void 0 : userResponse.usersBreakdown) !== null && _c !== void 0 ? _c : crashFreeTimeBreakdown;
                        chartSummary = eventsCountResponse.toLocaleString();
                        return [2 /*return*/, { chartData: [], crashFreeTimeBreakdown: breakdown, chartSummary: chartSummary }];
                }
            });
        }); };
        return _this;
    }
    ReleaseStatsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (isEqual(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentWillUnmount = function () {
        this.unmounting = true;
    };
    Object.defineProperty(ReleaseStatsRequest.prototype, "statsPath", {
        get: function () {
            var _a = this.props, orgId = _a.orgId, projectSlug = _a.projectSlug, version = _a.version;
            return "/projects/" + orgId + "/" + projectSlug + "/releases/" + version + "/stats/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseStatsRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a = this.props, location = _a.location, selection = _a.selection;
            return __assign(__assign({}, getParams(pick(location.query, __spread(Object.values(URL_PARAM))))), { interval: getInterval(selection.datetime) });
        },
        enumerable: false,
        configurable: true
    });
    ReleaseStatsRequest.prototype.transformCountData = function (responseData, yAxis, responseTotals) {
        // here we can configure colors of the chart
        var chartData = {
            crashed: {
                seriesName: t('Crashed'),
                data: [],
                color: CHART_PALETTE[3][0],
                areaStyle: {
                    color: CHART_PALETTE[3][0],
                    opacity: 1,
                },
                lineStyle: {
                    opacity: 0,
                    width: 0.4,
                },
            },
            abnormal: {
                seriesName: t('Abnormal'),
                data: [],
                color: CHART_PALETTE[3][1],
                areaStyle: {
                    color: CHART_PALETTE[3][1],
                    opacity: 1,
                },
                lineStyle: {
                    opacity: 0,
                    width: 0.4,
                },
            },
            errored: {
                seriesName: t('Errored'),
                data: [],
                color: CHART_PALETTE[3][2],
                areaStyle: {
                    color: CHART_PALETTE[3][2],
                    opacity: 1,
                },
                lineStyle: {
                    opacity: 0,
                    width: 0.4,
                },
            },
            healthy: {
                seriesName: t('Healthy'),
                data: [],
                color: CHART_PALETTE[3][3],
                areaStyle: {
                    color: CHART_PALETTE[3][3],
                    opacity: 1,
                },
                lineStyle: {
                    opacity: 0,
                    width: 0.4,
                },
            },
        };
        responseData.forEach(function (entry) {
            var _a = __read(entry, 2), timeframe = _a[0], values = _a[1];
            var date = timeframe * 1000;
            var crashed = values[yAxis + "_crashed"];
            var abnormal = values[yAxis + "_abnormal"];
            var errored = values[yAxis + "_errored"];
            var healthy = values[yAxis] - crashed - abnormal - errored;
            chartData.crashed.data.push({ name: date, value: crashed });
            chartData.abnormal.data.push({ name: date, value: abnormal });
            chartData.errored.data.push({ name: date, value: errored });
            chartData.healthy.data.push({
                name: date,
                value: healthy >= 0 ? healthy : 0,
            });
        });
        return {
            chartData: Object.values(chartData),
            chartSummary: responseTotals[yAxis].toLocaleString(),
        };
    };
    ReleaseStatsRequest.prototype.transformRateData = function (responseUsersData, responseSessionsData) {
        var chartData = {
            users: {
                seriesName: t('Crash Free Users'),
                data: [],
                color: CHART_PALETTE[1][0],
            },
            sessions: {
                seriesName: t('Crash Free Sessions'),
                data: [],
                color: CHART_PALETTE[1][1],
            },
        };
        var calculateDatePercentage = function (responseData, subject) {
            var percentageData = responseData.map(function (entry) {
                var _a = __read(entry, 2), timeframe = _a[0], values = _a[1];
                var date = timeframe * 1000;
                var crashFreePercent = values[subject] !== 0
                    ? getCrashFreePercent(100 - percent(values[subject + "_crashed"], values[subject]))
                    : null;
                return { name: date, value: crashFreePercent };
            });
            var averagePercent = displayCrashFreePercent(meanBy(percentageData.filter(function (item) { return defined(item.value); }), 'value'));
            return { averagePercent: averagePercent, percentageData: percentageData };
        };
        var usersPercentages = calculateDatePercentage(responseUsersData, YAxis.USERS);
        chartData.users.data = usersPercentages.percentageData;
        var sessionsPercentages = calculateDatePercentage(responseSessionsData, YAxis.SESSIONS);
        chartData.sessions.data = sessionsPercentages.percentageData;
        var summary = tct('[usersPercent] users, [sessionsPercent] sessions', {
            usersPercent: usersPercentages.averagePercent,
            sessionsPercent: sessionsPercentages.averagePercent,
        });
        return { chartData: Object.values(chartData), chartSummary: summary };
    };
    ReleaseStatsRequest.prototype.transformSessionDurationData = function (responseData) {
        // here we can configure colors of the chart
        var chartData = {
            seriesName: t('Session Duration'),
            data: [],
            lineStyle: {
                opacity: 0,
            },
        };
        var sessionDurationAverage = mean(responseData
            .map(function (_a) {
            var _b = __read(_a, 2), timeframe = _b[0], values = _b[1];
            chartData.data.push({
                name: timeframe * 1000,
                value: roundDuration(values.duration_p50),
            });
            return values.duration_p50;
        })
            .filter(function (duration) { return defined(duration); })) || 0;
        var summary = getExactDuration(roundDuration(sessionDurationAverage));
        return { chartData: [chartData], chartSummary: summary };
    };
    ReleaseStatsRequest.prototype.render = function () {
        var _a, _b, _c;
        var children = this.props.children;
        var _d = this.state, data = _d.data, reloading = _d.reloading, errored = _d.errored;
        var loading = data === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            chartData: (_a = data === null || data === void 0 ? void 0 : data.chartData) !== null && _a !== void 0 ? _a : [],
            chartSummary: (_b = data === null || data === void 0 ? void 0 : data.chartSummary) !== null && _b !== void 0 ? _b : '',
            crashFreeTimeBreakdown: (_c = data === null || data === void 0 ? void 0 : data.crashFreeTimeBreakdown) !== null && _c !== void 0 ? _c : [],
        });
    };
    return ReleaseStatsRequest;
}(React.Component));
export default ReleaseStatsRequest;
//# sourceMappingURL=releaseStatsRequest.jsx.map