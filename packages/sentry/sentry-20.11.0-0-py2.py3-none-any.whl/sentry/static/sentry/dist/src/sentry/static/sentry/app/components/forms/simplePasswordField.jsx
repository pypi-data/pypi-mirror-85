import { __extends } from "tslib";
import InputField from 'app/components/forms/inputField';
var SimplePasswordField = /** @class */ (function (_super) {
    __extends(SimplePasswordField, _super);
    function SimplePasswordField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SimplePasswordField.prototype.getType = function () {
        return 'password';
    };
    return SimplePasswordField;
}(InputField));
export default SimplePasswordField;
//# sourceMappingURL=simplePasswordField.jsx.map