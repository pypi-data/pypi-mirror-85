import { __assign, __rest } from "tslib";
import 'echarts/lib/chart/bar';
export default function barSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = __rest(props, ["data"]);
    return __assign(__assign({}, rest), { data: data, type: 'bar' });
}
//# sourceMappingURL=barSeries.jsx.map