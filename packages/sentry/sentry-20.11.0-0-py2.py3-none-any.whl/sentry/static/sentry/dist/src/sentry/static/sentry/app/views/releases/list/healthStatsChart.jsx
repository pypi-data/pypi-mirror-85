import { __extends } from "tslib";
// TODO(matej): this is very similar to app/components/stream/groupChart, will refactor to reusable component in a follow-up PR
import React from 'react';
import LazyLoad from 'react-lazyload';
import { t } from 'app/locale';
import MiniBarChart from 'app/components/charts/miniBarChart';
import theme from 'app/utils/theme';
var HealthStatsChart = /** @class */ (function (_super) {
    __extends(HealthStatsChart, _super);
    function HealthStatsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HealthStatsChart.prototype.shouldComponentUpdate = function (nextProps) {
        // Sometimes statsPeriod updates before graph data has been
        // pulled from server / propagated down to components ...
        // don't update until data is available
        var data = nextProps.data, period = nextProps.period;
        return data.hasOwnProperty(period);
    };
    HealthStatsChart.prototype.getChartLabel = function () {
        var subject = this.props.subject;
        if (subject === 'users') {
            return t('Users');
        }
        return t('Sessions');
    };
    HealthStatsChart.prototype.render = function () {
        var _a = this.props, height = _a.height, period = _a.period, data = _a.data;
        var stats = period ? data[period] : null;
        if (!stats || !stats.length) {
            return null;
        }
        var colors = [theme.gray300];
        var emphasisColors = [theme.purple300];
        var series = [
            {
                seriesName: this.getChartLabel(),
                data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
            },
        ];
        return (<LazyLoad debounce={50} height={height}>
        <MiniBarChart series={series} height={height} colors={colors} emphasisColors={emphasisColors} isGroupedByDate showTimeInTooltip/>
      </LazyLoad>);
    };
    HealthStatsChart.defaultProps = {
        height: 24,
    };
    return HealthStatsChart;
}(React.Component));
export default HealthStatsChart;
//# sourceMappingURL=healthStatsChart.jsx.map