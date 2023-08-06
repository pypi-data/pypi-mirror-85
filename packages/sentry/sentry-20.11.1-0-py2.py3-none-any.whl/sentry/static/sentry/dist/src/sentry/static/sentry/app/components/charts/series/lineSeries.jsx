import { __assign } from "tslib";
import 'echarts/lib/chart/line';
import theme from 'app/utils/theme';
export default function LineSeries(props) {
    return __assign(__assign({ showSymbol: false, symbolSize: theme.charts.symbolSize }, props), { type: 'line' });
}
//# sourceMappingURL=lineSeries.jsx.map