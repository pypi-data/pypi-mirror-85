import { __assign, __extends } from "tslib";
import $ from 'jquery';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import InputField from 'app/components/forms/inputField';
var RangeField = /** @class */ (function (_super) {
    __extends(RangeField, _super);
    function RangeField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RangeField.prototype.componentDidMount = function () {
        _super.prototype.componentDidMount.call(this);
        this.attachSlider();
    };
    RangeField.prototype.componentWillUnmount = function () {
        this.removeSlider();
        _super.prototype.componentWillUnmount.call(this);
    };
    RangeField.prototype.attachSlider = function () {
        var _this = this;
        var $value = $('<span class="value" />');
        var suffixClassNames = '';
        if (this.props.disabled) {
            suffixClassNames += ' disabled';
        }
        $(
        // eslint-disable-next-line react/no-find-dom-node
        ReactDOM.findDOMNode(this.refs.input))
            .on('slider:ready', function (_e, data) {
            var value = parseInt(data.value, 10);
            $value.appendTo(data.el);
            $value.html(_this.props.formatLabel(value));
        })
            .on('slider:changed', function (_e, data) {
            var value = parseInt(data.value, 10);
            $value.html(_this.props.formatLabel(value));
            _this.setValue(value);
        }).simpleSlider({
            value: this.props.defaultValue || this.props.value,
            range: [this.props.min, this.props.max],
            step: this.props.step,
            snap: this.props.snap,
            allowedValues: this.props.allowedValues,
            classSuffix: suffixClassNames,
        });
    };
    RangeField.prototype.removeSlider = function () {
        // TODO(dcramer): it seems we cant actually implement this with the current slider
        // implementation
    };
    RangeField.prototype.getAttributes = function () {
        return {
            min: this.props.min,
            max: this.props.max,
            step: this.props.step,
        };
    };
    RangeField.prototype.getType = function () {
        return 'range';
    };
    RangeField.formatMinutes = function (value) {
        value = value / 60;
        return value + " minute" + (value !== 1 ? 's' : '');
    };
    RangeField.propTypes = __assign(__assign({}, InputField.propTypes), { min: PropTypes.number, max: PropTypes.number, step: PropTypes.number, snap: PropTypes.bool, allowedValues: PropTypes.arrayOf(PropTypes.number) });
    RangeField.defaultProps = __assign(__assign({}, InputField.defaultProps), { formatLabel: function (value) { return value; }, min: 0, max: 100, step: 1, snap: true, allowedValues: null });
    return RangeField;
}(InputField));
export default RangeField;
//# sourceMappingURL=rangeField.jsx.map