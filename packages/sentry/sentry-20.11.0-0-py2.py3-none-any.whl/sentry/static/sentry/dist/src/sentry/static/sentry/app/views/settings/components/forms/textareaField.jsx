import React from 'react';
import omit from 'lodash/omit';
import InputField from 'app/views/settings/components/forms/inputField';
import Textarea from 'app/views/settings/components/forms/controls/textarea';
export default function TextareaField(props) {
    return (<InputField {...props} field={function (fieldProps) { return <Textarea {...omit(fieldProps, ['onKeyDown', 'children'])}/>; }}/>);
}
//# sourceMappingURL=textareaField.jsx.map