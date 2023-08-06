import { __extends, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { selectText } from 'app/utils/selectText';
import { isRenderFunc } from 'app/utils/isRenderFunc';
var AutoSelectText = /** @class */ (function (_super) {
    __extends(AutoSelectText, _super);
    function AutoSelectText() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.selectText = function () {
            if (!_this.el) {
                return;
            }
            selectText(_this.el);
        };
        _this.handleMount = function (el) {
            _this.el = el;
        };
        return _this;
    }
    AutoSelectText.prototype.render = function () {
        var _a = this.props, children = _a.children, className = _a.className, props = __rest(_a, ["children", "className"]);
        if (isRenderFunc(children)) {
            return children({
                doMount: this.handleMount,
                doSelect: this.selectText,
            });
        }
        // use an inner span here for the selection as otherwise the selectText
        // function will create a range that includes the entire part of the
        // div (including the div itself) which causes newlines to be selected
        // in chrome.
        return (<div {...props} onClick={this.selectText} className={classNames('auto-select-text', className)}>
        <span ref={this.handleMount}>{children}</span>
      </div>);
    };
    AutoSelectText.propTypes = {
        children: PropTypes.oneOfType([PropTypes.func, PropTypes.node]),
    };
    return AutoSelectText;
}(React.Component));
export default AutoSelectText;
//# sourceMappingURL=autoSelectText.jsx.map