import React from 'react';
import SvgIcon from './svgIcon';
var IconActivity = React.forwardRef(function IconActivity(props, ref) {
    return (<SvgIcon {...props} ref={ref}>
      <path d="M15.19,8.74H5.25a.75.75,0,0,1,0-1.5h9.94a.75.75,0,0,1,0,1.5Z"/>
      <path d="M15.19,15H5.25a.75.75,0,1,1,0-1.5h9.94a.75.75,0,0,1,0,1.5Z"/>
      <path d="M15.19,2.53H5.25a.75.75,0,0,1,0-1.5h9.94a.75.75,0,1,1,0,1.5Z"/>
      <path d="M2.25,8.74H.71a.75.75,0,1,1,0-1.5H2.25a.75.75,0,0,1,0,1.5Z"/>
      <path d="M2.25,15H.71a.75.75,0,0,1,0-1.5H2.25a.75.75,0,0,1,0,1.5Z"/>
      <path d="M2.25,2.53H.71A.75.75,0,0,1,.71,1H2.25a.75.75,0,1,1,0,1.5Z"/>
    </SvgIcon>);
});
IconActivity.displayName = 'IconActivity';
export { IconActivity };
//# sourceMappingURL=iconActivity.jsx.map