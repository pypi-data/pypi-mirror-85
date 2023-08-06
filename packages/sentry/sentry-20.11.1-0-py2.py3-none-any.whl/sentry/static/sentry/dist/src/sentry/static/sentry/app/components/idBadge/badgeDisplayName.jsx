import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var BadgeDisplayName = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  padding: ", " 0;\n"], ["\n  ",
    ";\n  padding: ", " 0;\n"])), function (p) {
    return p.hideOverflow &&
        "\n      " + overflowEllipsis + ";\n      max-width: " + (typeof p.hideOverflow === 'string'
            ? p.hideOverflow
            : p.theme.settings.maxCrumbWidth) + "\n  ";
}, space(0.25));
export default BadgeDisplayName;
var templateObject_1;
//# sourceMappingURL=badgeDisplayName.jsx.map