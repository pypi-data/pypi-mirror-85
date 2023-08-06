import { __assign } from "tslib";
import React from 'react';
import InputField from 'app/views/settings/components/forms/inputField';
export default function TextField(props) {
    return <InputField {...props} type="text"/>;
}
TextField.propTypes = __assign({}, InputField.propTypes);
//# sourceMappingURL=textField.jsx.map