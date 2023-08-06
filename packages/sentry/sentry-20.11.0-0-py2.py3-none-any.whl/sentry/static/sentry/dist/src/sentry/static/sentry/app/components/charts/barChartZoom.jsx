import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import DataZoomInside from 'app/components/charts/components/dataZoomInside';
import ToolBox from 'app/components/charts/components/toolBox';
import { callIfFunction } from 'app/utils/callIfFunction';
var BarChartZoom = /** @class */ (function (_super) {
    __extends(BarChartZoom, _super);
    function BarChartZoom() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Enable zoom immediately instead of having to toggle to zoom
         */
        _this.handleChartReady = function (chart) {
            chart.dispatchAction({
                type: 'takeGlobalCursor',
                key: 'dataZoomSelect',
                dataZoomSelectActive: true,
            });
            callIfFunction(_this.props.onChartReady, chart);
        };
        _this.handleDataZoom = function (evt, chart) {
            var _a;
            var model = chart.getModel();
            var xAxis = model.option.xAxis;
            var axis = xAxis[0];
            // Both of these values should not be null, but we include it just in case.
            // These values are null when the user uses the toolbox included in ECharts
            // to navigate back through zoom history, but we hide it below.
            if (axis.rangeStart !== null && axis.rangeEnd !== null) {
                var _b = _this.props, buckets = _b.buckets, location_1 = _b.location, paramStart = _b.paramStart, paramEnd = _b.paramEnd, minZoomWidth = _b.minZoomWidth;
                var start = buckets[axis.rangeStart].start;
                var end = buckets[axis.rangeEnd].end;
                if (minZoomWidth === undefined || end - start > minZoomWidth) {
                    var target = {
                        pathname: location_1.pathname,
                        query: __assign(__assign({}, location_1.query), (_a = {}, _a[paramStart] = start, _a[paramEnd] = end, _a)),
                    };
                    browserHistory.push(target);
                }
                else {
                    // Dispatch the restore action here to stop ECharts from zooming
                    chart.dispatchAction({ type: 'restore' });
                    callIfFunction(_this.props.onDataZoomCancelled);
                }
            }
            else {
                // Dispatch the restore action here to stop ECharts from zooming
                chart.dispatchAction({ type: 'restore' });
                callIfFunction(_this.props.onDataZoomCancelled);
            }
            callIfFunction(_this.props.onDataZoom, evt, chart);
        };
        return _this;
    }
    BarChartZoom.prototype.render = function () {
        var _a = this.props, children = _a.children, xAxisIndex = _a.xAxisIndex;
        var renderProps = {
            onChartReady: this.handleChartReady,
            dataZoom: DataZoomInside({ xAxisIndex: xAxisIndex }),
            // We must include data zoom in the toolbox for the zoom to work,
            // but we do not want to show the toolbox components.
            toolBox: ToolBox({}, {
                dataZoom: {
                    title: {
                        zoom: '',
                        back: '',
                    },
                    iconStyle: {
                        borderWidth: 0,
                        color: 'transparent',
                        opacity: 0,
                    },
                },
            }),
            onDataZoom: this.handleDataZoom,
        };
        return children(renderProps);
    };
    return BarChartZoom;
}(React.Component));
export default BarChartZoom;
//# sourceMappingURL=barChartZoom.jsx.map