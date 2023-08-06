import React from 'react';
import { IconWrapper } from './styles';
var Icon = React.memo(function (_a) {
    var icon = _a.icon, color = _a.color, size = _a.size;
    var Svg = icon;
    return (<IconWrapper color={color}>
      <Svg size={size}/>
    </IconWrapper>);
});
export default Icon;
//# sourceMappingURL=icon.jsx.map