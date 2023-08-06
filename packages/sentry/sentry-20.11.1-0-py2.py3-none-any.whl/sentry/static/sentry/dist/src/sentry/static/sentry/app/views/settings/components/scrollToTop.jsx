import { __extends } from "tslib";
import React from 'react';
import { callIfFunction } from 'app/utils/callIfFunction';
var ScrollToTop = /** @class */ (function (_super) {
    __extends(ScrollToTop, _super);
    function ScrollToTop() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ScrollToTop.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, disable = _a.disable, location = _a.location;
        var shouldDisable = callIfFunction(disable, location, prevProps.location);
        if (!shouldDisable && this.props.location !== prevProps.location) {
            window.scrollTo(0, 0);
        }
    };
    ScrollToTop.prototype.render = function () {
        return this.props.children;
    };
    return ScrollToTop;
}(React.Component));
export default ScrollToTop;
//# sourceMappingURL=scrollToTop.jsx.map