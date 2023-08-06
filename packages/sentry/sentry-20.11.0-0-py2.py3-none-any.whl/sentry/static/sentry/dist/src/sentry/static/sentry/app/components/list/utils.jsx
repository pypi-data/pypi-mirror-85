import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
var commonSymbolStyle = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  & > li {\n    padding-left: 34px;\n    :before {\n      border-radius: 50%;\n      position: absolute;\n    }\n  }\n"], ["\n  & > li {\n    padding-left: 34px;\n    :before {\n      border-radius: 50%;\n      position: absolute;\n    }\n  }\n"])));
var bulletStyle = function (theme) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n  & > li:before {\n    content: '';\n    width: 6px;\n    height: 6px;\n    left: 5px;\n    top: 10px;\n    border: 1px solid ", ";\n  }\n"], ["\n  ", "\n  & > li:before {\n    content: '';\n    width: 6px;\n    height: 6px;\n    left: 5px;\n    top: 10px;\n    border: 1px solid ", ";\n  }\n"])), commonSymbolStyle, theme.gray500); };
var numericStyle = function (theme, isSolid) {
    if (isSolid === void 0) { isSolid = false; }
    return css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n  & > li:before {\n    counter-increment: numberedList;\n    content: counter(numberedList);\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    text-align: center;\n    left: 0;\n    ", "\n  }\n  counter-reset: numberedList;\n"], ["\n  ", "\n  & > li:before {\n    counter-increment: numberedList;\n    content: counter(numberedList);\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    text-align: center;\n    left: 0;\n    ",
        "\n  }\n  counter-reset: numberedList;\n"])), commonSymbolStyle, isSolid
        ? css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n          width: 24px;\n          height: 24px;\n          font-weight: 500;\n          font-size: ", ";\n          background-color: ", ";\n        "], ["\n          width: 24px;\n          height: 24px;\n          font-weight: 500;\n          font-size: ", ";\n          background-color: ", ";\n        "])), theme.fontSizeSmall, theme.yellow300) : css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n          top: 3px;\n          width: 18px;\n          height: 18px;\n          font-weight: 600;\n          font-size: 10px;\n          border: 1px solid ", ";\n        "], ["\n          top: 3px;\n          width: 18px;\n          height: 18px;\n          font-weight: 600;\n          font-size: 10px;\n          border: 1px solid ", ";\n        "])), theme.gray500));
};
export var listSymbol = {
    numeric: 'numeric',
    'colored-numeric': 'colored-numeric',
    bullet: 'bullet',
};
export function getListSymbolStyle(theme, symbol) {
    switch (symbol) {
        case 'numeric':
            return numericStyle(theme);
        case 'colored-numeric':
            return numericStyle(theme, true);
        default:
            return bulletStyle(theme);
    }
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=utils.jsx.map