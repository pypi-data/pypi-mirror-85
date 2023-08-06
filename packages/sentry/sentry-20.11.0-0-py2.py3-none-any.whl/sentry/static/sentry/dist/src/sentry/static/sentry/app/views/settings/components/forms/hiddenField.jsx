import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import InputField from './inputField';
export default function HiddenField(props) {
    return <HiddenInputField {...props} type="hidden"/>;
}
var HiddenInputField = styled(InputField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: none;\n"], ["\n  display: none;\n"])));
var templateObject_1;
//# sourceMappingURL=hiddenField.jsx.map