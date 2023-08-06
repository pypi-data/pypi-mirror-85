var _a;
import AreaChart from 'app/components/charts/areaChart';
import BarChart from 'app/components/charts/barChart';
import LineChart from 'app/components/charts/lineChart';
import PercentageAreaChart from 'app/components/charts/percentageAreaChart';
import PercentageTableChart from 'app/components/charts/percentageTableChart';
import PieChart from 'app/components/charts/pieChart';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import WorldMapChart from 'app/components/charts/worldMapChart';
import { WIDGET_DISPLAY } from '../constants';
var CHART_MAP = (_a = {},
    _a[WIDGET_DISPLAY.LINE_CHART] = LineChart,
    _a[WIDGET_DISPLAY.AREA_CHART] = AreaChart,
    _a[WIDGET_DISPLAY.STACKED_AREA_CHART] = StackedAreaChart,
    _a[WIDGET_DISPLAY.BAR_CHART] = BarChart,
    _a[WIDGET_DISPLAY.PIE_CHART] = PieChart,
    _a[WIDGET_DISPLAY.WORLD_MAP] = WorldMapChart,
    _a[WIDGET_DISPLAY.TABLE] = PercentageTableChart,
    _a[WIDGET_DISPLAY.PERCENTAGE_AREA_CHART] = PercentageAreaChart,
    _a);
export function getChartComponent(_a) {
    var type = _a.type;
    return CHART_MAP[type];
}
//# sourceMappingURL=getChartComponent.jsx.map