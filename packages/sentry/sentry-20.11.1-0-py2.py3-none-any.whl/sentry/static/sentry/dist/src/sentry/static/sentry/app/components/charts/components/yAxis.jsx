import { __assign, __rest } from "tslib";
export default function YAxis(_a) {
    var theme = _a.theme, props = __rest(_a, ["theme"]);
    return __assign({ axisLine: {
            show: false,
        }, axisTick: {
            show: false,
        }, axisLabel: {
            color: theme.chartLabel,
        }, splitLine: {
            lineStyle: {
                color: theme.chartLineColor,
                opacity: 0.3,
            },
        } }, props);
}
//# sourceMappingURL=yAxis.jsx.map