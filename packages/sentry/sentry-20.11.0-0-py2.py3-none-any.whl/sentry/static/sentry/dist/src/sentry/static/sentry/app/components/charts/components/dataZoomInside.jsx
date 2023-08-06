import { __assign } from "tslib";
import 'echarts/lib/component/dataZoomInside';
var DEFAULT = {
    type: 'inside',
    zoomOnMouseWheel: 'shift',
    throttle: 50,
};
export default function DataZoomInside(props) {
    // `props` can be boolean, if so return default
    if (!props || !Array.isArray(props)) {
        var dataZoom = __assign(__assign({}, DEFAULT), props);
        return [dataZoom];
    }
    return props;
}
//# sourceMappingURL=dataZoomInside.jsx.map