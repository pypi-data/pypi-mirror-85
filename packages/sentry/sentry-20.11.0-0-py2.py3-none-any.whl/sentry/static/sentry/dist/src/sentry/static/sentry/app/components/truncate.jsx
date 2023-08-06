import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
var Truncate = /** @class */ (function (_super) {
    __extends(Truncate, _super);
    function Truncate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: false,
        };
        _this.onFocus = function () {
            var _a = _this.props, value = _a.value, maxLength = _a.maxLength;
            if (value.length <= maxLength) {
                return;
            }
            _this.setState({ isExpanded: true });
        };
        _this.onBlur = function () {
            if (_this.state.isExpanded) {
                _this.setState({ isExpanded: false });
            }
        };
        return _this;
    }
    Truncate.prototype.render = function () {
        var _a = this.props, leftTrim = _a.leftTrim, maxLength = _a.maxLength, value = _a.value;
        var isTruncated = value.length > maxLength;
        var shortValue = '';
        if (isTruncated) {
            if (leftTrim) {
                shortValue = (<span>… {value.slice(value.length - (maxLength - 4), value.length)}</span>);
            }
            else {
                shortValue = <span>{value.slice(0, maxLength - 4)} …</span>;
            }
        }
        else {
            shortValue = value;
        }
        var className = this.props.className || '';
        className += ' truncated';
        if (this.state.isExpanded) {
            className += ' expanded';
        }
        return (<span className={className} onMouseOver={this.onFocus} onMouseOut={this.onBlur} onFocus={this.onFocus} onBlur={this.onBlur}>
        <span className="short-value">{shortValue}</span>
        {isTruncated && <span className="full-value">{value}</span>}
      </span>);
    };
    Truncate.propTypes = {
        value: PropTypes.string.isRequired,
        leftTrim: PropTypes.bool,
        maxLength: PropTypes.number,
    };
    Truncate.defaultProps = {
        maxLength: 50,
        leftTrim: false,
    };
    return Truncate;
}(React.Component));
export default Truncate;
//# sourceMappingURL=truncate.jsx.map