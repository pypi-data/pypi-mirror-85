import { __rest } from "tslib";
import React from 'react';
import BaseBadge from 'app/components/idBadge/baseBadge';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
var Badge = function (_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, team = _a.team, props = __rest(_a, ["hideOverflow", "team"]);
    return (<BaseBadge data-test-id="team-badge" displayName={<BadgeDisplayName hideOverflow={hideOverflow}>{"#" + team.slug}</BadgeDisplayName>} team={team} {...props}/>);
};
export default Badge;
//# sourceMappingURL=badge.jsx.map