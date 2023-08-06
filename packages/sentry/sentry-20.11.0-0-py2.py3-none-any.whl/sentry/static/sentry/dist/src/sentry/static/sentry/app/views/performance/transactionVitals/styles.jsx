import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import { PanelItem } from 'app/components/panels';
import space from 'app/styles/space';
export var Card = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 325px minmax(100px, auto);\n  padding: 0;\n"], ["\n  display: grid;\n  grid-template-columns: 325px minmax(100px, auto);\n  padding: 0;\n"])));
export var CardSection = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(3));
export var CardSummary = styled(CardSection)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  border-right: 1px solid ", ";\n  grid-column: 1/1;\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n"], ["\n  position: relative;\n  border-right: 1px solid ", ";\n  grid-column: 1/1;\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n"])), function (p) { return p.theme.border; });
export var CardSectionHeading = styled(SectionHeading)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0px;\n"], ["\n  margin: 0px;\n"])));
export var Description = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
export var StatNumber = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: 32px;\n"], ["\n  font-size: 32px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=styles.jsx.map