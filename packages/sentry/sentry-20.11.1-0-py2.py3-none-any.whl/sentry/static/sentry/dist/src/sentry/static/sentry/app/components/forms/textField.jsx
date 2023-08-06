import { __extends } from "tslib";
import PropTypes from 'prop-types';
import InputField from 'app/components/forms/inputField';
var TextField = /** @class */ (function (_super) {
    __extends(TextField, _super);
    function TextField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextField.prototype.getAttributes = function () {
        return {
            spellCheck: this.props.spellCheck,
        };
    };
    TextField.prototype.getType = function () {
        return 'text';
    };
    TextField.propTypes = {
        spellCheck: PropTypes.string,
    }; // TODO(ts): remove when proptypes are no longer required, some views don't implement all required proptypes of underlying InputField.
    return TextField;
}(InputField));
export default TextField;
//# sourceMappingURL=textField.jsx.map