import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import BarSeries from './series/barSeries';
import BaseChart from './baseChart';
var BarChart = /** @class */ (function (_super) {
    __extends(BarChart, _super);
    function BarChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BarChart.prototype.render = function () {
        var _a = this.props, series = _a.series, stacked = _a.stacked, xAxis = _a.xAxis, props = __rest(_a, ["series", "stacked", "xAxis"]);
        return (<BaseChart {...props} xAxis={xAxis !== null ? __assign(__assign({}, (xAxis || {})), { boundaryGap: true }) : null} series={series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data, options = __rest(_a, ["seriesName", "data"]);
            return BarSeries(__assign({ name: seriesName, stack: stacked ? 'stack1' : undefined, data: data.map(function (_a) {
                    var value = _a.value, name = _a.name, itemStyle = _a.itemStyle;
                    if (itemStyle === undefined) {
                        return [name, value];
                    }
                    return { value: [name, value], itemStyle: itemStyle };
                }) }, options));
        })}/>);
    };
    BarChart.propTypes = __assign({}, BaseChart.propTypes);
    return BarChart;
}(React.Component));
export default BarChart;
//# sourceMappingURL=barChart.jsx.map