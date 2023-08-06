import { __extends } from "tslib";
import InputField from 'app/components/forms/inputField';
var EmailField = /** @class */ (function (_super) {
    __extends(EmailField, _super);
    function EmailField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EmailField.prototype.getType = function () {
        return 'email';
    };
    return EmailField;
}(InputField));
export default EmailField;
//# sourceMappingURL=emailField.jsx.map