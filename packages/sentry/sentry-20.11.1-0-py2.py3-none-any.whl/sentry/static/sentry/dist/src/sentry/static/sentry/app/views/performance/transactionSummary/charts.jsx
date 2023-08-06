import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import { Panel } from 'app/components/panels';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { decodeScalar } from 'app/utils/queryString';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartContainer } from '../styles';
import DurationChart from './durationChart';
import LatencyChart from './latencyChart';
import TrendChart from './trendChart';
import VitalsChart from './vitalsChart';
import DurationPercentileChart from './durationPercentileChart';
import { TrendFunctionField } from '../trends/types';
import { TRENDS_FUNCTIONS } from '../trends/utils';
export var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DURATION_PERCENTILE"] = "durationpercentile";
    DisplayModes["DURATION"] = "duration";
    DisplayModes["LATENCY"] = "latency";
    DisplayModes["TREND"] = "trend";
    DisplayModes["VITALS"] = "vitals";
})(DisplayModes || (DisplayModes = {}));
var DISPLAY_OPTIONS = [
    { value: DisplayModes.DURATION, label: t('Duration Breakdown') },
    { value: DisplayModes.DURATION_PERCENTILE, label: t('Duration Percentiles') },
    { value: DisplayModes.LATENCY, label: t('Latency Distribution') },
    { value: DisplayModes.TREND, label: t('Trends') },
    { value: DisplayModes.VITALS, label: t('Web Vitals') },
];
var TREND_OPTIONS = TRENDS_FUNCTIONS.map(function (_a) {
    var field = _a.field, label = _a.label;
    return ({
        value: field,
        label: label,
    });
});
var TransactionSummaryCharts = /** @class */ (function (_super) {
    __extends(TransactionSummaryCharts, _super);
    function TransactionSummaryCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisplayChange = function (value) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { display: value }),
            });
        };
        _this.handleTrendDisplayChange = function (value) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { trendDisplay: value }),
            });
        };
        return _this;
    }
    TransactionSummaryCharts.prototype.render = function () {
        var _a = this.props, totalValues = _a.totalValues, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var display = decodeScalar(location.query.display) || DisplayModes.DURATION;
        var trendDisplay = decodeScalar(location.query.trendDisplay) || TrendFunctionField.P50;
        if (!Object.values(DisplayModes).includes(display)) {
            display = DisplayModes.DURATION;
        }
        if (!Object.values(TrendFunctionField).includes(trendDisplay)) {
            trendDisplay = TrendFunctionField.P50;
        }
        return (<Panel>
        <ChartContainer>
          {display === DisplayModes.LATENCY && (<LatencyChart organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.DURATION && (<DurationChart organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.DURATION_PERCENTILE && (<DurationPercentileChart organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.TREND && (<TrendChart trendDisplay={trendDisplay} organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.VITALS && (<VitalsChart organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
        </ChartContainer>

        <ChartControls>
          <InlineContainer>
            <SectionHeading key="total-heading">{t('Total Transactions')}</SectionHeading>
            <SectionValue key="total-value">{calculateTotal(totalValues)}</SectionValue>
          </InlineContainer>
          <InlineContainer>
            {display === DisplayModes.TREND && (<OptionSelector title={t('Trend')} selected={trendDisplay} options={TREND_OPTIONS} onChange={this.handleTrendDisplayChange}/>)}
            <OptionSelector title={t('Display')} selected={display} options={DISPLAY_OPTIONS} onChange={this.handleDisplayChange}/>
          </InlineContainer>
        </ChartControls>
      </Panel>);
    };
    return TransactionSummaryCharts;
}(React.Component));
function calculateTotal(total) {
    if (total === null) {
        return '\u2014';
    }
    return total.toLocaleString();
}
export default TransactionSummaryCharts;
//# sourceMappingURL=charts.jsx.map