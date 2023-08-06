import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import theme from 'app/utils/theme';
import SvgIcon from './svgIcon';
var IconSliders = React.forwardRef(function IconSliders(_a, ref) {
    var _b = _a.direction, direction = _b === void 0 ? 'up' : _b, props = __rest(_a, ["direction"]);
    return (<SvgIcon {...props} ref={ref} css={direction
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n              transform: rotate(", "deg);\n            "], ["\n              transform: rotate(", "deg);\n            "])), theme.iconDirections[direction]) : undefined}>
      <path d="M4.33,14a2.86,2.86,0,1,1,2.86-2.85A2.86,2.86,0,0,1,4.33,14Zm0-4.21a1.36,1.36,0,1,0,1.36,1.36A1.35,1.35,0,0,0,4.33,9.75Z"/>
      <path d="M11.71,7.75a2.86,2.86,0,1,1,2.85-2.86A2.86,2.86,0,0,1,11.71,7.75Zm0-4.21a1.36,1.36,0,1,0,1.35,1.35A1.36,1.36,0,0,0,11.71,3.54Z"/>
      <path d="M15.19,11.86H6.44a.75.75,0,0,1,0-1.5h8.75a.75.75,0,0,1,0,1.5Z"/>
      <path d="M2.23,11.86H.81a.75.75,0,0,1,0-1.5H2.23a.75.75,0,1,1,0,1.5Z"/>
      <path d="M15.19,5.64H13.81a.75.75,0,0,1,0-1.5h1.38a.75.75,0,0,1,0,1.5Z"/>
      <path d="M9.6,5.64H.81a.75.75,0,1,1,0-1.5H9.6a.75.75,0,0,1,0,1.5Z"/>
    </SvgIcon>);
});
IconSliders.displayName = 'IconSliders';
export { IconSliders };
var templateObject_1;
//# sourceMappingURL=iconSliders.jsx.map