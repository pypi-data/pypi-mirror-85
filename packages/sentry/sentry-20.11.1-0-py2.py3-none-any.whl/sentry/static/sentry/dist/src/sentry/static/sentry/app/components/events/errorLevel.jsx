import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
var DEFAULT_SIZE = '13px';
function getLevelColor(_a) {
    var _b = _a.level, level = _b === void 0 ? '' : _b, theme = _a.theme;
    var COLORS = {
        error: theme.orange400,
        info: theme.blue300,
        warning: theme.orange300,
        fatal: theme.red300,
        sample: theme.purple300,
    };
    return "background-color: " + (COLORS[level] || theme.orange400) + ";";
}
var ErrorLevel = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  position: relative;\n  width: ", ";\n  height: ", ";\n  text-indent: -9999em;\n  display: inline-block;\n  border-radius: 50%;\n  flex-shrink: 0;\n\n  ", "\n"], ["\n  padding: 0;\n  position: relative;\n  width: ", ";\n  height: ", ";\n  text-indent: -9999em;\n  display: inline-block;\n  border-radius: 50%;\n  flex-shrink: 0;\n\n  ", "\n"])), function (p) { return p.size || DEFAULT_SIZE; }, function (p) { return p.size || DEFAULT_SIZE; }, getLevelColor);
export default ErrorLevel;
var templateObject_1;
//# sourceMappingURL=errorLevel.jsx.map