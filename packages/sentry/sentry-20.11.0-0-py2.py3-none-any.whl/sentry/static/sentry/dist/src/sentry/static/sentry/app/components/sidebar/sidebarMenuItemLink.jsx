import { __rest } from "tslib";
import React from 'react';
import Link from 'app/components/links/link';
import ExternalLink from 'app/components/links/externalLink';
var SidebarMenuItemLink = function (_a) {
    var to = _a.to, href = _a.href, props = __rest(_a, ["to", "href"]);
    if (href) {
        return <ExternalLink href={href} {...props}/>;
    }
    if (to) {
        return <Link to={to} {...props}/>;
    }
    return <div tabIndex={0} {...props}/>;
};
export default SidebarMenuItemLink;
//# sourceMappingURL=sidebarMenuItemLink.jsx.map