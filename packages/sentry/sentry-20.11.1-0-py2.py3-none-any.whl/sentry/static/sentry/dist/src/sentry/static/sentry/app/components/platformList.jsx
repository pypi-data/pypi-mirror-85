import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PlatformIcon from 'platformicons';
var PlatformList = function (_a) {
    var _b = _a.platforms, platforms = _b === void 0 ? [] : _b, _c = _a.direction, direction = _c === void 0 ? 'right' : _c, _d = _a.max, max = _d === void 0 ? 3 : _d, _e = _a.size, size = _e === void 0 ? 16 : _e, _f = _a.consistentWidth, consistentWidth = _f === void 0 ? false : _f, className = _a.className;
    var getIcon = function (platform, index) { return (<StyledPlatformIcon key={platform + index} platform={platform} size={size}/>); };
    var getIcons = function (items) { return items.slice().reverse().map(getIcon); };
    var platformsPreview = platforms.slice(0, max);
    return (<PlatformIcons direction={direction} max={max} size={size} consistentWidth={consistentWidth} className={className}>
      {platforms.length > 0 ? (getIcons(platformsPreview)) : (<StyledPlatformIcon size={size} platform="default"/>)}
    </PlatformIcons>);
};
var getOverlapWidth = function (size) { return Math.round(size / 4); };
var PlatformIcons = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n  flex-direction: row;\n  justify-content: ", ";\n  ", ";\n"], ["\n  display: flex;\n  flex-shrink: 0;\n  flex-direction: row;\n  justify-content: ", ";\n  ",
    ";\n"])), function (p) { return (p.direction === 'right' ? 'flex-end' : 'flex-start'); }, function (p) {
    return p.consistentWidth && "width: " + (p.size + (p.max - 1) * getOverlapWidth(p.size)) + "px;";
});
var StyledPlatformIcon = styled(function (_a) {
    var size = _a.size, props = __rest(_a, ["size"]);
    return (<PlatformIcon size={size + "px"} {...props}/>);
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: ", ";\n  box-shadow: 0 0 0 1px ", ";\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"], ["\n  border-radius: ", ";\n  box-shadow: 0 0 0 1px ", ";\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.background; }, function (p) { return p.size * -1 + getOverlapWidth(p.size) + "px;"; });
export default PlatformList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=platformList.jsx.map