import { __extends } from "tslib";
import React from 'react';
import { rectOfContent, clamp } from './utils';
var CursorGuideManagerContext = React.createContext({
    showCursorGuide: false,
    mouseLeft: void 0,
    traceViewMouseLeft: void 0,
    displayCursorGuide: function () { },
    hideCursorGuide: function () { },
});
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showCursorGuide: false,
            mouseLeft: void 0,
            traceViewMouseLeft: void 0,
        };
        _this.hasInteractiveLayer = function () { return !!_this.props.interactiveLayerRef.current; };
        _this.displayCursorGuide = function (mousePageX) {
            if (!_this.hasInteractiveLayer()) {
                return;
            }
            var _a = _this.props, trace = _a.trace, dragProps = _a.dragProps;
            var interactiveLayer = _this.props.interactiveLayerRef.current;
            var rect = rectOfContent(interactiveLayer);
            // duration of the entire trace in seconds
            var traceDuration = trace.traceEndTimestamp - trace.traceStartTimestamp;
            var viewStart = dragProps.viewWindowStart;
            var viewEnd = dragProps.viewWindowEnd;
            var viewStartTimestamp = trace.traceStartTimestamp + viewStart * traceDuration;
            var viewEndTimestamp = trace.traceEndTimestamp - (1 - viewEnd) * traceDuration;
            var viewDuration = viewEndTimestamp - viewStartTimestamp;
            // clamp mouseLeft to be within [0, 1]
            var mouseLeft = clamp((mousePageX - rect.x) / rect.width, 0, 1);
            var duration = mouseLeft * Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
            var startTimestamp = trace.traceStartTimestamp + duration;
            var start = (startTimestamp - viewStartTimestamp) / viewDuration;
            _this.setState({
                showCursorGuide: true,
                mouseLeft: mouseLeft,
                traceViewMouseLeft: start,
            });
        };
        _this.hideCursorGuide = function () {
            if (!_this.hasInteractiveLayer()) {
                return;
            }
            _this.setState({
                showCursorGuide: false,
                mouseLeft: void 0,
                traceViewMouseLeft: void 0,
            });
        };
        return _this;
    }
    Provider.prototype.render = function () {
        var childrenProps = {
            showCursorGuide: this.state.showCursorGuide,
            mouseLeft: this.state.mouseLeft,
            traceViewMouseLeft: this.state.traceViewMouseLeft,
            displayCursorGuide: this.displayCursorGuide,
            hideCursorGuide: this.hideCursorGuide,
        };
        return (<CursorGuideManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </CursorGuideManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = CursorGuideManagerContext.Consumer;
//# sourceMappingURL=cursorGuideHandler.jsx.map