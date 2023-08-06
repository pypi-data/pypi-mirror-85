import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import InputField from 'app/components/forms/inputField';
var NumberField = /** @class */ (function (_super) {
    __extends(NumberField, _super);
    function NumberField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NumberField.prototype.coerceValue = function (value) {
        var intValue = parseInt(value, 10);
        // return previous value if new value is NaN, otherwise, will get recursive error
        var isNewCoercedNaN = isNaN(intValue);
        if (!isNewCoercedNaN) {
            return intValue;
        }
        return '';
    };
    NumberField.prototype.getType = function () {
        return 'number';
    };
    NumberField.prototype.getAttributes = function () {
        return {
            min: this.props.min || undefined,
            max: this.props.max || undefined,
        };
    };
    NumberField.propTypes = __assign(__assign({}, InputField.propTypes), { min: PropTypes.number, max: PropTypes.number });
    return NumberField;
}(InputField));
export default NumberField;
//# sourceMappingURL=numberField.jsx.map