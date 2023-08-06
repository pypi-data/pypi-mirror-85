import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
/**
 * This creates a bordered box that has a left pointing arrow
 * on the left-side at the top.
 */
var ActivityBubble = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  position: relative;\n  width: 100%; /* this is used in Incidents Details - a chart can cause overflow and won't resize properly */\n\n  &:before {\n    display: block;\n    content: '';\n    width: 0;\n    height: 0;\n    border-top: 7px solid transparent;\n    border-bottom: 7px solid transparent;\n    border-right: 7px solid ", ";\n    position: absolute;\n    left: -7px;\n    top: 12px;\n  }\n\n  &:after {\n    display: block;\n    content: '';\n    width: 0;\n    height: 0;\n    border-top: 6px solid transparent;\n    border-bottom: 6px solid transparent;\n    border-right: 6px solid ", ";\n    position: absolute;\n    left: -6px;\n    top: 13px;\n  }\n"], ["\n  flex: 1;\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  position: relative;\n  width: 100%; /* this is used in Incidents Details - a chart can cause overflow and won't resize properly */\n\n  &:before {\n    display: block;\n    content: '';\n    width: 0;\n    height: 0;\n    border-top: 7px solid transparent;\n    border-bottom: 7px solid transparent;\n    border-right: 7px solid ", ";\n    position: absolute;\n    left: -7px;\n    top: 12px;\n  }\n\n  &:after {\n    display: block;\n    content: '';\n    width: 0;\n    height: 0;\n    border-top: 6px solid transparent;\n    border-bottom: 6px solid transparent;\n    border-right: 6px solid ", ";\n    position: absolute;\n    left: -6px;\n    top: 13px;\n  }\n"])), function (p) { return p.backgroundColor || p.theme.background; }, function (p) { return p.borderColor || p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.borderColor || p.theme.border; }, function (p) { return p.backgroundColor || p.theme.background; });
ActivityBubble.propTypes = {
    backgroundColor: PropTypes.string,
    borderColor: PropTypes.string,
};
export default ActivityBubble;
var templateObject_1;
//# sourceMappingURL=bubble.jsx.map