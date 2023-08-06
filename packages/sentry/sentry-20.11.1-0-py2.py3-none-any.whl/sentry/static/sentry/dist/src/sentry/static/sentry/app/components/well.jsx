import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
var Well = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  box-shadow: none;\n  background: ", ";\n  padding: ", ";\n  margin-bottom: 20px;\n  border-radius: 3px;\n  ", ";\n"], ["\n  border: 1px solid ", ";\n  box-shadow: none;\n  background: ", ";\n  padding: ", ";\n  margin-bottom: 20px;\n  border-radius: 3px;\n  ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return (p.hasImage ? '80px 30px' : '15px 20px'); }, function (p) { return p.centered && 'text-align: center'; });
Well.propTypes = {
    hasImage: PropTypes.bool,
    centered: PropTypes.bool,
};
export default Well;
var templateObject_1;
//# sourceMappingURL=well.jsx.map