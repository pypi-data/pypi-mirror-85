import { __extends } from "tslib";
import uniqBy from 'lodash/uniqBy';
import React from 'react';
import MemberListStore from 'app/stores/memberListStore';
import Projects from 'app/utils/projects';
import { callIfFunction } from 'app/utils/callIfFunction';
import { isRenderFunc } from 'app/utils/isRenderFunc';
import withOrganization from 'app/utils/withOrganization';
var buildUserId = function (id) { return "user:" + id; };
var buildTeamId = function (id) { return "team:" + id; };
/**
 * Make sure the actionCreator, `fetchOrgMembers`, has been called somewhere
 * higher up the component chain.
 *
 * Will provide a list of users and teams that can be used for @-mentions
 * */
var Mentionables = /** @class */ (function (_super) {
    __extends(Mentionables, _super);
    function Mentionables() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            members: MemberListStore.getAll(),
        };
        _this.listeners = [
            MemberListStore.listen(function (users) {
                _this.handleMemberListUpdate(users);
            }, undefined),
        ];
        _this.handleMemberListUpdate = function (members) {
            if (members === _this.state.members) {
                return;
            }
            _this.setState({
                members: members,
            });
        };
        _this.renderChildren = function (_a) {
            var projects = _a.projects;
            var _b = _this.props, children = _b.children, me = _b.me;
            if (isRenderFunc(children)) {
                return children({
                    members: _this.getMemberList(_this.state.members, me),
                    teams: _this.getTeams(projects),
                });
            }
            return null;
        };
        return _this;
    }
    Mentionables.prototype.componentWillUnmount = function () {
        this.listeners.forEach(callIfFunction);
    };
    Mentionables.prototype.getMemberList = function (memberList, sessionUser) {
        var members = uniqBy(memberList, function (_a) {
            var id = _a.id;
            return id;
        }).filter(function (_a) {
            var id = _a.id;
            return !sessionUser || sessionUser.id !== id;
        });
        return members.map(function (member) { return ({
            id: buildUserId(member.id),
            display: member.name,
            email: member.email,
        }); });
    };
    Mentionables.prototype.getTeams = function (projects) {
        var uniqueTeams = uniqBy(projects
            .map(function (_a) {
            var teams = _a.teams;
            return teams;
        })
            .reduce(function (acc, teams) { return acc.concat(teams || []); }, []), 'id');
        return uniqueTeams.map(function (team) { return ({
            id: buildTeamId(team.id),
            display: "#" + team.slug,
            email: team.id,
        }); });
    };
    Mentionables.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projectSlugs = _a.projectSlugs;
        if (!projectSlugs || !projectSlugs.length) {
            return this.renderChildren({ projects: [] });
        }
        return (<Projects slugs={projectSlugs} orgId={organization.slug}>
        {this.renderChildren}
      </Projects>);
    };
    return Mentionables;
}(React.PureComponent));
export default withOrganization(Mentionables);
//# sourceMappingURL=mentionables.jsx.map