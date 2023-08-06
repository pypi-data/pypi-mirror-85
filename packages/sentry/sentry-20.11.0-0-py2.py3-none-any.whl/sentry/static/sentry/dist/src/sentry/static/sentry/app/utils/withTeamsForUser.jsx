import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import getDisplayName from 'app/utils/getDisplayName';
import getProjectsByTeams from 'app/utils/getProjectsByTeams';
import ConfigStore from 'app/stores/configStore';
import { metric } from './analytics';
var withTeamsForUser = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                teams: [],
                loadingTeams: true,
                error: null,
            };
            return _this;
        }
        class_1.prototype.componentDidMount = function () {
            this.fetchTeams();
        };
        class_1.prototype.fetchTeams = function () {
            return __awaiter(this, void 0, void 0, function () {
                var teamsWithProjects, error_1;
                var _this = this;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            this.setState({
                                loadingTeams: true,
                            });
                            _a.label = 1;
                        case 1:
                            _a.trys.push([1, 3, , 4]);
                            metric.mark({ name: 'user-teams-fetch-start' });
                            return [4 /*yield*/, this.props.api.requestPromise(this.getUsersTeamsEndpoint())];
                        case 2:
                            teamsWithProjects = _a.sent();
                            this.setState({
                                teams: teamsWithProjects,
                                loadingTeams: false,
                            }, function () {
                                metric.measure({
                                    name: 'app.component.perf',
                                    start: 'user-teams-fetch-start',
                                    data: {
                                        name: 'user-teams',
                                        route: '/organizations/:orgid/user-teams',
                                        organization_id: parseInt(_this.props.organization.id, 10),
                                    },
                                });
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            error_1 = _a.sent();
                            this.setState({
                                error: error_1,
                                loadingTeams: false,
                            });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        class_1.prototype.populateTeamsWithProjects = function (teams, projects) {
            var isSuperuser = ConfigStore.get('user').isSuperuser;
            var projectsByTeam = getProjectsByTeams(teams, projects, isSuperuser).projectsByTeam;
            var teamsWithProjects = teams.map(function (team) {
                var teamProjects = projectsByTeam[team.slug] || [];
                return __assign(__assign({}, team), { projects: teamProjects });
            });
            this.setState({
                teams: teamsWithProjects,
                loadingTeams: false,
            });
        };
        class_1.prototype.getUsersTeamsEndpoint = function () {
            return "/organizations/" + this.props.organization.slug + "/user-teams/";
        };
        class_1.prototype.render = function () {
            return <WrappedComponent {...this.props} {...this.state}/>;
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withUsersTeams(" + getDisplayName(WrappedComponent) + ")",
    _a; };
export default withTeamsForUser;
//# sourceMappingURL=withTeamsForUser.jsx.map