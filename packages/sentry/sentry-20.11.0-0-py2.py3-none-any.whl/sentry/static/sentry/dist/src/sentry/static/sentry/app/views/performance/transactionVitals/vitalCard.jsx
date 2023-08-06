import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import throttle from 'lodash/throttle';
import isEqual from 'lodash/isEqual';
import BarChart from 'app/components/charts/barChart';
import BarChartZoom from 'app/components/charts/barChartZoom';
import MarkLine from 'app/components/charts/components/markLine';
import MarkPoint from 'app/components/charts/components/markPoint';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import Tag from 'app/components/tagDeprecated';
import DiscoverButton from 'app/components/discoverButton';
import { FIRE_SVG_PATH } from 'app/icons/iconFire';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { formatAbbreviatedNumber, formatFloat, formatPercentage, getDuration, } from 'app/utils/formatters';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import theme from 'app/utils/theme';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { NUM_BUCKETS, PERCENTILE } from './constants';
import { Card, CardSummary, CardSectionHeading, StatNumber, Description } from './styles';
import { findNearestBucketIndex, getRefRect, asPixelRect, mapPoint } from './utils';
var VitalCard = /** @class */ (function (_super) {
    __extends(VitalCard, _super);
    function VitalCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            refDataRect: null,
            refPixelRect: null,
        };
        _this.trackOpenInDiscoverClicked = function () {
            var organization = _this.props.organization;
            var vital = _this.props.vital;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.open_in_discover',
                eventName: 'Performance Views: Open vitals in discover',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        /**
         * This callback happens everytime ECharts renders. This is NOT when ECharts
         * finishes rendering, so it can be called quite frequently. The calculations
         * here can get expensive if done frequently, furthermore, this can trigger a
         * state change leading to a re-render. So slow down the updates here as they
         * do not need to be updated every single time.
         */
        _this.handleRendered = throttle(function (_, chartRef) {
            var chartData = _this.props.chartData;
            var refDataRect = _this.state.refDataRect;
            if (refDataRect === null || chartData.length < 1) {
                return;
            }
            var refPixelRect = refDataRect === null ? null : asPixelRect(chartRef, refDataRect);
            if (refPixelRect !== null && !isEqual(refPixelRect, _this.state.refPixelRect)) {
                _this.setState({ refPixelRect: refPixelRect });
            }
        }, 200, { leading: true });
        _this.handleDataZoomCancelled = function () { };
        return _this;
    }
    VitalCard.getDerivedStateFromProps = function (nextProps, prevState) {
        var isLoading = nextProps.isLoading, error = nextProps.error, chartData = nextProps.chartData;
        if (isLoading || error === null) {
            return __assign({}, prevState);
        }
        var refDataRect = getRefRect(chartData);
        if (prevState.refDataRect === null ||
            (refDataRect !== null && !isEqual(refDataRect, prevState.refDataRect))) {
            return __assign(__assign({}, prevState), { refDataRect: refDataRect });
        }
        return __assign({}, prevState);
    };
    VitalCard.prototype.getFormattedStatNumber = function () {
        var _a = this.props, summary = _a.summary, vital = _a.vital;
        var type = vital.type;
        return summary === null
            ? '\u2014'
            : type === 'duration'
                ? getDuration(summary / 1000, 2, true)
                : formatFloat(summary, 2);
    };
    VitalCard.prototype.renderSummary = function () {
        var _a;
        var _b = this.props, summary = _b.summary, vital = _b.vital, colors = _b.colors, eventView = _b.eventView, organization = _b.organization, min = _b.min, max = _b.max;
        var slug = vital.slug, name = vital.name, description = vital.description, failureThreshold = vital.failureThreshold;
        var column = "measurements." + slug;
        var newEventView = eventView
            .withColumns([
            { kind: 'field', field: 'transaction' },
            { kind: 'function', function: ['percentile', column, PERCENTILE.toString()] },
            { kind: 'function', function: ['count', '', ''] },
        ])
            .withSorts([
            {
                kind: 'desc',
                field: getAggregateAlias("percentile(" + column + "," + PERCENTILE.toString() + ")"),
            },
        ]);
        var query = tokenizeSearch((_a = newEventView.query) !== null && _a !== void 0 ? _a : '');
        query.addTagValues('has', [column]);
        // add in any range constraints if any
        if (min !== undefined || max !== undefined) {
            if (min !== undefined) {
                query.addTagValues(column, [">=" + min]);
            }
            if (max !== undefined) {
                query.addTagValues(column, ["<=" + max]);
            }
        }
        newEventView.query = stringifyQueryObject(query);
        return (<CardSummary>
        <Indicator color={colors[0]}/>
        <CardSectionHeading>
          {name + " (" + slug.toUpperCase() + ")"}
          {summary === null ? null : summary < failureThreshold ? (<StyledTag color={theme.purple300}>{t('pass')}</StyledTag>) : (<StyledTag color={theme.red300}>{t('fail')}</StyledTag>)}
        </CardSectionHeading>
        <StatNumber>{this.getFormattedStatNumber()}</StatNumber>
        <Description>{description}</Description>
        <div>
          <DiscoverButton size="small" to={newEventView.getResultsViewUrlTarget(organization.slug)} onClick={this.trackOpenInDiscoverClicked}>
            {t('Open in Discover')}
          </DiscoverButton>
        </div>
      </CardSummary>);
    };
    VitalCard.prototype.renderHistogram = function () {
        var _this = this;
        var _a = this.props, location = _a.location, isLoading = _a.isLoading, error = _a.error, colors = _a.colors, vital = _a.vital, _b = _a.precision, precision = _b === void 0 ? 0 : _b;
        var slug = vital.slug;
        var series = this.getSeries();
        var xAxis = {
            type: 'category',
            truncate: true,
            axisLabel: {
                margin: 20,
            },
            axisTick: {
                alignWithLabel: true,
            },
        };
        var values = series.data.map(function (point) { return point.value; });
        var max = values.length ? Math.max.apply(Math, __spread(values)) : undefined;
        var yAxis = {
            type: 'value',
            max: max,
            axisLabel: {
                color: theme.chartLabel,
                formatter: formatAbbreviatedNumber,
            },
        };
        var allSeries = [series];
        if (!isLoading && !error) {
            var baselineSeries = this.getBaselineSeries();
            if (baselineSeries !== null) {
                allSeries.push(baselineSeries);
            }
            var failureSeries = this.getFailureSeries();
            if (failureSeries !== null) {
                allSeries.push(failureSeries);
            }
        }
        return (<BarChartZoom minZoomWidth={Math.pow(10, -precision) * NUM_BUCKETS} location={location} paramStart={slug + "Start"} paramEnd={slug + "End"} xAxisIndex={[0]} buckets={this.computeBuckets()} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<Container>
            <TransparentLoadingMask visible={isLoading}/>
            <BarChart series={allSeries} xAxis={xAxis} yAxis={yAxis} colors={colors} onRendered={_this.handleRendered} grid={{ left: space(3), right: space(3), top: space(3), bottom: space(1.5) }} stacked {...zoomRenderProps}/>
          </Container>); }}
      </BarChartZoom>);
    };
    VitalCard.prototype.bucketWidth = function () {
        var chartData = this.props.chartData;
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return chartData.length >= 2 ? chartData[1].histogram - chartData[0].histogram : 0;
    };
    VitalCard.prototype.computeBuckets = function () {
        var chartData = this.props.chartData;
        var bucketWidth = this.bucketWidth();
        return chartData.map(function (item) {
            var bucket = item.histogram;
            return {
                start: bucket,
                end: bucket + bucketWidth,
            };
        });
    };
    VitalCard.prototype.getSeries = function () {
        var _a = this.props, chartData = _a.chartData, vital = _a.vital;
        var bucketWidth = this.bucketWidth();
        var seriesData = chartData.map(function (item) {
            var bucket = item.histogram;
            var midPoint = bucketWidth > 1 ? Math.ceil(bucket + bucketWidth / 2) : bucket;
            var name = vital.type === 'duration'
                ? formatDuration(midPoint)
                : // This is trying to avoid some of potential rounding errors that cause bins
                    // have the same label, if the number of bins doesn't visually match what is
                    // expected, check that this rounding is correct. If this issue persists,
                    // consider formatting the bin as a string in the response
                    (Math.round((midPoint + Number.EPSILON) * 100) / 100).toLocaleString();
            return {
                value: item.count,
                name: name,
            };
        });
        return {
            seriesName: t('Count'),
            data: seriesData,
        };
    };
    VitalCard.prototype.getBaselineSeries = function () {
        var _a = this.props, chartData = _a.chartData, summary = _a.summary;
        if (summary === null || this.state.refPixelRect === null) {
            return null;
        }
        var summaryBucket = findNearestBucketIndex(chartData, this.bucketWidth(), summary);
        if (summaryBucket === null || summaryBucket === -1) {
            return null;
        }
        var thresholdPixelBottom = mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: 0,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelBottom === null) {
            return null;
        }
        var thresholdPixelTop = mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: Math.max.apply(Math, __spread(chartData.map(function (data) { return data.count; }))) || 1,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelTop === null) {
            return null;
        }
        var markLine = MarkLine({
            animationDuration: 200,
            data: [[thresholdPixelBottom, thresholdPixelTop]],
            label: {
                show: false,
            },
            lineStyle: {
                color: theme.textColor,
                type: 'solid',
            },
        });
        // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
        // if we add it in the constructor. So we opt to add it here so typescript
        // doesn't complain.
        markLine.tooltip = {
            formatter: function () {
                return [
                    '<div class="tooltip-series tooltip-series-solo">',
                    '<span class="tooltip-label">',
                    "<strong>" + t('Baseline') + "</strong>",
                    '</span>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        return {
            seriesName: t('Baseline'),
            data: [],
            markLine: markLine,
        };
    };
    VitalCard.prototype.getFailureSeries = function () {
        var _a = this.props, chartData = _a.chartData, vital = _a.vital, failureRate = _a.failureRate;
        var failureThreshold = vital.failureThreshold, type = vital.type;
        if (this.state.refDataRect === null || this.state.refPixelRect === null) {
            return null;
        }
        var failureBucket = findNearestBucketIndex(chartData, this.bucketWidth(), failureThreshold);
        if (failureBucket === null) {
            return null;
        }
        failureBucket = failureBucket === -1 ? 0 : failureBucket;
        // since we found the failure bucket, the failure threshold is
        // visible on the graph, so let's draw the fail region
        var failurePixel = mapPoint({
            // subtract 0.5 from the x here to ensure that the boundary of
            // the failure region lies between buckets
            x: failureBucket - 0.5,
            y: 0,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (failurePixel === null) {
            return null;
        }
        var topRightPixel = mapPoint({
            // subtract 0.5 to get on the right side of the right most bar
            x: chartData.length - 0.5,
            y: Math.max.apply(Math, __spread(chartData.map(function (data) { return data.count; }))) || 1,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (topRightPixel === null) {
            return null;
        }
        // Using a MarkArea means that hovering over the interior of the area
        // will trigger the tooltip for the MarkArea, making it impossible to
        // see outliers with the tooltip. So we get around this using lines.
        var markLine = MarkLine({
            animation: false,
            data: [
                // left
                [
                    { x: failurePixel.x, y: failurePixel.y },
                    { x: failurePixel.x, y: topRightPixel.y },
                ],
                // top
                [
                    { x: failurePixel.x, y: topRightPixel.y },
                    { x: topRightPixel.x, y: topRightPixel.y },
                ],
                // right
                [
                    { x: topRightPixel.x, y: topRightPixel.y },
                    { x: topRightPixel.x, y: failurePixel.y },
                ],
            ],
            label: {
                show: false,
            },
            lineStyle: {
                color: theme.red300,
                type: 'dashed',
                width: 1.5,
                // prevent each individual line from looking emphasized
                // by styling it the same as the unemphasized line
                emphasis: {
                    color: theme.red300,
                    type: 'dashed',
                    width: 1.5,
                },
            },
        });
        markLine.tooltip = {
            formatter: function () {
                return [
                    '<div class="tooltip-series tooltip-series-solo">',
                    '<span class="tooltip-label">',
                    '<strong>',
                    t('Fails threshold at %s.', type === 'duration'
                        ? getDuration(failureThreshold / 1000, 2, true)
                        : formatFloat(failureThreshold, 2)),
                    '</strong>',
                    '</span>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        var markPoint = MarkPoint({
            animationDuration: 200,
            data: [{ x: topRightPixel.x - 16, y: topRightPixel.y + 16 }],
            itemStyle: { color: theme.red300 },
            silent: true,
            symbol: "path://" + FIRE_SVG_PATH,
            symbolKeepAspect: true,
            symbolSize: [14, 16],
            label: {
                formatter: formatPercentage(failureRate, 0),
                position: 'left',
            },
        });
        return {
            seriesName: t('Failure Region'),
            data: [],
            markLine: markLine,
            markPoint: markPoint,
        };
    };
    VitalCard.prototype.render = function () {
        return (<Card>
        {this.renderSummary()}
        {this.renderHistogram()}
      </Card>);
    };
    return VitalCard;
}(React.Component));
var Indicator = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: 20px;\n  left: 0px;\n  width: 6px;\n  height: 18px;\n  border-radius: 0 3px 3px 0;\n  background-color: ", ";\n"], ["\n  position: absolute;\n  top: 20px;\n  left: 0px;\n  width: 6px;\n  height: 18px;\n  border-radius: 0 3px 3px 0;\n  background-color: ", ";\n"])), function (p) { return p.color; });
var StyledTag = styled(Tag)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  right: ", ";\n  background-color: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  right: ", ";\n  background-color: ", ";\n  color: ", ";\n"])), space(3), function (p) { return p.color; }, function (p) { return p.theme.white; });
var Container = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
function formatDuration(duration) {
    // assume duration is in milliseconds.
    if (duration <= 1000) {
        return getDuration(duration / 1000, 2, true);
    }
    return getDuration(duration / 1000, 3, true);
}
export default VitalCard;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=vitalCard.jsx.map