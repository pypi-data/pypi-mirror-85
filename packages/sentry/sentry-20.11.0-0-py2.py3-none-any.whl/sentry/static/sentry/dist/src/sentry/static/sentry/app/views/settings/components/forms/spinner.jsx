import { __makeTemplateObject } from "tslib";
import { keyframes } from '@emotion/core';
import styled from '@emotion/styled';
var spin = keyframes(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  0% {\n    transform: rotate(0deg);\n  }\n  100% {\n    transform: rotate(360deg);\n  }\n"], ["\n  0% {\n    transform: rotate(0deg);\n  }\n  100% {\n    transform: rotate(360deg);\n  }\n"])));
var Spinner = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  animation: ", " 0.4s linear infinite;\n  width: 18px;\n  height: 18px;\n  border-radius: 18px;\n  border-top: 2px solid ", ";\n  border-right: 2px solid ", ";\n  border-bottom: 2px solid ", ";\n  border-left: 2px solid ", ";\n  margin-left: auto;\n"], ["\n  animation: ", " 0.4s linear infinite;\n  width: 18px;\n  height: 18px;\n  border-radius: 18px;\n  border-top: 2px solid ", ";\n  border-right: 2px solid ", ";\n  border-bottom: 2px solid ", ";\n  border-left: 2px solid ", ";\n  margin-left: auto;\n"])), spin, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.purple300; });
export default Spinner;
var templateObject_1, templateObject_2;
//# sourceMappingURL=spinner.jsx.map