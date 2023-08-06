import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import Link from 'app/components/links/link';
import ShortId from 'app/components/shortId';
import overflowEllipsis from 'app/styles/overflowEllipsis';
/**
 * Styled components used to render discover result sets.
 */
export var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
export var VersionContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"], ["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"])), overflowEllipsis);
export var NumberContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: right;\n  ", ";\n"], ["\n  text-align: right;\n  ", ";\n"])), overflowEllipsis);
export var StyledDateTime = styled(DateTime)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.gray300; }, overflowEllipsis);
export var OverflowLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
export var StyledShortId = styled(ShortId)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
export var BarContainer = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  max-width: 80px;\n  margin-left: auto;\n"], ["\n  max-width: 80px;\n  margin-left: auto;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=styles.jsx.map