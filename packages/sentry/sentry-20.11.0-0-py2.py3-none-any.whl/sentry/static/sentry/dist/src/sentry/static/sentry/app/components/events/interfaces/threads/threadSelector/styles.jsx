import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var Grid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-template-columns: 30px 2.5fr 4fr 0fr 40px;\n  @media (min-width: ", ") {\n    grid-template-columns: 40px 2.5fr 3.5fr 105px 40px;\n  }\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-template-columns: 30px 2.5fr 4fr 0fr 40px;\n  @media (min-width: ", ") {\n    grid-template-columns: 40px 2.5fr 3.5fr 105px 40px;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1), function (p) { return p.theme.breakpoints[0]; });
var GridCell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
export { Grid, GridCell };
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map