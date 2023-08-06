import { __extends } from "tslib";
import React from 'react';
import { rectOfContent, clamp, toPercent, setBodyUserSelect, } from './utils';
// divider handle is positioned at 50% width from the left-hand side
var DEFAULT_DIVIDER_POSITION = 0.4;
var selectRefs = function (refs, transform) {
    refs.forEach(function (ref) {
        if (ref.current) {
            transform(ref.current);
        }
    });
};
var DividerManagerContext = React.createContext({
    dividerPosition: DEFAULT_DIVIDER_POSITION,
    onDragStart: function () { },
    setHover: function () { },
    addDividerLineRef: function () { return React.createRef(); },
    addGhostDividerLineRef: function () { return React.createRef(); },
});
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dividerPosition: DEFAULT_DIVIDER_POSITION,
        };
        _this.previousUserSelect = null;
        _this.dividerHandlePosition = DEFAULT_DIVIDER_POSITION;
        _this.isDragging = false;
        _this.dividerLineRefs = [];
        _this.ghostDividerLineRefs = [];
        _this.hasInteractiveLayer = function () { return !!_this.props.interactiveLayerRef.current; };
        _this.addDividerLineRef = function () {
            var ref = React.createRef();
            _this.dividerLineRefs.push(ref);
            return ref;
        };
        _this.addGhostDividerLineRef = function () {
            var ref = React.createRef();
            _this.ghostDividerLineRefs.push(ref);
            return ref;
        };
        _this.setHover = function (nextHover) {
            if (_this.isDragging) {
                return;
            }
            selectRefs(_this.dividerLineRefs, function (dividerDOM) {
                if (nextHover) {
                    dividerDOM.classList.add('hovering');
                    return;
                }
                dividerDOM.classList.remove('hovering');
            });
        };
        _this.onDragStart = function (event) {
            if (_this.isDragging || event.type !== 'mousedown' || !_this.hasInteractiveLayer()) {
                return;
            }
            event.stopPropagation();
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor inside the minimap
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor does not select text during a drag
            window.addEventListener('mousemove', _this.onDragMove);
            window.addEventListener('mouseup', _this.onDragEnd);
            _this.setHover(true);
            // indicate drag has begun
            _this.isDragging = true;
            selectRefs(_this.dividerLineRefs, function (dividerDOM) {
                dividerDOM.style.backgroundColor = 'rgba(73,80,87,0.75)';
                dividerDOM.style.cursor = 'col-resize';
            });
            selectRefs(_this.ghostDividerLineRefs, function (dividerDOM) {
                dividerDOM.style.cursor = 'col-resize';
                var parentNode = dividerDOM.parentNode;
                if (!parentNode) {
                    return;
                }
                var container = parentNode;
                container.style.display = 'block';
            });
        };
        _this.onDragMove = function (event) {
            if (!_this.isDragging || event.type !== 'mousemove' || !_this.hasInteractiveLayer()) {
                return;
            }
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            // mouse x-coordinate relative to the interactive layer's left side
            var rawMouseX = (event.pageX - rect.x) / rect.width;
            var min = 0;
            var max = 1;
            // clamp rawMouseX to be within [0, 1]
            _this.dividerHandlePosition = clamp(rawMouseX, min, max);
            var dividerHandlePositionString = toPercent(_this.dividerHandlePosition);
            selectRefs(_this.ghostDividerLineRefs, function (dividerDOM) {
                var parentNode = dividerDOM.parentNode;
                if (!parentNode) {
                    return;
                }
                var container = parentNode;
                container.style.width = "calc(" + dividerHandlePositionString + " + 0.5px)";
            });
        };
        _this.onDragEnd = function (event) {
            if (!_this.isDragging || event.type !== 'mouseup' || !_this.hasInteractiveLayer()) {
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
            _this.isDragging = false;
            _this.setHover(false);
            selectRefs(_this.dividerLineRefs, function (dividerDOM) {
                dividerDOM.style.backgroundColor = '';
                dividerDOM.style.cursor = '';
            });
            selectRefs(_this.ghostDividerLineRefs, function (dividerDOM) {
                dividerDOM.style.cursor = '';
                var parentNode = dividerDOM.parentNode;
                if (!parentNode) {
                    return;
                }
                var container = parentNode;
                container.style.display = 'none';
            });
            _this.setState({
                // commit dividerHandlePosition to be dividerPosition
                dividerPosition: _this.dividerHandlePosition,
            });
        };
        _this.cleanUpListeners = function () {
            if (_this.isDragging) {
                // we only remove listeners during a drag
                window.removeEventListener('mousemove', _this.onDragMove);
                window.removeEventListener('mouseup', _this.onDragEnd);
            }
        };
        return _this;
    }
    Provider.prototype.componentWillUnmount = function () {
        this.cleanUpListeners();
    };
    Provider.prototype.render = function () {
        var childrenProps = {
            dividerPosition: this.state.dividerPosition,
            setHover: this.setHover,
            onDragStart: this.onDragStart,
            addDividerLineRef: this.addDividerLineRef,
            addGhostDividerLineRef: this.addGhostDividerLineRef,
        };
        // NOTE: <DividerManagerContext.Provider /> will not re-render its children
        // - if the `value` prop changes, and
        // - if the `children` prop stays the same
        //
        // Thus, only <DividerManagerContext.Consumer /> components will re-render.
        // This is an optimization for when childrenProps changes, but this.props does not change.
        //
        // We prefer to minimize the amount of top-down prop drilling from this component
        // to the respective divider components.
        return (<DividerManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </DividerManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = DividerManagerContext.Consumer;
//# sourceMappingURL=dividerHandlerManager.jsx.map