import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import LineChart from 'app/components/charts/lineChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import TransitionChart from 'app/components/charts/transitionChart';
import EventsRequest from 'app/components/charts/eventsRequest';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import QuestionTooltip from 'app/components/questionTooltip';
import { getInterval, getSeriesSelection } from 'app/components/charts/utils';
import { IconWarning } from 'app/icons';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import withApi from 'app/utils/withApi';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { tooltipFormatter, axisLabelFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import { HeaderTitleLegend } from '../styles';
import { transformEventStatsSmoothed } from '../trends/utils';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var YAXIS_VALUES = [
    'p50()',
    'p75()',
    'p95()',
    'p99()',
    'p100()',
    'avg(transaction.duration)',
];
var TrendChart = /** @class */ (function (_super) {
    __extends(TrendChart, _super);
    function TrendChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { trendsUnselectedSeries: unselected }) });
            browserHistory.push(to);
        };
        return _this;
    }
    TrendChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router, trendDisplay = _a.trendDisplay;
        var start = this.props.start
            ? getUtcToLocalDateObject(this.props.start)
            : undefined;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : undefined;
        var utc = decodeScalar(router.location.query.utc);
        var legend = {
            right: 10,
            top: 0,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
            selected: getSeriesSelection(location),
        };
        var datetimeSelection = {
            start: start || null,
            end: end || null,
            period: statsPeriod,
        };
        var chartOptions = {
            grid: {
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: function (value) { return tooltipFormatter(value, 'p50()'); },
            },
            yAxis: {
                min: 0,
                axisLabel: {
                    color: theme.chartLabel,
                    // p50() coerces the axis to be time based
                    formatter: function (value) { return axisLabelFormatter(value, 'p50()'); },
                },
            },
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Trend')}
          <QuestionTooltip size="sm" position="top" title={t("Trends shows the smoothed value of an aggregate over time.")}/>
        </HeaderTitleLegend>
        <ChartZoom router={router} period={statsPeriod} projects={project} environments={environment}>
          {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={__spread(project)} environment={__spread(environment)} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={YAXIS_VALUES}>
              {function (_a) {
            var _results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
            if (errored) {
                return (<ErrorPanel>
                      <IconWarning color="gray300" size="lg"/>
                    </ErrorPanel>);
            }
            var results = _results === null || _results === void 0 ? void 0 : _results.filter(function (r) { return r.seriesName === trendDisplay; });
            var series = results
                ? results
                    .map(function (values) {
                    return __assign(__assign({}, values), { color: theme.purple300, lineStyle: {
                            opacity: 0.75,
                            width: 1,
                        } });
                })
                    .reverse()
                : [];
            var smoothedResults = transformEventStatsSmoothed(results, t('Smoothed')).smoothedResults;
            var smoothedSeries = smoothedResults
                ? smoothedResults.map(function (values) {
                    return __assign(__assign({}, values), { color: theme.purple300, lineStyle: {
                            opacity: 1,
                        } });
                })
                : [];
            // Stack the toolbox under the legend.
            // so all series names are clickable.
            zoomRenderProps.toolBox.z = -1;
            return (<ReleaseSeries start={start} end={end} period={statsPeriod} utc={utc} projects={project} environments={environment}>
                    {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return (<TransitionChart loading={loading} reloading={reloading}>
                        <TransparentLoadingMask visible={reloading}/>
                        {getDynamicText({
                    value: (<LineChart {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spread(series, smoothedSeries, releaseSeries)}/>),
                    fixed: 'Trend Chart',
                })}
                      </TransitionChart>);
            }}
                  </ReleaseSeries>);
        }}
            </EventsRequest>); }}
        </ChartZoom>
      </React.Fragment>);
    };
    return TrendChart;
}(React.Component));
export default withApi(ReactRouter.withRouter(TrendChart));
//# sourceMappingURL=trendChart.jsx.map