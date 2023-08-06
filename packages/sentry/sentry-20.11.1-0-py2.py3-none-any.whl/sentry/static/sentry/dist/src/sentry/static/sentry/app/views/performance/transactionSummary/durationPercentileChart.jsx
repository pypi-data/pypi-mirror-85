import { __extends, __read, __spread } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import AreaChart from 'app/components/charts/areaChart';
import ErrorPanel from 'app/components/charts/errorPanel';
import LoadingPanel from 'app/components/charts/loadingPanel';
import QuestionTooltip from 'app/components/questionTooltip';
import AsyncComponent from 'app/components/asyncComponent';
import EventView from 'app/utils/discover/eventView';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import theme from 'app/utils/theme';
import { getDuration } from 'app/utils/formatters';
import { HeaderTitleLegend } from '../styles';
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
var DurationPercentileChart = /** @class */ (function (_super) {
    __extends(DurationPercentileChart, _super);
    function DurationPercentileChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DurationPercentileChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, query = _a.query, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, environment = _a.environment, project = _a.project, location = _a.location;
        var eventView = EventView.fromSavedQuery({
            id: '',
            name: '',
            version: 2,
            fields: [
                'percentile(transaction.duration, 0.10)',
                'percentile(transaction.duration, 0.25)',
                'percentile(transaction.duration, 0.50)',
                'percentile(transaction.duration, 0.75)',
                'percentile(transaction.duration, 0.90)',
                'percentile(transaction.duration, 0.95)',
                'percentile(transaction.duration, 0.99)',
                'percentile(transaction.duration, 0.995)',
                'percentile(transaction.duration, 0.999)',
                'p100()',
            ],
            orderby: '',
            projects: project,
            range: statsPeriod,
            query: query,
            environment: environment,
            start: start,
            end: end,
        });
        var apiPayload = eventView.getEventsAPIPayload(location);
        apiPayload.referrer = 'api.performance.durationpercentilechart';
        return [
            ['chartData', "/organizations/" + organization.slug + "/eventsv2/", { query: apiPayload }],
        ];
    };
    DurationPercentileChart.prototype.componentDidUpdate = function (prevProps) {
        if (this.shouldRefetchData(prevProps)) {
            this.fetchData();
        }
    };
    DurationPercentileChart.prototype.shouldRefetchData = function (prevProps) {
        if (this.state.loading) {
            return false;
        }
        return !isEqual(pick(prevProps, QUERY_KEYS), pick(this.props, QUERY_KEYS));
    };
    DurationPercentileChart.prototype.renderLoading = function () {
        return <LoadingPanel data-test-id="histogram-loading"/>;
    };
    DurationPercentileChart.prototype.renderError = function () {
        // Don't call super as we don't really need issues for this.
        return (<ErrorPanel>
        <IconWarning color="gray300" size="lg"/>
      </ErrorPanel>);
    };
    DurationPercentileChart.prototype.renderBody = function () {
        var chartData = this.state.chartData;
        if (chartData === null) {
            return null;
        }
        var xAxis = {
            type: 'category',
            truncate: true,
            axisLabel: {
                showMinLabel: true,
                showMaxLabel: true,
            },
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        };
        var yAxis = {
            type: 'value',
            axisLabel: {
                color: theme.chartLabel,
                // Use p50() to force time formatting.
                formatter: function (value) { return axisLabelFormatter(value, 'p50()'); },
            },
        };
        var tooltip = {
            valueFormatter: function (value) {
                return getDuration(value / 1000, 2);
            },
        };
        var colors = theme.charts.getColorPalette(1);
        return (<AreaChart grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={xAxis} yAxis={yAxis} series={transformData(chartData.data)} tooltip={tooltip} colors={__spread(colors)}/>);
    };
    DurationPercentileChart.prototype.render = function () {
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Duration Percentiles')}
          <QuestionTooltip position="top" size="sm" title={t("Compare the duration at each percentile. Compare with Latency Histogram to see transaction volume at duration intervals.")}/>
        </HeaderTitleLegend>
        {this.renderComponent()}
      </React.Fragment>);
    };
    return DurationPercentileChart;
}(AsyncComponent));
var VALUE_EXTRACT_PATTERN = /(\d+)$/;
/**
 * Convert a discover response into a barchart compatible series
 */
function transformData(data) {
    var extractedData = Object.keys(data[0])
        .map(function (key) {
        var nameMatch = VALUE_EXTRACT_PATTERN.exec(key);
        if (!nameMatch) {
            return [-1, -1];
        }
        var nameValue = Number(nameMatch[1]);
        if (nameValue > 100) {
            nameValue /= 10;
        }
        return [nameValue, data[0][key]];
    })
        .filter(function (i) { return i[0] > 0; });
    extractedData.sort(function (a, b) {
        if (a[0] > b[0]) {
            return 1;
        }
        if (a[0] < b[0]) {
            return -1;
        }
        return 0;
    });
    return [
        {
            seriesName: t('Duration'),
            data: extractedData.map(function (i) { return ({ value: i[1], name: i[0].toLocaleString() + "%" }); }),
        },
    ];
}
export default DurationPercentileChart;
//# sourceMappingURL=durationPercentileChart.jsx.map