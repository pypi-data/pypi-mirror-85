import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import FormField from 'app/components/forms/formField';
var InputField = /** @class */ (function (_super) {
    __extends(InputField, _super);
    function InputField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputField.prototype.getField = function () {
        return (<input id={this.getId()} //TODO(Priscila): check the reason behind this. We are getting warnings if we have 2 or more fields with the same name, for instance in the DATA PRIVACY RULES
         type={this.getType()} className="form-control" autoComplete={this.props.autoComplete} placeholder={this.props.placeholder} onChange={this.onChange} disabled={this.props.disabled} name={this.props.name} required={this.props.required} value={this.state.value} //can't pass in boolean here
         style={this.props.inputStyle} onBlur={this.props.onBlur} onFocus={this.props.onFocus} onKeyPress={this.props.onKeyPress} onKeyDown={this.props.onKeyDown}/>);
    };
    InputField.prototype.getClassName = function () {
        return 'control-group';
    };
    InputField.prototype.getType = function () {
        throw new Error('Must be implemented by child.');
    };
    InputField.propTypes = __assign(__assign({}, FormField.propTypes), { placeholder: PropTypes.string });
    return InputField;
}(FormField));
export default InputField;
//# sourceMappingURL=inputField.jsx.map