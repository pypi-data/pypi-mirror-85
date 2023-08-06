import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import AsyncComponent from 'app/components/asyncComponent';
import AvatarList from 'app/components/avatar/avatarList';
var TeamMembers = /** @class */ (function (_super) {
    __extends(TeamMembers, _super);
    function TeamMembers() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamMembers.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, teamId = _a.teamId;
        return [['members', "/teams/" + orgId + "/" + teamId + "/members/"]];
    };
    TeamMembers.prototype.renderLoading = function () {
        return this.renderBody();
    };
    TeamMembers.prototype.renderBody = function () {
        var members = this.state.members;
        if (!members) {
            return null;
        }
        var users = members.filter(function (_a) {
            var user = _a.user;
            return !!user;
        }).map(function (_a) {
            var user = _a.user;
            return user;
        });
        return <AvatarList users={users}/>;
    };
    TeamMembers.propTypes = {
        teamId: PropTypes.string.isRequired,
        orgId: PropTypes.string.isRequired,
    };
    return TeamMembers;
}(AsyncComponent));
export default TeamMembers;
//# sourceMappingURL=teamMembers.jsx.map