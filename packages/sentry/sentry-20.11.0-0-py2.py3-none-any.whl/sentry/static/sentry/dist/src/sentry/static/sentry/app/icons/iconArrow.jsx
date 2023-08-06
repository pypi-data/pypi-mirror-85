import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import theme from 'app/utils/theme';
import SvgIcon from './svgIcon';
var IconArrow = React.forwardRef(function IconArrow(_a, ref) {
    var _b = _a.direction, direction = _b === void 0 ? 'up' : _b, props = __rest(_a, ["direction"]);
    return (<SvgIcon {...props} ref={ref} css={direction
        ? direction === 'down'
            ? // Down arrows have a zoom issue with Firefox inside of tables due to rotate.
             
            // Since arrows are symmetric, scaling to only flip vertically works to fix the issue.
            css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                transform: scale(1, -1);\n              "], ["\n                transform: scale(1, -1);\n              "]))) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n                transform: rotate(", "deg);\n              "], ["\n                transform: rotate(", "deg);\n              "])), theme.iconDirections[direction])
        : undefined}>
      <path d="M13.76,7.32a.74.74,0,0,1-.53-.22L8,1.87,2.77,7.1A.75.75,0,1,1,1.71,6L7.47.28a.74.74,0,0,1,1.06,0L14.29,6a.75.75,0,0,1,0,1.06A.74.74,0,0,1,13.76,7.32Z"/>
      <path d="M8,15.94a.75.75,0,0,1-.75-.75V.81a.75.75,0,0,1,1.5,0V15.19A.75.75,0,0,1,8,15.94Z"/>
    </SvgIcon>);
});
IconArrow.displayName = 'IconArrow';
export { IconArrow };
var templateObject_1, templateObject_2;
//# sourceMappingURL=iconArrow.jsx.map