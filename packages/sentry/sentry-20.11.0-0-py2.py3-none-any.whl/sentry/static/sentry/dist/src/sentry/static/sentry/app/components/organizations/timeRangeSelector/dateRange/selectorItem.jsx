import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var SelectorItem = /** @class */ (function (_super) {
    __extends(SelectorItem, _super);
    function SelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function (e) {
            var _a = _this.props, onClick = _a.onClick, value = _a.value;
            onClick(value, e);
        };
        return _this;
    }
    SelectorItem.prototype.render = function () {
        var _a = this.props, className = _a.className, label = _a.label;
        return (<div className={className} onClick={this.handleClick}>
        <Label>{label}</Label>
      </div>);
    };
    SelectorItem.propTypes = {
        onClick: PropTypes.func.isRequired,
        value: PropTypes.string,
        label: PropTypes.node,
    };
    return SelectorItem;
}(React.PureComponent));
var StyledSelectorItem = styled(SelectorItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  cursor: pointer;\n  white-space: nowrap;\n  padding: ", ";\n  align-items: center;\n  flex: 1;\n  background-color: ", ";\n  font-weight: ", ";\n  border-bottom: 1px solid ", ";\n\n  &:hover {\n    background: ", ";\n  }\n"], ["\n  display: flex;\n  cursor: pointer;\n  white-space: nowrap;\n  padding: ", ";\n  align-items: center;\n  flex: 1;\n  background-color: ", ";\n  font-weight: ", ";\n  border-bottom: 1px solid ", ";\n\n  &:hover {\n    background: ", ";\n  }\n"])), space(1), function (p) { return (p.selected ? p.theme.backgroundSecondary : 'transparent'); }, function (p) { return (p.selected ? 'bold' : 'normal'); }, function (p) { return (p.last ? 'transparent' : p.theme.innerBorder); }, function (p) { return p.theme.backgroundSecondary; });
var Label = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space(1));
export default StyledSelectorItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=selectorItem.jsx.map