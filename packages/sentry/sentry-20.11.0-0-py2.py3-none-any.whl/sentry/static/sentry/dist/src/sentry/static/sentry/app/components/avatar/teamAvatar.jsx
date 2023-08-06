import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { explodeSlug } from 'app/utils';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import SentryTypes from 'app/sentryTypes';
var TeamAvatar = /** @class */ (function (_super) {
    __extends(TeamAvatar, _super);
    function TeamAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamAvatar.prototype.render = function () {
        var _a = this.props, team = _a.team, props = __rest(_a, ["team"]);
        if (!team) {
            return null;
        }
        var slug = (team && team.slug) || '';
        var title = explodeSlug(slug);
        var tooltip = "#" + title;
        return (<BaseAvatar {...props} type={(team.avatar && team.avatar.avatarType) || 'letter_avatar'} uploadPath="team-avatar" uploadId={team.avatar && team.avatar.avatarUuid} letterId={slug} tooltip={tooltip} title={title}/>);
    };
    TeamAvatar.propTypes = __assign({ team: SentryTypes.Team }, BaseAvatar.propTypes);
    return TeamAvatar;
}(React.Component));
export default TeamAvatar;
//# sourceMappingURL=teamAvatar.jsx.map