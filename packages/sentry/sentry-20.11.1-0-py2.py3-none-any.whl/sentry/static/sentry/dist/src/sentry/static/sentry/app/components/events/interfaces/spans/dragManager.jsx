import { __extends } from "tslib";
import React from 'react';
import { rectOfContent, clamp, setBodyUserSelect } from './utils';
// we establish the minimum window size so that the window size of 0% is not possible
var MINIMUM_WINDOW_SIZE = 0.5 / 100; // 0.5% window size
var ViewHandleType;
(function (ViewHandleType) {
    ViewHandleType[ViewHandleType["Left"] = 0] = "Left";
    ViewHandleType[ViewHandleType["Right"] = 1] = "Right";
})(ViewHandleType || (ViewHandleType = {}));
var DragManager = /** @class */ (function (_super) {
    __extends(DragManager, _super);
    function DragManager() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // draggable handles
            isDragging: false,
            currentDraggingHandle: void 0,
            leftHandlePosition: 0,
            rightHandlePosition: 1,
            // window selection
            isWindowSelectionDragging: false,
            windowSelectionInitial: 0,
            windowSelectionCurrent: 0,
            windowSelectionSize: 0,
            // window sizes
            viewWindowStart: 0,
            viewWindowEnd: 1,
        };
        _this.previousUserSelect = null;
        _this.hasInteractiveLayer = function () { return !!_this.props.interactiveLayerRef.current; };
        _this.onDragStart = function (viewHandle) { return function (event) {
            var isDragging = _this.state.isDragging || _this.state.isWindowSelectionDragging;
            if (isDragging || event.type !== 'mousedown' || !_this.hasInteractiveLayer()) {
                return;
            }
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor outside the minimap
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor can drag outside of the
            // minimap
            window.addEventListener('mousemove', _this.onDragMove);
            window.addEventListener('mouseup', _this.onDragEnd);
            // indicate drag has begun
            _this.setState({
                isDragging: true,
                isWindowSelectionDragging: false,
                currentDraggingHandle: viewHandle,
            });
        }; };
        _this.onLeftHandleDragStart = function (event) {
            _this.onDragStart(ViewHandleType.Left)(event);
        };
        _this.onRightHandleDragStart = function (event) {
            _this.onDragStart(ViewHandleType.Right)(event);
        };
        _this.onDragMove = function (event) {
            if (!_this.state.isDragging ||
                event.type !== 'mousemove' ||
                !_this.hasInteractiveLayer()) {
                return;
            }
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            var rawMouseX = (event.pageX - rect.x) / rect.width;
            switch (_this.state.currentDraggingHandle) {
                case ViewHandleType.Left: {
                    var min = 0;
                    var max = _this.state.rightHandlePosition - MINIMUM_WINDOW_SIZE;
                    _this.setState({
                        // clamp rawMouseX to be within [0, rightHandlePosition - MINIMUM_WINDOW_SIZE]
                        leftHandlePosition: clamp(rawMouseX, min, max),
                    });
                    break;
                }
                case ViewHandleType.Right: {
                    var min = _this.state.leftHandlePosition + MINIMUM_WINDOW_SIZE;
                    var max = 1;
                    _this.setState({
                        // clamp rawMouseX to be within [leftHandlePosition + MINIMUM_WINDOW_SIZE, 1]
                        rightHandlePosition: clamp(rawMouseX, min, max),
                    });
                    break;
                }
                default: {
                    throw Error('this.state.currentDraggingHandle is undefined');
                }
            }
        };
        _this.onDragEnd = function (event) {
            if (!_this.state.isDragging ||
                event.type !== 'mouseup' ||
                !_this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onDragStart
            _this.cleanUpListeners();
            // restore body styles
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // indicate drag has ended
            switch (_this.state.currentDraggingHandle) {
                case ViewHandleType.Left: {
                    _this.setState(function (state) { return ({
                        isDragging: false,
                        currentDraggingHandle: void 0,
                        // commit leftHandlePosition to be viewWindowStart
                        viewWindowStart: state.leftHandlePosition,
                    }); });
                    return;
                }
                case ViewHandleType.Right: {
                    _this.setState(function (state) { return ({
                        isDragging: false,
                        currentDraggingHandle: void 0,
                        // commit rightHandlePosition to be viewWindowEnd
                        viewWindowEnd: state.rightHandlePosition,
                    }); });
                    return;
                }
                default: {
                    throw Error('this.state.currentDraggingHandle is undefined');
                }
            }
        };
        _this.onWindowSelectionDragStart = function (event) {
            var isDragging = _this.state.isDragging || _this.state.isWindowSelectionDragging;
            if (isDragging || event.type !== 'mousedown' || !_this.hasInteractiveLayer()) {
                return;
            }
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor outside the minimap
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor can drag outside of the
            // minimap
            window.addEventListener('mousemove', _this.onWindowSelectionDragMove);
            window.addEventListener('mouseup', _this.onWindowSelectionDragEnd);
            // indicate drag has begun
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            var rawMouseX = (event.pageX - rect.x) / rect.width;
            _this.setState({
                isDragging: false,
                isWindowSelectionDragging: true,
                windowSelectionInitial: rawMouseX,
                windowSelectionCurrent: rawMouseX,
            });
        };
        _this.onWindowSelectionDragMove = function (event) {
            if (!_this.state.isWindowSelectionDragging ||
                event.type !== 'mousemove' ||
                !_this.hasInteractiveLayer()) {
                return;
            }
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            var rawMouseX = (event.pageX - rect.x) / rect.width;
            var min = 0;
            var max = 1;
            // clamp rawMouseX to be within [0, 1]
            var windowSelectionCurrent = clamp(rawMouseX, min, max);
            var windowSelectionSize = clamp(Math.abs(_this.state.windowSelectionInitial - windowSelectionCurrent), min, max);
            _this.setState({
                windowSelectionCurrent: windowSelectionCurrent,
                windowSelectionSize: windowSelectionSize,
            });
        };
        _this.onWindowSelectionDragEnd = function (event) {
            if (!_this.state.isWindowSelectionDragging ||
                event.type !== 'mouseup' ||
                !_this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onWindowSelectionDragStart
            _this.cleanUpListeners();
            // restore body styles
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // indicate drag has ended
            _this.setState(function (state) {
                var viewWindowStart = Math.min(state.windowSelectionInitial, state.windowSelectionCurrent);
                var viewWindowEnd = Math.max(state.windowSelectionInitial, state.windowSelectionCurrent);
                // enforce minimum window size
                if (viewWindowEnd - viewWindowStart < MINIMUM_WINDOW_SIZE) {
                    viewWindowEnd = viewWindowStart + MINIMUM_WINDOW_SIZE;
                    if (viewWindowEnd > 1) {
                        viewWindowEnd = 1;
                        viewWindowStart = 1 - MINIMUM_WINDOW_SIZE;
                    }
                }
                return {
                    isWindowSelectionDragging: false,
                    windowSelectionInitial: 0,
                    windowSelectionCurrent: 0,
                    windowSelectionSize: 0,
                    leftHandlePosition: viewWindowStart,
                    rightHandlePosition: viewWindowEnd,
                    viewWindowStart: viewWindowStart,
                    viewWindowEnd: viewWindowEnd,
                };
            });
        };
        _this.cleanUpListeners = function () {
            if (_this.state.isDragging) {
                window.removeEventListener('mousemove', _this.onDragMove);
                window.removeEventListener('mouseup', _this.onDragEnd);
            }
            if (_this.state.isWindowSelectionDragging) {
                window.removeEventListener('mousemove', _this.onWindowSelectionDragMove);
                window.removeEventListener('mouseup', _this.onWindowSelectionDragEnd);
            }
        };
        return _this;
    }
    DragManager.prototype.componentWillUnmount = function () {
        this.cleanUpListeners();
    };
    DragManager.prototype.render = function () {
        var childrenProps = {
            isDragging: this.state.isDragging,
            // left handle
            onLeftHandleDragStart: this.onLeftHandleDragStart,
            leftHandlePosition: this.state.leftHandlePosition,
            // right handle
            onRightHandleDragStart: this.onRightHandleDragStart,
            rightHandlePosition: this.state.rightHandlePosition,
            // window selection
            isWindowSelectionDragging: this.state.isWindowSelectionDragging,
            windowSelectionInitial: this.state.windowSelectionInitial,
            windowSelectionCurrent: this.state.windowSelectionCurrent,
            windowSelectionSize: this.state.windowSelectionSize,
            onWindowSelectionDragStart: this.onWindowSelectionDragStart,
            // window sizes
            viewWindowStart: this.state.viewWindowStart,
            viewWindowEnd: this.state.viewWindowEnd,
        };
        return this.props.children(childrenProps);
    };
    return DragManager;
}(React.Component));
export default DragManager;
//# sourceMappingURL=dragManager.jsx.map