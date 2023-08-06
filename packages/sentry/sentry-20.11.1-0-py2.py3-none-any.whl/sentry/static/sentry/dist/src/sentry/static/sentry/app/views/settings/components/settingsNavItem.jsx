import { __makeTemplateObject, __rest } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import Badge from 'app/components/badge';
import HookOrDefault from 'app/components/hookOrDefault';
import FeatureBadge from 'app/components/featureBadge';
var SettingsNavItem = function (_a) {
    var badge = _a.badge, label = _a.label, index = _a.index, id = _a.id, props = __rest(_a, ["badge", "label", "index", "id"]);
    var LabelHook = HookOrDefault({
        hookName: 'sidebar:item-label',
        defaultComponent: function (_a) {
            var children = _a.children;
            return <React.Fragment>{children}</React.Fragment>;
        },
    });
    var renderedBadge = badge === 'new' ? <FeatureBadge type="new"/> : <Badge text={badge}/>;
    return (<StyledNavItem onlyActiveOnIndex={index} activeClassName="active" {...props}>
      <LabelHook id={id}>{label}</LabelHook>

      {badge ? renderedBadge : null}
    </StyledNavItem>);
};
var StyledNavItem = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  line-height: 30px;\n  position: relative;\n\n  &.active {\n    color: ", ";\n\n    &:before {\n      background: ", ";\n    }\n  }\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n    outline: none;\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: #f2eff5;\n    padding: 0 15px;\n    margin: 0 -15px;\n    border-radius: 3px;\n\n    &:before {\n      left: -15px;\n    }\n  }\n\n  &:before {\n    position: absolute;\n    content: '';\n    display: block;\n    top: 4px;\n    left: -30px;\n    height: 20px;\n    width: 4px;\n    background: transparent;\n    border-radius: 0 2px 2px 0;\n  }\n"], ["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  line-height: 30px;\n  position: relative;\n\n  &.active {\n    color: ", ";\n\n    &:before {\n      background: ", ";\n    }\n  }\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n    outline: none;\n  }\n\n  &.focus-visible {\n    outline: none;\n    background: #f2eff5;\n    padding: 0 15px;\n    margin: 0 -15px;\n    border-radius: 3px;\n\n    &:before {\n      left: -15px;\n    }\n  }\n\n  &:before {\n    position: absolute;\n    content: '';\n    display: block;\n    top: 4px;\n    left: -30px;\n    height: 20px;\n    width: 4px;\n    background: transparent;\n    border-radius: 0 2px 2px 0;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.textColor; });
export default SettingsNavItem;
var templateObject_1;
//# sourceMappingURL=settingsNavItem.jsx.map