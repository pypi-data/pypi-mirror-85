import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import space from 'app/styles/space';
var defaultProps = {
    /**
     * This is a render prop which may be used to augment the checkbox rendered
     * to the right of the row. It will receive the default `checkbox` as a
     * prop along with the `checked` boolean.
     */
    renderCheckbox: (function (_a) {
        var checkbox = _a.checkbox;
        return checkbox;
    }),
    multi: true,
};
var GlobalSelectionHeaderRow = /** @class */ (function (_super) {
    __extends(GlobalSelectionHeaderRow, _super);
    function GlobalSelectionHeaderRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GlobalSelectionHeaderRow.prototype.render = function () {
        var _a = this.props, checked = _a.checked, onCheckClick = _a.onCheckClick, multi = _a.multi, renderCheckbox = _a.renderCheckbox, children = _a.children, props = __rest(_a, ["checked", "onCheckClick", "multi", "renderCheckbox", "children"]);
        var checkbox = <CheckboxFancy isDisabled={!multi} isChecked={checked}/>;
        return (<Container isChecked={checked} {...props}>
        <Content multi={multi}>{children}</Content>
        <CheckboxHitbox onClick={multi ? onCheckClick : undefined}>
          {renderCheckbox({ checkbox: checkbox, checked: checked })}
        </CheckboxHitbox>
      </Container>);
    };
    GlobalSelectionHeaderRow.defaultProps = defaultProps;
    return GlobalSelectionHeaderRow;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: 14px;\n  font-weight: 400;\n  padding-left: ", ";\n  height: ", "px;\n  flex-shrink: 0;\n\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: 14px;\n  font-weight: 400;\n  padding-left: ", ";\n  height: ", "px;\n  flex-shrink: 0;\n\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n"])), space(0.5), function (p) { return p.theme.headerSelectorRowHeight; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.33); }, CheckboxFancy);
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 1;\n  overflow: hidden;\n  align-items: center;\n  height: 100%;\n  flex-grow: 1;\n  user-select: none;\n\n  &:hover {\n    text-decoration: ", ";\n    color: ", ";\n  }\n"], ["\n  display: flex;\n  flex-shrink: 1;\n  overflow: hidden;\n  align-items: center;\n  height: 100%;\n  flex-grow: 1;\n  user-select: none;\n\n  &:hover {\n    text-decoration: ", ";\n    color: ", ";\n  }\n"])), function (p) { return (p.multi ? 'underline' : null); }, function (p) { return (p.multi ? p.theme.blue300 : null); });
var CheckboxHitbox = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 -", " 0 0; /* pushes the click box to be flush with the edge of the menu */\n  padding: 0 ", ";\n  height: 100%;\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  margin: 0 -", " 0 0; /* pushes the click box to be flush with the edge of the menu */\n  padding: 0 ", ";\n  height: 100%;\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"])), space(1), space(1.5));
export default GlobalSelectionHeaderRow;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=globalSelectionHeaderRow.jsx.map