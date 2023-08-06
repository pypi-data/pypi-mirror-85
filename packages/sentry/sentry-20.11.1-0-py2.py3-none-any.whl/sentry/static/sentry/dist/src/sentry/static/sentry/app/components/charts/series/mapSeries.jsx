import { __assign } from "tslib";
import 'echarts/lib/chart/map';
export default function MapSeries(props) {
    if (props === void 0) { props = {}; }
    return __assign(__assign({ roam: true, itemStyle: {
            // TODO(ts): label doesn't seem to exist on the emphasis? I have not
            //           verified if removing this has an affect on the world chart.
            emphasis: { label: { show: false } },
        } }, props), { type: 'map' });
}
//# sourceMappingURL=mapSeries.jsx.map