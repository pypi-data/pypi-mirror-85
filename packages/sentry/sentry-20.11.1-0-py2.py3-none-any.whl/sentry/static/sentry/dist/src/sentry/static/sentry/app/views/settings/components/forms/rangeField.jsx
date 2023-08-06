import { __rest } from "tslib";
import React from 'react';
import InputField from 'app/views/settings/components/forms/inputField';
import RangeSlider from 'app/views/settings/components/forms/controls/rangeSlider';
function onChange(fieldOnChange, value, e) {
    fieldOnChange(value, e);
}
function defaultFormatMessageValue(value, props) {
    return (typeof props.formatLabel === 'function' && props.formatLabel(value)) || value;
}
export default function RangeField(_a) {
    var _b = _a.formatMessageValue, formatMessageValue = _b === void 0 ? defaultFormatMessageValue : _b, otherProps = __rest(_a, ["formatMessageValue"]);
    if (typeof otherProps.disabled === 'function') {
        otherProps.disabled = otherProps.disabled(otherProps);
    }
    var props = Object.assign(otherProps, { formatMessageValue: formatMessageValue });
    return (<InputField {...props} field={function (_a) {
        var fieldOnChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, fieldProps = __rest(_a, ["onChange", "onBlur", "value"]);
        return (<RangeSlider {...fieldProps} value={value} onBlur={onBlur} onChange={function (val, event) { return onChange(fieldOnChange, val, event); }}/>);
    }}/>);
}
//# sourceMappingURL=rangeField.jsx.map