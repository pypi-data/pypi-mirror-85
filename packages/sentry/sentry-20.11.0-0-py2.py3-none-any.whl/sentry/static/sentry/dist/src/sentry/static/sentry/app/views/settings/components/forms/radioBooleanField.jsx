import React from 'react';
import omit from 'lodash/omit';
import InputField from './inputField';
import RadioBoolean from './controls/radioBoolean';
export default function RadioBooleanField(props) {
    return (<InputField {...props} field={function (fieldProps) { return (<RadioBoolean {...omit(fieldProps, ['onKeyDown', 'children'])}/>); }}/>);
}
//# sourceMappingURL=radioBooleanField.jsx.map