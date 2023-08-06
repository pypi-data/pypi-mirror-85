import { __extends, __read, __spread } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import BarChart from 'app/components/charts/barChart';
import ErrorPanel from 'app/components/charts/errorPanel';
import LoadingPanel from 'app/components/charts/loadingPanel';
import QuestionTooltip from 'app/components/questionTooltip';
import AsyncComponent from 'app/components/asyncComponent';
import EventView from 'app/utils/discover/eventView';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import theme from 'app/utils/theme';
import { getDuration } from 'app/utils/formatters';
import BarChartZoom from 'app/components/charts/barChartZoom';
import { HeaderTitleLegend } from '../styles';
var NUM_BUCKETS = 15;
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
/**
 * Fetch and render a bar chart that shows event volume
 * for each duration bucket. We always render 15 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
var LatencyChart = /** @class */ (function (_super) {
    __extends(LatencyChart, _super);
    function LatencyChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleMouseOver = function () {
            // Hide the zoom error tooltip on the next hover.
            if (_this.state.zoomError) {
                _this.setState({ zoomError: false });
            }
        };
        _this.handleDataZoom = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.latency_chart.zoom',
                eventName: 'Performance Views: Transaction Summary Latency Chart Zoom',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleDataZoomCancelled = function () {
            _this.setState({ zoomError: true });
        };
        return _this;
    }
    LatencyChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, query = _a.query, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, environment = _a.environment, project = _a.project, location = _a.location;
        var eventView = EventView.fromSavedQuery({
            id: '',
            name: '',
            version: 2,
            fields: ["histogram(transaction.duration," + NUM_BUCKETS + ")", 'count()'],
            orderby: 'histogram_transaction_duration_15',
            projects: project,
            range: statsPeriod,
            query: query,
            environment: environment,
            start: start,
            end: end,
        });
        var apiPayload = eventView.getEventsAPIPayload(location);
        apiPayload.referrer = 'api.performance.latencychart';
        return [
            ['chartData', "/organizations/" + organization.slug + "/eventsv2/", { query: apiPayload }],
        ];
    };
    LatencyChart.prototype.componentDidUpdate = function (prevProps) {
        if (this.shouldRefetchData(prevProps)) {
            this.fetchData();
        }
    };
    LatencyChart.prototype.shouldRefetchData = function (prevProps) {
        if (this.state.loading) {
            return false;
        }
        return !isEqual(pick(prevProps, QUERY_KEYS), pick(this.props, QUERY_KEYS));
    };
    Object.defineProperty(LatencyChart.prototype, "bucketWidth", {
        get: function () {
            if (this.state.chartData === null) {
                return 0;
            }
            // We can assume that all buckets are of equal width, use the first two
            // buckets to get the width. The value of each histogram function indicates
            // the beginning of the bucket.
            var data = this.state.chartData.data;
            return data.length > 2
                ? data[1].histogram_transaction_duration_15 -
                    data[0].histogram_transaction_duration_15
                : 0;
        },
        enumerable: false,
        configurable: true
    });
    LatencyChart.prototype.renderLoading = function () {
        return <LoadingPanel data-test-id="histogram-loading"/>;
    };
    LatencyChart.prototype.renderError = function () {
        // Don't call super as we don't really need issues for this.
        return (<ErrorPanel>
        <IconWarning color="gray300" size="lg"/>
      </ErrorPanel>);
    };
    LatencyChart.prototype.renderBody = function () {
        var _this = this;
        var location = this.props.location;
        var _a = this.state, chartData = _a.chartData, zoomError = _a.zoomError;
        if (chartData === null) {
            return null;
        }
        var xAxis = {
            type: 'category',
            truncate: true,
            axisLabel: {
                margin: 20,
            },
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        };
        var colors = __spread(theme.charts.getColorPalette(1));
        // Use a custom tooltip formatter as we need to replace
        // the tooltip content entirely when zooming is no longer available.
        var tooltip = {
            formatter: function (series) {
                var seriesData = Array.isArray(series) ? series : [series];
                var contents = [];
                if (!zoomError) {
                    // Replicate the necessary logic from app/components/charts/components/tooltip.jsx
                    contents = seriesData.map(function (item) {
                        var label = item.seriesName;
                        var value = item.value[1].toLocaleString();
                        return [
                            '<div class="tooltip-series">',
                            "<div><span class=\"tooltip-label\">" + item.marker + " <strong>" + label + "</strong></span> " + value + "</div>",
                            '</div>',
                        ].join('');
                    });
                    var seriesLabel = seriesData[0].value[0];
                    contents.push("<div class=\"tooltip-date\">" + seriesLabel + "</div>");
                }
                else {
                    contents = [
                        '<div class="tooltip-series tooltip-series-solo">',
                        t('Target zoom region too small'),
                        '</div>',
                    ];
                }
                contents.push('<div class="tooltip-arrow"></div>');
                return contents.join('');
            },
        };
        var bucketWidth = this.bucketWidth;
        var buckets = computeBuckets(chartData.data, bucketWidth);
        return (<BarChartZoom minZoomWidth={NUM_BUCKETS} location={location} paramStart="startDuration" paramEnd="endDuration" xAxisIndex={[0]} buckets={buckets} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<BarChart grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={xAxis} yAxis={{ type: 'value' }} series={transformData(chartData.data, bucketWidth)} tooltip={tooltip} colors={colors} onMouseOver={_this.handleMouseOver} {...zoomRenderProps}/>); }}
      </BarChartZoom>);
    };
    LatencyChart.prototype.render = function () {
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Latency Distribution')}
          <QuestionTooltip position="top" size="sm" title={t("Latency Distribution reflects the volume of transactions per median duration.")}/>
        </HeaderTitleLegend>
        {this.renderComponent()}
      </React.Fragment>);
    };
    return LatencyChart;
}(AsyncComponent));
function computeBuckets(data, bucketWidth) {
    return data.map(function (item) {
        var bucket = item.histogram_transaction_duration_15;
        return {
            start: bucket,
            end: bucket + bucketWidth,
        };
    });
}
/**
 * Convert a discover response into a barchart compatible series
 */
function transformData(data, bucketWidth) {
    var precision;
    if (bucketWidth < 10) {
        precision = 4;
    }
    else if (bucketWidth < 100) {
        precision = 3;
    }
    else if (bucketWidth < 1000) {
        precision = 2;
    }
    else if (bucketWidth < 10000) {
        precision = 1;
    }
    else {
        precision = 0;
    }
    var seriesData = data.map(function (item) {
        var bucket = item.histogram_transaction_duration_15;
        var midPoint = bucketWidth > 1 ? Math.ceil(bucket + bucketWidth / 2) : bucket;
        return {
            value: item.count,
            name: getDuration(midPoint / 1000, midPoint > 1000 ? precision : 0, true),
        };
    });
    return [
        {
            seriesName: t('Count'),
            data: seriesData,
        },
    ];
}
export default LatencyChart;
//# sourceMappingURL=latencyChart.jsx.map