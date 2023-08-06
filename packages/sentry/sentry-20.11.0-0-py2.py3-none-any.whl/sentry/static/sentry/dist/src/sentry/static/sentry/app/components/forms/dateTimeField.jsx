import { __extends } from "tslib";
import InputField from 'app/components/forms/inputField';
var DateTimeField = /** @class */ (function (_super) {
    __extends(DateTimeField, _super);
    function DateTimeField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DateTimeField.prototype.getType = function () {
        return 'datetime-local';
    };
    return DateTimeField;
}(InputField));
export default DateTimeField;
//# sourceMappingURL=dateTimeField.jsx.map