import { __extends } from "tslib";
import React from 'react';
import InputField from 'app/components/forms/inputField';
var TextareaField = /** @class */ (function (_super) {
    __extends(TextareaField, _super);
    function TextareaField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextareaField.prototype.getField = function () {
        return (<textarea id={this.getId()} className="form-control" value={this.state.value} disabled={this.props.disabled} required={this.props.required} placeholder={this.props.placeholder} onChange={this.onChange.bind(this)}/>);
    };
    return TextareaField;
}(InputField));
export default TextareaField;
//# sourceMappingURL=textareaField.jsx.map