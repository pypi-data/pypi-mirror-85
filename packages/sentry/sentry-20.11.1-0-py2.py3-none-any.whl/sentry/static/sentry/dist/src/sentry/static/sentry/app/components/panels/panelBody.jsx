import { __makeTemplateObject, __rest } from "tslib";
import { Flex } from 'reflexbox';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import textStyles from 'app/styles/text';
var PanelBody = function (_a) {
    var flexible = _a.flexible, forwardRef = _a.forwardRef, props = __rest(_a, ["flexible", "forwardRef"]);
    return (<FlexBox {...props} ref={forwardRef} {...(flexible ? { flexDirection: 'column' } : null)}/>);
};
PanelBody.propTypes = {
    flexible: PropTypes.bool,
    withPadding: PropTypes.bool,
};
PanelBody.defaultProps = {
    flexible: false,
    withPadding: false,
};
var FlexBox = styled(Flex)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  ", ";\n  ", ";\n"], ["\n  ", ";\n  ", ";\n  ", ";\n"])), textStyles, function (p) { return !p.flexible && 'display: block'; }, function (p) { return p.withPadding && "padding: " + space(2); });
export default PanelBody;
var templateObject_1;
//# sourceMappingURL=panelBody.jsx.map