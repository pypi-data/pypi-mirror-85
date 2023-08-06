import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
var TableLayout = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: ",
    ";\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"])), function (p) {
    return p.status === 'open' ? '4fr 1fr 2fr' : '3fr 2fr 2fr 1fr 2fr';
}, space(1.5));
var TitleAndSparkLine = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: ", ";\n  grid-gap: ", ";\n  grid-template-columns: auto 120px;\n  align-items: center;\n  padding-right: ", ";\n  overflow: hidden;\n"], ["\n  display: ", ";\n  grid-gap: ", ";\n  grid-template-columns: auto 120px;\n  align-items: center;\n  padding-right: ", ";\n  overflow: hidden;\n"])), function (p) { return (p.status === 'open' ? 'grid' : 'flex'); }, space(1), space(2));
export { TableLayout, TitleAndSparkLine };
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map