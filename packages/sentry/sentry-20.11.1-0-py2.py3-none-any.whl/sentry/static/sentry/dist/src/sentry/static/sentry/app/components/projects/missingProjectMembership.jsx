import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { joinTeam } from 'app/actionCreators/teams';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { IconFlag } from 'app/icons';
import Well from 'app/components/well';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var MissingProjectMembership = /** @class */ (function (_super) {
    __extends(MissingProjectMembership, _super);
    function MissingProjectMembership(props) {
        var _this = _super.call(this, props) || this;
        var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
        var project = organization.projects.find(function (p) { return p.slug === projectId; });
        _this.state = {
            loading: false,
            error: false,
            project: project,
        };
        return _this;
    }
    MissingProjectMembership.prototype.joinTeam = function (team) {
        var _this = this;
        this.setState({
            loading: true,
        });
        joinTeam(this.props.api, {
            orgId: this.props.organization.slug,
            teamId: team.slug,
        }, {
            success: function () {
                _this.setState({
                    loading: false,
                    error: false,
                });
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
                addErrorMessage(t('There was an error while trying to leave the team.'));
            },
        });
    };
    MissingProjectMembership.prototype.renderJoinTeam = function (team, features) {
        if (!team) {
            return null;
        }
        if (this.state.loading) {
            return <a className="btn btn-default btn-loading btn-disabled">...</a>;
        }
        else if (team.isPending) {
            return <a className="btn btn-default btn-disabled">{t('Request Pending')}</a>;
        }
        else if (features.has('open-membership')) {
            return (<a className="btn btn-default" onClick={this.joinTeam.bind(this, team)}>
          {t('Join Team')}
        </a>);
        }
        return (<a className="btn btn-default" onClick={this.joinTeam.bind(this, team)}>
        {t('Request Access')}
      </a>);
    };
    MissingProjectMembership.prototype.renderExplanation = function (features) {
        if (features.has('open-membership')) {
            return t('To view this data you must one of the following teams.');
        }
        else {
            return t('To view this data you must first request access to one of the following teams:');
        }
    };
    MissingProjectMembership.prototype.renderJoinTeams = function (features) {
        var _this = this;
        var _a, _b;
        var teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        if (!teams.length) {
            return (<EmptyMessage>
          {t('No teams have access to this project yet. Ask an admin to add your team to this project.')}
        </EmptyMessage>);
        }
        return teams.map(function (team) { return (<p key={team.slug}>
        #{team.slug}: {_this.renderJoinTeam(team, features)}
      </p>); });
    };
    MissingProjectMembership.prototype.render = function () {
        var organization = this.props.organization;
        var features = new Set(organization.features);
        return (<div className="container">
        <StyledWell centered>
          <StyledIconFlag size="xxl"/>
          <p>{t("You're not a member of this project.")}</p>
          <p>{this.renderExplanation(features)}</p>
          {this.renderJoinTeams(features)}
        </StyledWell>
      </div>);
    };
    return MissingProjectMembership;
}(React.Component));
var StyledWell = styled(Well)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var StyledIconFlag = styled(IconFlag)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export { MissingProjectMembership };
export default withApi(MissingProjectMembership);
var templateObject_1, templateObject_2;
//# sourceMappingURL=missingProjectMembership.jsx.map