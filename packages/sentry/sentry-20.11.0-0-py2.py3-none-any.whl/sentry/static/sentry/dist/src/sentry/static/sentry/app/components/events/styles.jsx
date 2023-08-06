import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var COLORS = {
    default: {
        background: theme.backgroundSecondary,
        border: theme.border,
    },
    danger: {
        background: theme.alert.error.backgroundLight,
        border: theme.alert.error.border,
    },
};
export var DataSection = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " 0;\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", " 0 40px;\n  }\n"], ["\n  padding: ", " 0;\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    padding: ", " ", " 0 40px;\n  }\n"])), space(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.breakpoints[0]; }, space(3), space(4));
export var BannerContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n\n  background: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n\n  /* Muted box & processing errors are in different parts of the DOM */\n  &\n    + ", ":first-child,\n    &\n    + div\n    > ", ":first-child {\n    border-top: 0;\n  }\n"], ["\n  font-size: ", ";\n\n  background: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n\n  /* Muted box & processing errors are in different parts of the DOM */\n  &\n    + " /* sc-selector */, ":first-child,\n    &\n    + div\n    > " /* sc-selector */, ":first-child {\n    border-top: 0;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return COLORS[p.priority].background; }, function (p) { return COLORS[p.priority].border; }, function (p) { return COLORS[p.priority].border; }, /* sc-selector */ DataSection, /* sc-selector */ DataSection);
export var BannerSummary = styled('p')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  padding: ", " ", " ", " 40px;\n  margin-bottom: 0;\n\n  /* Get icons in top right of content box */\n  & > .icon,\n  & > svg {\n    flex-shrink: 0;\n    flex-grow: 0;\n    margin-right: ", ";\n    margin-top: 2px;\n  }\n\n  & > span {\n    flex-grow: 1;\n  }\n\n  & > a {\n    align-self: flex-end;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  padding: ", " ", " ", " 40px;\n  margin-bottom: 0;\n\n  /* Get icons in top right of content box */\n  & > .icon,\n  & > svg {\n    flex-shrink: 0;\n    flex-grow: 0;\n    margin-right: ", ";\n    margin-top: 2px;\n  }\n\n  & > span {\n    flex-grow: 1;\n  }\n\n  & > a {\n    align-self: flex-end;\n  }\n"])), space(2), space(4), space(2), space(1));
export var CauseHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n\n  & button,\n  & h3 {\n    color: ", ";\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    text-transform: uppercase;\n  }\n\n  & h3 {\n    margin-bottom: 0;\n  }\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n\n  & button,\n  & h3 {\n    color: ", ";\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    text-transform: uppercase;\n  }\n\n  & h3 {\n    margin-bottom: 0;\n  }\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n  }\n"])), space(3), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map