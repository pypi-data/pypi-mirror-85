var _a, _b;
import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread, __values } from "tslib";
import React from 'react';
import maxBy from 'lodash/maxBy';
import chunk from 'lodash/chunk';
import styled from '@emotion/styled';
import { fetchTotalCount } from 'app/actionCreators/events';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { t } from 'app/locale';
import { Panel, PanelBody } from 'app/components/panels';
import Feature from 'app/components/acl/feature';
import EventsRequest from 'app/components/charts/eventsRequest';
import LoadingMask from 'app/components/loadingMask';
import Placeholder from 'app/components/placeholder';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { TimeWindow, TimePeriod } from '../../types';
import ThresholdsChart from './thresholdsChart';
var TIME_PERIOD_MAP = (_a = {},
    _a[TimePeriod.SIX_HOURS] = t('Last 6 hours'),
    _a[TimePeriod.ONE_DAY] = t('Last 24 hours'),
    _a[TimePeriod.THREE_DAYS] = t('Last 3 days'),
    _a[TimePeriod.SEVEN_DAYS] = t('Last 7 days'),
    _a[TimePeriod.FOURTEEN_DAYS] = t('Last 14 days'),
    _a[TimePeriod.THIRTY_DAYS] = t('Last 30 days'),
    _a);
/**
 * If TimeWindow is small we want to limit the stats period
 * If the time window is one day we want to use a larger stats period
 */
var AVAILABLE_TIME_PERIODS = (_b = {},
    _b[TimeWindow.ONE_MINUTE] = [
        TimePeriod.SIX_HOURS,
        TimePeriod.ONE_DAY,
        TimePeriod.THREE_DAYS,
        TimePeriod.SEVEN_DAYS,
    ],
    _b[TimeWindow.FIVE_MINUTES] = [
        TimePeriod.ONE_DAY,
        TimePeriod.THREE_DAYS,
        TimePeriod.SEVEN_DAYS,
        TimePeriod.FOURTEEN_DAYS,
        TimePeriod.THIRTY_DAYS,
    ],
    _b[TimeWindow.TEN_MINUTES] = [
        TimePeriod.ONE_DAY,
        TimePeriod.THREE_DAYS,
        TimePeriod.SEVEN_DAYS,
        TimePeriod.FOURTEEN_DAYS,
        TimePeriod.THIRTY_DAYS,
    ],
    _b[TimeWindow.FIFTEEN_MINUTES] = [
        TimePeriod.THREE_DAYS,
        TimePeriod.SEVEN_DAYS,
        TimePeriod.FOURTEEN_DAYS,
        TimePeriod.THIRTY_DAYS,
    ],
    _b[TimeWindow.THIRTY_MINUTES] = [
        TimePeriod.SEVEN_DAYS,
        TimePeriod.FOURTEEN_DAYS,
        TimePeriod.THIRTY_DAYS,
    ],
    _b[TimeWindow.ONE_HOUR] = [TimePeriod.FOURTEEN_DAYS, TimePeriod.THIRTY_DAYS],
    _b[TimeWindow.TWO_HOURS] = [TimePeriod.THIRTY_DAYS],
    _b[TimeWindow.FOUR_HOURS] = [TimePeriod.THIRTY_DAYS],
    _b[TimeWindow.ONE_DAY] = [TimePeriod.THIRTY_DAYS],
    _b);
var AGGREGATE_FUNCTIONS = {
    avg: function (seriesChunk) {
        return AGGREGATE_FUNCTIONS.sum(seriesChunk) / seriesChunk.length;
    },
    sum: function (seriesChunk) {
        return seriesChunk.reduce(function (acc, series) { return acc + series.value; }, 0);
    },
    max: function (seriesChunk) {
        return Math.max.apply(Math, __spread(seriesChunk.map(function (series) { return series.value; })));
    },
    min: function (seriesChunk) {
        return Math.min.apply(Math, __spread(seriesChunk.map(function (series) { return series.value; })));
    },
};
/**
 * Determines the number of datapoints to roll up
 */
