import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { AutoCompleteRoot } from 'app/components/dropdownAutoComplete/menu';
import { TimeRangeRoot } from 'app/components/organizations/timeRangeSelector/index';
function getMediaQueryForSpacer(p) {
    return p.isSpacer
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        @media (max-width: ", ") {\n          display: none;\n        }\n      "], ["\n        @media (max-width: ", ") {\n          display: none;\n        }\n      "])), p.theme.breakpoints[1]) : '';
}
var HeaderItemPosition = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  min-width: 0;\n  height: 100%;\n\n  ", "\n\n  ", ", ", " {\n    flex: 1;\n    min-width: 0;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n  min-width: 0;\n  height: 100%;\n\n  ", "\n\n  ", ", ", " {\n    flex: 1;\n    min-width: 0;\n  }\n"])), getMediaQueryForSpacer, AutoCompleteRoot, TimeRangeRoot);
export default HeaderItemPosition;
var templateObject_1, templateObject_2;
//# sourceMappingURL=headerItemPosition.jsx.map