import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import space from 'app/styles/space';
var getPadding = function (_a) {
    var disablePadding = _a.disablePadding, hasButtons = _a.hasButtons;
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  padding-right: ", ";\n"], ["\n  padding: ", " ", ";\n  padding-right: ", ";\n"])), hasButtons ? space(1) : space(2), disablePadding ? 0 : space(2), hasButtons ? space(1) : null);
};
var PanelHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  color: ", ";\n  font-size: 13px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  position: relative;\n  ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  color: ", ";\n  font-size: 13px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  position: relative;\n  ", ";\n"])), function (p) { return (p.lightText ? p.theme.gray300 : p.theme.gray400); }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.backgroundSecondary; }, getPadding);
PanelHeader.propTypes = {
    disablePadding: PropTypes.bool,
    hasButtons: PropTypes.bool,
    lightText: PropTypes.bool,
};
export default PanelHeader;
var templateObject_1, templateObject_2;
//# sourceMappingURL=panelHeader.jsx.map