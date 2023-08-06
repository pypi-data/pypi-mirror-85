import { __extends } from "tslib";
import React from 'react';
import AreaChart from 'app/components/charts/areaChart';
var StackedAreaChart = /** @class */ (function (_super) {
    __extends(StackedAreaChart, _super);
    function StackedAreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StackedAreaChart.prototype.render = function () {
        return <AreaChart tooltip={{ filter: function (val) { return val > 0; } }} {...this.props} stacked/>;
    };
    return StackedAreaChart;
}(React.Component));
export default StackedAreaChart;
//# sourceMappingURL=stackedAreaChart.jsx.map