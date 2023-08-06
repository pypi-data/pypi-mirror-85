import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Row = function (_a) {
    var item = _a.item, style = _a.style, itemSize = _a.itemSize, highlightedIndex = _a.highlightedIndex, inputValue = _a.inputValue, getItemProps = _a.getItemProps;
    var index = item.index;
    if (item === null || item === void 0 ? void 0 : item.groupLabel) {
        return (<LabelWithBorder style={style}>
        {item.label && <GroupLabel>{item.label}</GroupLabel>}
      </LabelWithBorder>);
    }
    return (<AutoCompleteItem itemSize={itemSize} hasGrayBackground={index === highlightedIndex} {...getItemProps({ item: item, index: index, style: style })}>
      {typeof item.label === 'function' ? item.label({ inputValue: inputValue }) : item.label}
    </AutoCompleteItem>);
};
export default Row;
var LabelWithBorder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n\n  :first-child {\n    border-top: none;\n  }\n  :last-child {\n    border-bottom: none;\n  }\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n\n  :first-child {\n    border-top: none;\n  }\n  :last-child {\n    border-bottom: none;\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var GroupLabel = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n"], ["\n  padding: ", " ", ";\n"])), space(0.25), space(1));
var getItemPaddingForSize = function (itemSize) {
    if (itemSize === 'small') {
        return space(0.5) + " " + space(1);
    }
    if (itemSize === 'zero') {
        return '0';
    }
    return space(1);
};
var AutoCompleteItem = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* needed for virtualized lists that do not fill parent height */\n  /* e.g. breadcrumbs (org height > project, but want same fixed height for both) */\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  font-size: 0.9em;\n  background-color: ", ";\n  color: ", ";\n  padding: ", ";\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n\n  :last-child {\n    border-bottom: none;\n  }\n\n  :hover {\n    color: ", ";\n    background-color: ", ";\n  }\n"], ["\n  /* needed for virtualized lists that do not fill parent height */\n  /* e.g. breadcrumbs (org height > project, but want same fixed height for both) */\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  font-size: 0.9em;\n  background-color: ",
    ";\n  color: ", ";\n  padding: ", ";\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n\n  :last-child {\n    border-bottom: none;\n  }\n\n  :hover {\n    color: ", ";\n    background-color: ", ";\n  }\n"])), function (p) {
    return p.hasGrayBackground ? p.theme.backgroundSecondary : 'transparent';
}, function (p) { return (p.hasGrayBackground ? p.theme.textColor : 'inherit'); }, function (p) { return getItemPaddingForSize(p.itemSize); }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.backgroundSecondary; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=row.jsx.map