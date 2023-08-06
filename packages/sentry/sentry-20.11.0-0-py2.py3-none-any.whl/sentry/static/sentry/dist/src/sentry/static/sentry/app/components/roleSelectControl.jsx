import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import SelectControl from 'app/components/forms/selectControl';
var RoleSelector = function (_a) {
    var roles = _a.roles, disableUnallowed = _a.disableUnallowed, props = __rest(_a, ["roles", "disableUnallowed"]);
    return (<RoleSelectControl deprecatedSelectControl options={roles &&
        roles.map(function (r) { return ({
            value: r.id,
            label: r.name,
            disabled: disableUnallowed && !r.allowed,
        }); })} optionRenderer={function (option) {
        var _a = roles.find(function (r) { return r.id === option.value; }), name = _a.name, desc = _a.desc;
        return (<RoleItem>
          <h1>{name}</h1>
          <div>{desc}</div>
        </RoleItem>);
    }} {...props}/>);
};
var RoleSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .Select-menu-outer {\n    margin-top: ", ";\n    width: 350px;\n    border-radius: 4px;\n    overflow: hidden;\n    box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);\n  }\n\n  &.Select.is-focused.is-open > .Select-control {\n    border-radius: 4px;\n  }\n\n  .Select-option:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  .Select-menu-outer {\n    margin-top: ", ";\n    width: 350px;\n    border-radius: 4px;\n    overflow: hidden;\n    box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);\n  }\n\n  &.Select.is-focused.is-open > .Select-control {\n    border-radius: 4px;\n  }\n\n  .Select-option:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(1), function (p) { return p.theme.innerBorder; });
var RoleItem = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeSmall; }, space(0.25));
export default RoleSelector;
var templateObject_1, templateObject_2;
//# sourceMappingURL=roleSelectControl.jsx.map