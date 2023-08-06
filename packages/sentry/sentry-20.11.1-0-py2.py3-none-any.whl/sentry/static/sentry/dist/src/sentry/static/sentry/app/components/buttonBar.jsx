import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import space from 'app/styles/space';
function ButtonBar(_a) {
    var children = _a.children, className = _a.className, active = _a.active, _b = _a.merged, merged = _b === void 0 ? false : _b, _c = _a.gap, gap = _c === void 0 ? 0 : _c;
    var shouldCheckActive = typeof active !== 'undefined';
    return (<ButtonGrid merged={merged} gap={gap} className={className}>
      {!shouldCheckActive
        ? children
        : React.Children.map(children, function (child) {
            if (!React.isValidElement(child)) {
                return child;
            }
            var childProps = child.props, childWithoutProps = __rest(child, ["props"]);
            // We do not want to pass `barId` to <Button>`
            var barId = childProps.barId, props = __rest(childProps, ["barId"]);
            var isActive = active === barId;
            // This ["primary"] could be customizable with a prop,
            // but let's just enforce one "active" type for now
            var priority = isActive ? 'primary' : childProps.priority || 'default';
            return React.cloneElement(childWithoutProps, __assign(__assign({}, props), { className: classNames(className, { active: isActive }), priority: priority }));
        })}
    </ButtonGrid>);
}
var ButtonGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ", "\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ",
    "\n"])), function (p) { return space(p.gap); }, function (p) {
    return p.merged &&
        "\n    & > button,\n    & > a {\n      position: relative;\n    }\n\n    /* Raised buttons show borders on both sides. Useful to create pill bars */\n    & > .active {\n      z-index: 2;\n    }\n\n    /* First button is square on the right side */\n    & > button:first-child:not(:last-child),\n    & > a:first-child:not(:last-child) {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n    }\n    /* Middle buttons are square */\n    & > button:not(:last-child):not(:first-child),\n    & > a:not(:last-child):not(:first-child) {\n      border-radius: 0;\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    & > a:first-child + a:not(:last-child),\n    & > button:first-child + button:not(:last-child) {\n      margin-left: -1px;\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    & > button:not(:last-child):not(:first-child) + button,\n    & > a:not(:last-child):not(:first-child) + a {\n      margin-left: -1px;\n    }\n\n    /* Last button is square on the left side */\n    & > button:last-child:not(:first-child),\n    & > a:last-child:not(:first-child) {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n      margin-left: -1px;\n    }\n  ";
});
export default ButtonBar;
var templateObject_1;
//# sourceMappingURL=buttonBar.jsx.map