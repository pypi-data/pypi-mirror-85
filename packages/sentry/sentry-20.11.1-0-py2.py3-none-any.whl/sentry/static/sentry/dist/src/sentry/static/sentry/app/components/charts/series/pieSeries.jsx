import { __assign } from "tslib";
import 'echarts/lib/chart/pie';
export default function PieSeries(props) {
    if (props === void 0) { props = {}; }
    return __assign(__assign({ radius: ['50%', '70%'] }, props), { type: 'pie' });
}
//# sourceMappingURL=pieSeries.jsx.map