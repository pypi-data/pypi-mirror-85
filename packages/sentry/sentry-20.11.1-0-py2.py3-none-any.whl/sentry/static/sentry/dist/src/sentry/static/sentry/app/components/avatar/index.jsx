import { __assign, __rest } from "tslib";
import React from 'react';
import OrganizationAvatar from 'app/components/avatar/organizationAvatar';
import ProjectAvatar from 'app/components/avatar/projectAvatar';
import TeamAvatar from 'app/components/avatar/teamAvatar';
import UserAvatar from 'app/components/avatar/userAvatar';
var Avatar = React.forwardRef(function Avatar(_a, ref) {
    var _b = _a.hasTooltip, hasTooltip = _b === void 0 ? false : _b, user = _a.user, team = _a.team, project = _a.project, organization = _a.organization, props = __rest(_a, ["hasTooltip", "user", "team", "project", "organization"]);
    var commonProps = __assign({ hasTooltip: hasTooltip, forwardedRef: ref }, props);
    if (user) {
        return <UserAvatar user={user} {...commonProps}/>;
    }
    if (team) {
        return <TeamAvatar team={team} {...commonProps}/>;
    }
    if (project) {
        return <ProjectAvatar project={project} {...commonProps}/>;
    }
    return <OrganizationAvatar organization={organization} {...commonProps}/>;
});
export default Avatar;
//# sourceMappingURL=index.jsx.map