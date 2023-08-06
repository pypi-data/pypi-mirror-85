import { __rest } from "tslib";
import React from 'react';
import BaseBadge from 'app/components/idBadge/baseBadge';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
var ProjectBadge = function (_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, project = _a.project, props = __rest(_a, ["hideOverflow", "project"]);
    return (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>{project.slug}</BadgeDisplayName>} project={project} {...props}/>);
};
export default ProjectBadge;
//# sourceMappingURL=projectBadge.jsx.map