import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Menu from './menu';
var DropdownAutoComplete = function (_a) {
    var _b = _a.allowActorToggle, allowActorToggle = _b === void 0 ? false : _b, children = _a.children, props = __rest(_a, ["allowActorToggle", "children"]);
    return (<Menu {...props}>
    {function (renderProps) {
        var isOpen = renderProps.isOpen, actions = renderProps.actions, getActorProps = renderProps.getActorProps;
        // Don't pass `onClick` from `getActorProps`
        var _a = getActorProps(), _onClick = _a.onClick, actorProps = __rest(_a, ["onClick"]);
        return (<Actor isOpen={isOpen} role="button" tabIndex={0} onClick={isOpen && allowActorToggle ? actions.close : actions.open} {...actorProps}>
          {children(renderProps)}
        </Actor>);
    }}
  </Menu>);
};
var Actor = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  /* This is needed to be able to cover dropdown menu so that it looks like one unit */\n  ", ";\n"], ["\n  position: relative;\n  width: 100%;\n  /* This is needed to be able to cover dropdown menu so that it looks like one unit */\n  ", ";\n"])), function (p) { return p.isOpen && "z-index: " + p.theme.zIndex.dropdownAutocomplete.actor; });
export default DropdownAutoComplete;
var templateObject_1;
//# sourceMappingURL=index.jsx.map