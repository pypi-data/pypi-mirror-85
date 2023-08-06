import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import space from 'app/styles/space';
var defaultProps = {
    shape: 'rect',
    bottomGutter: 0,
    width: '100%',
    height: '60px',
};
var Placeholder = styled(function (props) {
    var className = props.className, children = props.children, error = props.error;
    return (<div data-test-id="loading-placeholder" className={className}>
      {error || children}
    </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ", "\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ",
    "\n"])), function (p) { return (p.error ? p.theme.red100 : p.theme.backgroundSecondary); }, function (p) { return p.error && "color: " + p.theme.red200 + ";"; }, function (p) { return p.width; }, function (p) { return p.height; }, function (p) { return (p.shape === 'circle' ? 'border-radius: 100%;' : ''); }, function (p) {
    return typeof p.bottomGutter === 'number' && p.bottomGutter > 0
        ? "margin-bottom: " + space(p.bottomGutter) + ";"
        : '';
});
Placeholder.defaultProps = defaultProps;
Placeholder.propTypes = {
    shape: PropTypes.oneOf(['rect', 'circle']),
    width: PropTypes.string,
    height: PropTypes.string,
    bottomGutter: PropTypes.number,
};
export default Placeholder;
var templateObject_1;
//# sourceMappingURL=placeholder.jsx.map