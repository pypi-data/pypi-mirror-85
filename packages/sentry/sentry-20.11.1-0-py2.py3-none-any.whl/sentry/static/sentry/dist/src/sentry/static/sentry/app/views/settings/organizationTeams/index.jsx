import { __extends } from "tslib";
import React from 'react';
import { loadStats } from 'app/actionCreators/projects';
import { sortArray } from 'app/utils';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withTeams from 'app/utils/withTeams';
import OrganizationTeams from './organizationTeams';
var OrganizationTeamsContainer = /** @class */ (function (_super) {
    __extends(OrganizationTeamsContainer, _super);
    function OrganizationTeamsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationTeamsContainer.prototype.componentDidMount = function () {
        this.fetchStats();
    };
    OrganizationTeamsContainer.prototype.fetchStats = function () {
        loadStats(this.props.api, {
            orgId: this.props.params.orgId,
            query: {
                since: (new Date().getTime() / 1000 - 3600 * 24).toString(),
                stat: 'generated',
                group: 'project',
            },
        });
    };
    OrganizationTeamsContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, teams = _a.teams;
        if (!organization) {
            return null;
        }
        var allTeams = sortArray(teams, function (team) { return team.name; });
        var activeTeams = allTeams.filter(function (team) { return team.isMember; });
        return (<OrganizationTeams {...this.props} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} allTeams={allTeams} activeTeams={activeTeams}/>);
    };
    return OrganizationTeamsContainer;
}(React.Component));
export { OrganizationTeamsContainer };
export default withApi(withOrganization(withTeams(OrganizationTeamsContainer)));
//# sourceMappingURL=index.jsx.map