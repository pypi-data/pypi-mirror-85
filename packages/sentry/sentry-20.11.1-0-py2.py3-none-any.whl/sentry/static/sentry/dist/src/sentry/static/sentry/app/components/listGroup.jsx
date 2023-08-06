import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
var ListGroupItem = styled('li')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: block;\n  min-height: 36px;\n  border: 1px solid ", ";\n\n  padding: ", " ", ";\n\n  margin-bottom: -1px;\n  ", "\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    border-top-right-radius: ", ";\n  }\n  &:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"], ["\n  position: relative;\n  display: block;\n  min-height: 36px;\n  border: 1px solid ", ";\n\n  padding: ", " ", ";\n\n  margin-bottom: -1px;\n  ", "\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    border-top-right-radius: ", ";\n  }\n  &:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"])), function (p) { return p.theme.border; }, space(0.5), space(1.5), function (p) { return (p.centered ? 'text-align: center;' : ''); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ListGroup = styled('ul')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);\n  background: ", ";\n  padding: 0;\n  margin: 0;\n\n  ", "\n"], ["\n  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);\n  background: ", ";\n  padding: 0;\n  margin: 0;\n\n  ",
    "\n"])), function (p) { return p.theme.background; }, function (p) {
    return p.striped
        ? "\n    & > li:nth-child(odd) {\n      background: " + p.theme.backgroundSecondary + ";\n    }\n  "
        : '';
});
export { ListGroup, ListGroupItem };
var templateObject_1, templateObject_2;
//# sourceMappingURL=listGroup.jsx.map