import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var PageHeading = styled('h1')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: ", ";\n  font-weight: normal;\n  margin: 0;\n  margin-bottom: ", ";\n  margin-top: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: ", ";\n  font-weight: normal;\n  margin: 0;\n  margin-bottom: ", ";\n  margin-top: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.withMargins && space(3); }, function (p) { return p.withMargins && space(1); });
PageHeading.propTypes = {
    children: PropTypes.node,
    className: PropTypes.string,
    withMargins: PropTypes.bool,
};
export default PageHeading;
var templateObject_1;
//# sourceMappingURL=pageHeading.jsx.map