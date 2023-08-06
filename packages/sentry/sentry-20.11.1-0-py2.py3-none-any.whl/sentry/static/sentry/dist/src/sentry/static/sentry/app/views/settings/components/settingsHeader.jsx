import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
// This is required to offer components that sit between this settings header
// and i.e. dropdowns, some zIndex layer room
//
// e.g. app/views/settings/incidentRules/triggers/chart/
var HEADER_Z_INDEX_OFFSET = 5;
var SettingsHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: sticky;\n  top: 0;\n  z-index: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  height: ", ";\n"], ["\n  position: sticky;\n  top: 0;\n  z-index: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  height: ", ";\n"])), function (p) { return p.theme.zIndex.header + HEADER_Z_INDEX_OFFSET; }, space(3), space(4), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.settings.headerHeight; });
export default SettingsHeader;
var templateObject_1;
//# sourceMappingURL=settingsHeader.jsx.map