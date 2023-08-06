import { __extends } from "tslib";
import React from 'react';
import { Panel } from 'app/components/panels';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { NUM_BUCKETS, PERCENTILE, WEB_VITAL_DETAILS, VITAL_GROUPS } from './constants';
import VitalCard from './vitalCard';
import MeasurementsHistogramQuery from './measurementsHistogramQuery';
var VitalsPanel = /** @class */ (function (_super) {
    __extends(VitalsPanel, _super);
    function VitalsPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    VitalsPanel.prototype.renderVitalCard = function (vital, isLoading, error, summary, failureRate, histogram, color, min, max, precision) {
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitalDetails = WEB_VITAL_DETAILS[vital];
        var zoomed = min !== undefined || max !== undefined;
        return (<MeasurementsHistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} measurements={zoomed ? [vitalDetails.slug] : []} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (results) {
            var _a, _b;
            var loading = zoomed ? results.isLoading : isLoading;
            var errored = zoomed ? results.error !== null : error;
            var chartData = zoomed ? (_b = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : histogram : histogram;
            return (<VitalCard location={location} isLoading={loading} error={errored} vital={vitalDetails} summary={summary} failureRate={failureRate} chartData={chartData} colors={color} eventView={eventView} organization={organization} min={min} max={max} precision={precision}/>);
        }}
      </MeasurementsHistogramQuery>);
    };
    VitalsPanel.prototype.renderVitalGroup = function (group, summaryResults) {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitals = group.vitals, colors = group.colors, min = group.min, max = group.max, precision = group.precision;
        var bounds = vitals.reduce(function (allBounds, vital) {
            var slug = WEB_VITAL_DETAILS[vital].slug;
            allBounds[vital] = {
                start: decodeScalar(location.query[slug + "Start"]),
                end: decodeScalar(location.query[slug + "End"]),
            };
            return allBounds;
        }, {});
        return (<MeasurementsHistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} measurements={vitals.map(function (vital) { return WEB_VITAL_DETAILS[vital].slug; })} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (multiHistogramResults) {
            var isLoading = summaryResults.isLoading || multiHistogramResults.isLoading;
            var error = summaryResults.error !== null || multiHistogramResults.error !== null;
            return (<React.Fragment>
              {vitals.map(function (vital, index) {
                var _a, _b, _c, _d, _e, _f, _g, _h;
                var details = WEB_VITAL_DETAILS[vital];
                var data = (_b = (_a = summaryResults.tableData) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b[0];
                var percentileAlias = getAggregateAlias("percentile(" + vital + ", " + PERCENTILE + ")");
                var summary = ((_c = data === null || data === void 0 ? void 0 : data[percentileAlias]) !== null && _c !== void 0 ? _c : null);
                var countAlias = getAggregateAlias("count_at_least(" + vital + ", 0)");
                var failedAlias = getAggregateAlias("count_at_least(" + vital + ", " + details.failureThreshold + ")");
                var numerator = ((_d = data === null || data === void 0 ? void 0 : data[failedAlias]) !== null && _d !== void 0 ? _d : 0);
                var denominator = ((_e = data === null || data === void 0 ? void 0 : data[countAlias]) !== null && _e !== void 0 ? _e : 0);
                var failureRate = denominator <= 0 ? 0 : numerator / denominator;
                var _j = (_f = bounds[vital]) !== null && _f !== void 0 ? _f : {}, start = _j.start, end = _j.end;
                return (<React.Fragment key={vital}>
                    {_this.renderVitalCard(vital, isLoading, error, summary, failureRate, (_h = (_g = multiHistogramResults.histograms) === null || _g === void 0 ? void 0 : _g[vital]) !== null && _h !== void 0 ? _h : [], [colors[index]], parseBound(start, precision), parseBound(end, precision), precision)}
                  </React.Fragment>);
            })}
            </React.Fragment>);
        }}
      </MeasurementsHistogramQuery>);
    };
    VitalsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView;
        return (<Panel>
        <DiscoverQuery location={location} orgSlug={organization.slug} eventView={eventView} limit={1}>
          {function (results) { return (<React.Fragment>
              {VITAL_GROUPS.map(function (vitalGroup) { return (<React.Fragment key={vitalGroup.vitals.join('')}>
                  {_this.renderVitalGroup(vitalGroup, results)}
                </React.Fragment>); })}
            </React.Fragment>); }}
        </DiscoverQuery>
      </Panel>);
    };
    return VitalsPanel;
}(React.Component));
function parseBound(boundString, precision) {
    if (boundString === undefined) {
        return undefined;
    }
    else if (precision === undefined || precision === 0) {
        return parseInt(boundString, 10);
    }
    return parseFloat(boundString);
}
export default VitalsPanel;
//# sourceMappingURL=vitalsPanel.jsx.map