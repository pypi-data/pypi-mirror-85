import { __assign, __extends, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import omit from 'lodash/omit';
import FormField from 'app/views/settings/components/forms/formField';
import Input from 'app/views/settings/components/forms/controls/input';
var InputField = /** @class */ (function (_super) {
    __extends(InputField, _super);
    function InputField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InputField.prototype.render = function () {
        var _a = this.props, className = _a.className, field = _a.field;
        return (<FormField className={className} {...this.props}>
        {function (formFieldProps) { return field && field(omit(formFieldProps, 'children')); }}
      </FormField>);
    };
    InputField.propTypes = __assign(__assign({}, FormField.propTypes), { field: PropTypes.func });
    InputField.defaultProps = {
        field: function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, props = __rest(_a, ["onChange", "onBlur", "onKeyDown"]);
            return (<Input {...props} onBlur={function (e) { return onBlur(e.target.value, e); }} onKeyDown={function (e) { return onKeyDown(e.target.value, e); }} onChange={function (e) { return onChange(e.target.value, e); }}/>);
        },
    };
    return InputField;
}(React.Component));
export default InputField;
//# sourceMappingURL=inputField.jsx.map