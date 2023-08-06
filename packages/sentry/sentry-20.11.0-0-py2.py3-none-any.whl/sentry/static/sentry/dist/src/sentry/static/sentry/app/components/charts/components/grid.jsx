import { __assign } from "tslib";
/**
 * Drawing grid in rectangular coordinates
 *
 * e.g. alignment of your chart?
 */
export default function Grid(props) {
    if (props === void 0) { props = {}; }
    return __assign({ top: 20, bottom: 20, 
        // This should allow for sufficient space for Y-axis labels
        left: '0%', right: '0%', containLabel: true }, props);
}
//# sourceMappingURL=grid.jsx.map