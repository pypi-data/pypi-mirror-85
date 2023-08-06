import { __extends } from "tslib";
import { withRouter } from 'react-router';
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import NarrowLayout from 'app/components/narrowLayout';
import CreateTeamForm from 'app/components/teams/createTeamForm';
import withOrganization from 'app/utils/withOrganization';
var TeamCreate = /** @class */ (function (_super) {
    __extends(TeamCreate, _super);
    function TeamCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (data) {
            var orgId = _this.props.params.orgId;
            var redirectUrl = "/settings/" + orgId + "/teams/" + data.slug + "/";
            _this.props.router.push(redirectUrl);
        };
        return _this;
    }
    TeamCreate.prototype.getTitle = function () {
        return t('Create Team');
    };
    TeamCreate.prototype.getEndpoints = function () {
        return [];
    };
    TeamCreate.prototype.renderBody = function () {
        return (<NarrowLayout>
        <h3>{t('Create a New Team')}</h3>

        <CreateTeamForm onSuccess={this.handleSubmitSuccess} organization={this.props.organization}/>
      </NarrowLayout>);
    };
    return TeamCreate;
}(AsyncView));
export { TeamCreate };
export default withRouter(withOrganization(TeamCreate));
//# sourceMappingURL=teamCreate.jsx.map