import { __rest } from "tslib";
import React from 'react';
import MemberBadge from 'app/components/idBadge/memberBadge';
import UserBadge from 'app/components/idBadge/userBadge';
import TeamBadge from 'app/components/idBadge/teamBadge/badge';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import OrganizationBadge from 'app/components/idBadge/organizationBadge';
function getBadge(_a) {
    var organization = _a.organization, team = _a.team, project = _a.project, user = _a.user, member = _a.member, props = __rest(_a, ["organization", "team", "project", "user", "member"]);
    if (organization) {
        return <OrganizationBadge organization={organization} {...props}/>;
    }
    if (team) {
        return <TeamBadge team={team} {...props}/>;
    }
    if (project) {
        return <ProjectBadge project={project} {...props}/>;
    }
    if (user) {
        return <UserBadge user={user} {...props}/>;
    }
    if (member) {
        return <MemberBadge member={member} {...props}/>;
    }
    return null;
}
export default getBadge;
//# sourceMappingURL=getBadge.jsx.map