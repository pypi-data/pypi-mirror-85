import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
var FlowLayout = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  flex-direction: ", ";\n  justify-content: ", ";\n  overflow: ", ";\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  flex-direction: ", ";\n  justify-content: ", ";\n  overflow: ", ";\n"])), function (p) { return (p.vertical ? 'column' : null); }, function (p) { return (p.center ? 'center' : null); }, function (p) { return (p.truncate ? 'hidden' : null); });
FlowLayout.propTypes = {
    center: PropTypes.bool,
    vertical: PropTypes.bool,
    truncate: PropTypes.bool,
};
FlowLayout.defaultProps = {
    truncate: true,
};
export default FlowLayout;
var templateObject_1;
//# sourceMappingURL=flowLayout.jsx.map