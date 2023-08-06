import { __assign, __awaiter, __extends, __generator, __read, __rest } from "tslib";
import isEqual from 'lodash/isEqual';
import omitBy from 'lodash/omitBy';
import PropTypes from 'prop-types';
import React from 'react';
import LoadingPanel from 'app/components/charts/loadingPanel';
import { doEventsRequest } from 'app/actionCreators/events';
import { canIncludePreviousPeriod } from 'app/components/charts/utils';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
var propNamesToIgnore = ['api', 'children', 'organization', 'loading'];
var omitIgnoredProps = function (props) {
    return omitBy(props, function (_value, key) { return propNamesToIgnore.includes(key); });
};
function isMultiSeriesStats(data) {
    return data !== null && data.data === undefined && data.totals === undefined;
}
var EventsRequest = /** @class */ (function (_super) {
    __extends(EventsRequest, _super);
    function EventsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: !!_this.props.loading,
            errored: false,
            timeseriesData: null,
        };
        _this.unmounting = false;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, confirmedQuery, props, timeseriesData, resp_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, confirmedQuery = _a.confirmedQuery, props = __rest(_a, ["api", "confirmedQuery"]);
                        timeseriesData = null;
                        if (confirmedQuery === false) {
                            return [2 /*return*/];
                        }
                        this.setState(function (state) { return ({
                            reloading: state.timeseriesData !== null,
                            errored: false,
                        }); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        api.clear();
                        return [4 /*yield*/, doEventsRequest(api, props)];
                    case 2:
                        timeseriesData = _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        resp_1 = _b.sent();
                        if (resp_1 && resp_1.responseJSON && resp_1.responseJSON.detail) {
                            addErrorMessage(resp_1.responseJSON.detail);
                        }
                        else {
                            addErrorMessage(t('Error loading chart data'));
                        }
                        this.setState({
                            errored: true,
                        });
                        return [3 /*break*/, 4];
                    case 4:
                        if (this.unmounting) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            reloading: false,
                            timeseriesData: timeseriesData,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * Retrieves data set for the current period (since data can potentially
         * contain previous period's data), as well as the previous period if
         * possible.
         *
         * Returns `null` if data does not exist
         */
        _this.getData = function (data) {
            var _a = _this.props, period = _a.period, includePrevious = _a.includePrevious;
            var hasPreviousPeriod = canIncludePreviousPeriod(includePrevious, period);
            // Take the floor just in case, but data should always be divisible by 2
            var dataMiddleIndex = Math.floor(data.length / 2);
            return {
                current: hasPreviousPeriod ? data.slice(dataMiddleIndex) : data,
                previous: hasPreviousPeriod ? data.slice(0, dataMiddleIndex) : null,
            };
        };
        return _this;
    }
    EventsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (isEqual(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    EventsRequest.prototype.componentWillUnmount = function () {
        this.unmounting = true;
    };
    // This aggregates all values per `timestamp`
    EventsRequest.prototype.calculateTotalsPerTimestamp = function (data, getName) {
        if (getName === void 0) { getName = function (timestamp) { return timestamp * 1000; }; }
        return data.map(function (_a, i) {
            var _b = __read(_a, 2), timestamp = _b[0], countArray = _b[1];
            return ({
                name: getName(timestamp, countArray, i),
                value: countArray.reduce(function (acc, _a) {
                    var count = _a.count;
                    return acc + count;
                }, 0),
            });
        });
    };
    /**
     * Get previous period data, but transform timestamps so that data fits unto
     * the current period's data axis
     */
    EventsRequest.prototype.transformPreviousPeriodData = function (current, previous) {
        var _a;
        // Need the current period data array so we can take the timestamp
        // so we can be sure the data lines up
        if (!previous) {
            return null;
        }
        return {
            seriesName: (_a = this.props.previousSeriesName) !== null && _a !== void 0 ? _a : 'Previous',
            data: this.calculateTotalsPerTimestamp(previous, function (_timestamp, _countArray, i) { return current[i][0] * 1000; }),
        };
    };
    /**
     * Aggregate all counts for each time stamp
     */
    EventsRequest.prototype.transformAggregatedTimeseries = function (data, seriesName) {
        if (seriesName === void 0) { seriesName = ''; }
        return {
            seriesName: seriesName,
            data: this.calculateTotalsPerTimestamp(data),
        };
    };
    /**
     * Transforms query response into timeseries data to be used in a chart
     */
    EventsRequest.prototype.transformTimeseriesData = function (data, seriesName) {
        return [
            {
                seriesName: seriesName || 'Current',
                data: data.map(function (_a) {
                    var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                    return ({
                        name: timestamp * 1000,
                        value: countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    });
                }),
            },
        ];
    };
    EventsRequest.prototype.processData = function (response) {
        if (!response) {
            return {};
        }
        var data = response.data, totals = response.totals;
        var _a = this.props, includeTransformedData = _a.includeTransformedData, includeTimeAggregation = _a.includeTimeAggregation, timeAggregationSeriesName = _a.timeAggregationSeriesName;
        var _b = this.getData(data), current = _b.current, previous = _b.previous;
        var transformedData = includeTransformedData
            ? this.transformTimeseriesData(current, this.props.currentSeriesName)
            : [];
        var previousData = includeTransformedData
            ? this.transformPreviousPeriodData(current, previous)
            : null;
        var timeAggregatedData = includeTimeAggregation
            ? this.transformAggregatedTimeseries(current, timeAggregationSeriesName || '')
            : {};
        return {
            data: transformedData,
            allData: data,
            originalData: current,
            totals: totals,
            originalPreviousData: previous,
            previousData: previousData,
            timeAggregatedData: timeAggregatedData,
        };
    };
    EventsRequest.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, showLoading = _a.showLoading, props = __rest(_a, ["children", "showLoading"]);
        var _b = this.state, timeseriesData = _b.timeseriesData, reloading = _b.reloading, errored = _b.errored;
        // Is "loading" if data is null
        var loading = this.props.loading || timeseriesData === null;
        if (showLoading && loading) {
            return <LoadingPanel data-test-id="events-request-loading"/>;
        }
        if (isMultiSeriesStats(timeseriesData)) {
            // Convert multi-series results into chartable series. Multi series results
            // are created when multiple yAxis are used or a topEvents request is made.
            // Convert the timeseries data into a multi-series result set.
            // As the server will have replied with a map like:
            // {[titleString: string]: EventsStats}
            var results = Object.keys(timeseriesData)
                .map(function (seriesName) {
                var seriesData = timeseriesData[seriesName];
                var transformed = _this.transformTimeseriesData(seriesData.data, seriesName)[0];
                return [seriesData.order || 0, transformed];
            })
                .sort(function (a, b) { return a[0] - b[0]; })
                .map(function (item) { return item[1]; });
            return children(__assign({ loading: loading,
                reloading: reloading,
                errored: errored,
                results: results }, props));
        }
        var _c = this.processData(timeseriesData), transformedTimeseriesData = _c.data, allTimeseriesData = _c.allData, originalTimeseriesData = _c.originalData, timeseriesTotals = _c.totals, originalPreviousTimeseriesData = _c.originalPreviousData, previousTimeseriesData = _c.previousData, timeAggregatedData = _c.timeAggregatedData;
        return children(__assign({ loading: loading,
            reloading: reloading,
            errored: errored, 
            // timeseries data
            timeseriesData: transformedTimeseriesData, allTimeseriesData: allTimeseriesData,
            originalTimeseriesData: originalTimeseriesData,
            timeseriesTotals: timeseriesTotals,
            originalPreviousTimeseriesData: originalPreviousTimeseriesData,
            previousTimeseriesData: previousTimeseriesData,
            timeAggregatedData: timeAggregatedData }, props));
    };
    EventsRequest.propTypes = {
        api: PropTypes.object.isRequired,
        organization: SentryTypes.Organization.isRequired,
        project: PropTypes.arrayOf(PropTypes.number),
        environment: PropTypes.arrayOf(PropTypes.string),
        period: PropTypes.string,
        start: PropTypes.instanceOf(Date),
        end: PropTypes.instanceOf(Date),
        interval: PropTypes.string,
        includePrevious: PropTypes.bool,
        limit: PropTypes.number,
        query: PropTypes.string,
        includeTransformedData: PropTypes.bool,
        /**
         * Include a dataset transform that will aggregate count values for each
         * timestamp. Be sure to supply a name to `timeAggregationSeriesName`
         */
        includeTimeAggregation: PropTypes.bool,
        /**
         * Name of series of aggregated timeseries
         */
        timeAggregationSeriesName: PropTypes.string,
        loading: PropTypes.bool,
        errored: PropTypes.bool,
        showLoading: PropTypes.bool,
        currentSeriesName: PropTypes.string,
        yAxis: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
        field: PropTypes.arrayOf(PropTypes.string),
        topEvents: PropTypes.number,
        orderby: PropTypes.string,
        confirmedQuery: PropTypes.bool,
    };
    EventsRequest.defaultProps = {
        period: undefined,
        start: null,
        end: null,
        interval: '1d',
        limit: 15,
        query: '',
        includePrevious: true,
        includeTransformedData: true,
    };
    return EventsRequest;
}(React.PureComponent));
export default EventsRequest;
//# sourceMappingURL=eventsRequest.jsx.map