var getBucketSize = function (timeWindow, dataPoints) {
    var e_1, _a;
    var MAX_DPS = 720;
    try {
        for (var _b = __values([5, 10, 15, 30, 60, 120, 240]), _c = _b.next(); !_c.done; _c = _b.next()) {
            var bucketSize = _c.value;
            var chunkSize = bucketSize / timeWindow;
            if (dataPoints / chunkSize <= MAX_DPS) {
                return bucketSize / timeWindow;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return 2;
};
/**
 * This is a chart to be used in Metric Alert rules that fetches events based on
 * query, timewindow, and aggregations.
 */
var TriggersChart = /** @class */ (function (_super) {
    __extends(TriggersChart, _super);
    function TriggersChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            statsPeriod: TimePeriod.ONE_DAY,
            totalEvents: null,
        };
        _this.handleStatsPeriodChange = function (statsPeriod) {
            _this.setState({ statsPeriod: statsPeriod.value });
        };
        _this.getStatsPeriod = function () {
            var statsPeriod = _this.state.statsPeriod;
            var timeWindow = _this.props.timeWindow;
            var statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
            var period = statsPeriodOptions.includes(statsPeriod)
                ? statsPeriod
                : statsPeriodOptions[0];
            return period;
        };
        return _this;
    }
    TriggersChart.prototype.componentDidMount = function () {
        this.fetchTotalCount();
    };
    TriggersChart.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, query = _a.query, environment = _a.environment;
        var statsPeriod = this.state.statsPeriod;
        if (prevProps.environment !== environment ||
            prevProps.query !== query ||
            prevState.statsPeriod !== statsPeriod) {
            this.fetchTotalCount();
        }
    };
    TriggersChart.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, environment, projects, query, statsPeriod, totalEvents, e_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, environment = _a.environment, projects = _a.projects, query = _a.query;
                        statsPeriod = this.getStatsPeriod();
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, {
                                field: [],
                                project: projects.map(function (_a) {
                                    var id = _a.id;
                                    return id;
                                }),
                                query: query,
                                statsPeriod: statsPeriod,
                                environment: environment ? [environment] : [],
                            })];
                    case 2:
                        totalEvents = _b.sent();
                        this.setState({ totalEvents: totalEvents });
                        return [3 /*break*/, 4];
                    case 3:
                        e_2 = _b.sent();
                        this.setState({ totalEvents: null });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    TriggersChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, organization = _a.organization, projects = _a.projects, timeWindow = _a.timeWindow, query = _a.query, aggregate = _a.aggregate, triggers = _a.triggers, resolveThreshold = _a.resolveThreshold, thresholdType = _a.thresholdType, environment = _a.environment;
        var _b = this.state, statsPeriod = _b.statsPeriod, totalEvents = _b.totalEvents;
        var statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
        var period = this.getStatsPeriod();
        return (<Feature features={['metric-alert-builder-aggregate']} organization={organization}>
        {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<EventsRequest api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects.map(function (_a) {
                var id = _a.id;
                return Number(id);
            })} interval={timeWindow + "m"} period={period} yAxis={aggregate} includePrevious={false} currentSeriesName={aggregate}>
              {function (_a) {
                var _b;
                var loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData;
                var maxValue;
                var timeseriesLength;
                if (((_b = timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0]) === null || _b === void 0 ? void 0 : _b.data) !== undefined) {
                    maxValue = maxBy(timeseriesData[0].data, function (_a) {
                        var value = _a.value;
                        return value;
                    });
                    timeseriesLength = timeseriesData[0].data.length;
                    if (hasFeature && timeseriesLength > 600) {
                        var avgData_1 = [];
                        var minData_1 = [];
                        var maxData_1 = [];
                        var chunkSize = getBucketSize(timeWindow, timeseriesData[0].data.length);
                        chunk(timeseriesData[0].data, chunkSize).forEach(function (seriesChunk) {
                            avgData_1.push({
                                name: seriesChunk[0].name,
                                value: AGGREGATE_FUNCTIONS.avg(seriesChunk),
                            });
                            minData_1.push({
                                name: seriesChunk[0].name,
                                value: AGGREGATE_FUNCTIONS.min(seriesChunk),
                            });
                            maxData_1.push({
                                name: seriesChunk[0].name,
                                value: AGGREGATE_FUNCTIONS.max(seriesChunk),
                            });
                        });
                        timeseriesData = [
                            timeseriesData[0],
                            { seriesName: t('Minimum'), data: minData_1 },
                            { seriesName: t('Average'), data: avgData_1 },
                            { seriesName: t('Maximum'), data: maxData_1 },
                        ];
                    }
                }
                var chart = (<React.Fragment>
                    {loading || reloading ? (<ChartPlaceholder />) : (<React.Fragment>
                        <TransparentLoadingMask visible={reloading}/>
                        <ThresholdsChart period={statsPeriod} maxValue={maxValue ? maxValue.value : maxValue} data={timeseriesData} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType}/>
                      </React.Fragment>)}
                    <ChartControls>
                      <InlineContainer>
                        <SectionHeading>{t('Total Events')}</SectionHeading>
                        {totalEvents !== null ? (<SectionValue>{totalEvents.toLocaleString()}</SectionValue>) : (<SectionValue>&mdash;</SectionValue>)}
                      </InlineContainer>
                      <InlineContainer>
                        <SectionHeading>{t('Display')}</SectionHeading>
                        <PeriodSelectControl inline={false} styles={{
                    control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '25px', height: '25px' })); },
                }} isSearchable={false} isClearable={false} disabled={loading || reloading} name="statsPeriod" value={period} choices={statsPeriodOptions.map(function (timePeriod) { return [
                    timePeriod,
                    TIME_PERIOD_MAP[timePeriod],
                ]; })} onChange={_this.handleStatsPeriodChange}/>
                      </InlineContainer>
                    </ChartControls>
                  </React.Fragment>);
                return (<Feature organization={organization} features={['metric-alert-gui-filters']}>
                    {function (_a) {
                    var hasGuiFilters = _a.hasFeature;
                    return hasGuiFilters ? (<React.Fragment>{chart}</React.Fragment>) : (<StickyWrapper>
                          <StyledPanel>
                            <StyledPanelBody>{chart}</StyledPanelBody>
                          </StyledPanel>
                        </StickyWrapper>);
                }}
                  </Feature>);
            }}
            </EventsRequest>);
        }}
      </Feature>);
    };
    return TriggersChart;
}(React.PureComponent));
export default withApi(TriggersChart);
var TransparentLoadingMask = styled(LoadingMask)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"], ["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"])), function (p) { return !p.visible && 'display: none;'; });
var ChartPlaceholder = styled(Placeholder)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  /* Height and margin should add up to graph size (200px) */\n  margin: 0 0 ", ";\n  height: 184px;\n"], ["\n  /* Height and margin should add up to graph size (200px) */\n  margin: 0 0 ", ";\n  height: 184px;\n"])), space(2));
var StickyWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: sticky;\n  top: ", ";\n  z-index: ", ";\n"], ["\n  position: sticky;\n  top: ", ";\n  z-index: ", ";\n"])), space(1), function (p) { return p.theme.zIndex.dropdown - 1; });
var StyledPanel = styled(Panel)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  /* Remove margin for the sticky window */\n  margin-bottom: 0;\n"], ["\n  /* Remove margin for the sticky window */\n  margin-bottom: 0;\n"])));
var StyledPanelBody = styled(PanelBody)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  h4 {\n    margin-bottom: ", ";\n  }\n  padding-top: ", ";\n"], ["\n  h4 {\n    margin-bottom: ", ";\n  }\n  padding-top: ", ";\n"])), space(1), space(2));
var PeriodSelectControl = styled(SelectControl)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: inline-block;\n  width: 180px;\n  font-weight: normal;\n  text-transform: none;\n  border: 0;\n"], ["\n  display: inline-block;\n  width: 180px;\n  font-weight: normal;\n  text-transform: none;\n  border: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map