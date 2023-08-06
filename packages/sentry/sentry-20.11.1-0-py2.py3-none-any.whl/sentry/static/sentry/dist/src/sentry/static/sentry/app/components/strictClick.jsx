import { __extends, __read } from "tslib";
import React from 'react';
/**
 * Does not fire the onlick event if the mouse has moved outside of the
 * original click location upon release.
 *
 * <StrictClick onClick={this.onClickHandler}>
 *   <button>Some button</button>
 * </StrictClick>
 */
var StrictClick = /** @class */ (function (_super) {
    __extends(StrictClick, _super);
    function StrictClick() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleMouseDown = function (_a) {
            var screenX = _a.screenX, screenY = _a.screenY;
            return _this.setState({ startCoords: [screenX, screenY] });
        };
        _this.handleMouseClick = function (evt) {
            if (!_this.props.onClick) {
                return;
            }
            // Click happens if mouse down/up in same element - click will not fire if
            // either initial mouse down OR final mouse up occurs in different element
            var _a = __read(_this.state.startCoords, 2), x = _a[0], y = _a[1];
            var deltaX = Math.abs(evt.screenX - x);
            var deltaY = Math.abs(evt.screenY - y);
            // If mouse hasn't moved more than 10 pixels in either Y or X direction,
            // fire onClick
            if (deltaX < StrictClick.MAX_DELTA_X && deltaY < StrictClick.MAX_DELTA_Y) {
                _this.props.onClick(evt);
            }
            _this.setState({ startCoords: undefined });
        };
        return _this;
    }
    StrictClick.prototype.render = function () {
        // Bail out early if there is no onClick handler
        if (!this.props.onClick) {
            return this.props.children;
        }
        return React.cloneElement(this.props.children, {
            onMouseDown: this.handleMouseDown,
            onClick: this.handleMouseClick,
        });
    };
    StrictClick.MAX_DELTA_X = 10;
    StrictClick.MAX_DELTA_Y = 10;
    return StrictClick;
}(React.PureComponent));
export default StrictClick;
//# sourceMappingURL=strictClick.jsx.map