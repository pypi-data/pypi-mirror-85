import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import { inputStyles } from 'app/styles/input';
/**
 * Do not forward required to `input` to avoid default browser behavior
 */
var Input = styled('input', {
    shouldForwardProp: function (prop) { return isPropValid(prop) && prop !== 'required'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), inputStyles);
// Cast type to avoid exporting theme
export default Input;
var templateObject_1;
//# sourceMappingURL=input.jsx.map