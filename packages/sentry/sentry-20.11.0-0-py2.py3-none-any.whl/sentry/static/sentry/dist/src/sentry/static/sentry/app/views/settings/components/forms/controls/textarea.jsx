import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import TextareaAutosize from 'react-autosize-textarea';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import { inputStyles } from 'app/styles/input';
var TextAreaControl = React.forwardRef(function TextAreaControl(_a, ref) {
    var autosize = _a.autosize, rows = _a.rows, p = __rest(_a, ["autosize", "rows"]);
    return autosize ? (<TextareaAutosize async ref={ref} rows={rows ? rows : 2} {...p}/>) : (<textarea ref={ref} {...p}/>);
});
TextAreaControl.displayName = 'TextAreaControl';
TextAreaControl.propTypes = {
    autosize: PropTypes.bool,
    rows: PropTypes.number,
    monospace: PropTypes.bool,
};
var propFilter = function (p) {
    return ['autosize', 'rows', 'maxRows'].includes(p) || isPropValid(p);
};
var TextArea = styled(TextAreaControl, { shouldForwardProp: propFilter })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  line-height: 1.3em;\n"], ["\n  ", ";\n  line-height: 1.3em;\n"])), inputStyles);
export default TextArea;
var templateObject_1;
//# sourceMappingURL=textarea.jsx.map