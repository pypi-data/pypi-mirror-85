import LazyLoad from 'react-lazyload';
import React from 'react';
import { t } from 'app/locale';
import MiniBarChart from 'app/components/charts/miniBarChart';
import theme from 'app/utils/theme';
function GroupChart(_a) {
    var data = _a.data, statsPeriod = _a.statsPeriod, _b = _a.showSecondaryPoints, showSecondaryPoints = _b === void 0 ? false : _b, _c = _a.height, height = _c === void 0 ? 24 : _c;
    var stats = statsPeriod
        ? data.filtered
            ? data.filtered.stats[statsPeriod]
            : data.stats[statsPeriod]
        : null;
    var secondaryStats = statsPeriod && data.filtered ? data.stats[statsPeriod] : null;
    if (!stats || !stats.length) {
        return null;
    }
    var colors = undefined;
    var emphasisColors = undefined;
    var series = [];
    if (showSecondaryPoints && secondaryStats && secondaryStats.length) {
        series.push({
            seriesName: t('Total Events'),
            data: secondaryStats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
        series.push({
            seriesName: t('Matching Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
    }
    else {
        // Colors are custom to preserve historical appearance where the single series is
        // considerably darker than the two series results.
        colors = [theme.gray300];
        emphasisColors = [theme.purple300];
        series.push({
            seriesName: t('Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        });
    }
    return (<LazyLoad debounce={50} height={height}>
      <MiniBarChart height={height} isGroupedByDate showTimeInTooltip series={series} colors={colors} emphasisColors={emphasisColors}/>
    </LazyLoad>);
}
export default GroupChart;
//# sourceMappingURL=groupChart.jsx.map