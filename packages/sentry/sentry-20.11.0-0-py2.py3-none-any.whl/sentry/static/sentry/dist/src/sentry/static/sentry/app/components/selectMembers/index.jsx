import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import debounce from 'lodash/debounce';
import styled from '@emotion/styled';
import { IconAdd } from 'app/icons';
import { addTeamToProject } from 'app/actionCreators/projects';
import { callIfFunction } from 'app/utils/callIfFunction';
import { t } from 'app/locale';
import Button from 'app/components/button';
import IdBadge from 'app/components/idBadge';
import MemberListStore from 'app/stores/memberListStore';
import ProjectsStore from 'app/stores/projectsStore';
import SelectControl from 'app/components/forms/selectControl';
import TeamStore from 'app/stores/teamStore';
import Tooltip from 'app/components/tooltip';
import withApi from 'app/utils/withApi';
var getSearchKeyForUser = function (user) {
    return (user.email && user.email.toLowerCase()) + " " + (user.name && user.name.toLowerCase());
};
/**
 * A component that allows you to select either members and/or teams
 */
var SelectMembers = /** @class */ (function (_super) {
    __extends(SelectMembers, _super);
    function SelectMembers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            inputValue: '',
            options: null,
            memberListLoading: !MemberListStore.isLoaded(),
        };
        _this.selectRef = React.createRef();
        _this.unlisteners = [
            MemberListStore.listen(function () {
                _this.setState({
                    memberListLoading: !MemberListStore.isLoaded(),
                });
            }, undefined),
        ];
        _this.renderUserBadge = function (user) { return (<IdBadge avatarSize={24} user={user} hideEmail useLink={false}/>); };
        _this.createMentionableUser = function (user) { return ({
            value: user.id,
            label: _this.renderUserBadge(user),
            searchKey: getSearchKeyForUser(user),
            actor: {
                type: 'user',
                id: user.id,
                name: user.name,
            },
        }); };
        _this.createUnmentionableUser = function (_a) {
            var user = _a.user;
            return (__assign(__assign({}, _this.createMentionableUser(user)), { disabled: true, label: (<DisabledLabel>
        <Tooltip position="left" title={t('%s is not a member of project', user.name || user.email)}>
          {_this.renderUserBadge(user)}
        </Tooltip>
      </DisabledLabel>) }));
        };
        _this.createMentionableTeam = function (team) { return ({
            value: team.id,
            label: <IdBadge team={team}/>,
            searchKey: "#" + team.slug,
            actor: {
                type: 'team',
                id: team.id,
                name: team.slug,
            },
        }); };
        _this.createUnmentionableTeam = function (team) {
            var organization = _this.props.organization;
            var canAddTeam = organization.access.includes('project:write');
            return __assign(__assign({}, _this.createMentionableTeam(team)), { disabled: true, label: (<UnmentionableTeam>
          <DisabledLabel>
            <Tooltip position="left" title={t('%s is not a member of project', "#" + team.slug)}>
              <IdBadge team={team}/>
            </Tooltip>
          </DisabledLabel>
          <Tooltip title={canAddTeam
                    ? t('Add %s to project', "#" + team.slug)
                    : t('You do not have permission to add team to project.')}>
            <AddToProjectButton type="button" size="zero" borderless disabled={!canAddTeam} onClick={_this.handleAddTeamToProject.bind(_this, team)} icon={<IconAdd isCircled/>}/>
          </Tooltip>
        </UnmentionableTeam>) });
        };
        _this.handleChange = function (newValue) {
            _this.props.onChange(newValue);
        };
        _this.handleInputChange = function (inputValue) {
            _this.setState({ inputValue: inputValue });
            if (_this.props.onInputChange) {
                _this.props.onInputChange(inputValue);
            }
        };
        _this.queryMembers = debounce(function (query, cb) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            // Because this function is debounced, the component can potentially be
            // unmounted before this fires, in which case, `api` is null
            if (!api) {
                return null;
            }
            return api
                .requestPromise("/organizations/" + organization.slug + "/members/", {
                query: { query: query },
            })
                .then(function (data) { return cb(null, data); }, function (err) { return cb(err); });
        }, 250);
        _this.handleLoadOptions = function () {
            if (_this.props.showTeam) {
                var teamsInProject = _this.getMentionableTeams();
                var teamsNotInProject = _this.getTeamsNotInProject(teamsInProject);
                var options = __spread(teamsInProject, teamsNotInProject);
                _this.setState({ options: options });
                return Promise.resolve(options);
            }
            var usersInProject = _this.getMentionableUsers();
            var usersInProjectById = usersInProject.map(function (_a) {
                var actor = _a.actor;
                return actor.id;
            });
            // Return a promise for `react-select`
            return new Promise(function (resolve, reject) {
                _this.queryMembers(_this.state.inputValue, function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            })
                .then(function (members) {
                // Be careful here as we actually want the `users` object, otherwise it means user
                // has not registered for sentry yet, but has been invited
                return (members
                    ? members
                        .filter(function (_a) {
                        var user = _a.user;
                        return user && usersInProjectById.indexOf(user.id) === -1;
                    })
                        .map(_this.createUnmentionableUser)
                    : []);
            })
                .then(function (members) {
                var options = __spread(usersInProject, members);
                _this.setState({ options: options });
                return options;
            });
        };
        return _this;
    }
    SelectMembers.prototype.componentWillUnmount = function () {
        this.unlisteners.forEach(callIfFunction);
    };
    SelectMembers.prototype.getMentionableUsers = function () {
        return MemberListStore.getAll().map(this.createMentionableUser);
    };
    SelectMembers.prototype.getMentionableTeams = function () {
        var project = this.props.project;
        var projectData = project && ProjectsStore.getBySlug(project.slug);
        if (!projectData) {
            return [];
        }
        return projectData.teams.map(this.createMentionableTeam);
    };
    /**
     * Get list of teams that are not in the current project, for use in `MultiSelectMenu`
     *
     * @param {Team[]} teamsInProject A list of teams that are in the current project
     */
    SelectMembers.prototype.getTeamsNotInProject = function (teamsInProject) {
        if (teamsInProject === void 0) { teamsInProject = []; }
        var teams = TeamStore.getAll() || [];
        var excludedTeamIds = teamsInProject.map(function (_a) {
            var actor = _a.actor;
            return actor.id;
        });
        return teams
            .filter(function (team) { return excludedTeamIds.indexOf(team.id) === -1; })
            .map(this.createUnmentionableTeam);
    };
    /**
     * Closes the select menu by blurring input if possible since that seems to be the only
     * way to close it.
     */
    SelectMembers.prototype.closeSelectMenu = function () {
        if (!this.selectRef.current) {
            return;
        }
        var select = this.selectRef.current.select.select;
        var input = select.inputRef;
        if (input) {
            // I don't think there's another way to close `react-select`
            input.blur();
        }
    };
    SelectMembers.prototype.handleAddTeamToProject = function (team) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, project, value, options, oldValue, newOptions, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, value = _a.value;
                        options = this.state.options;
                        oldValue = __spread(value);
                        // Optimistic update
                        this.props.onChange(this.createMentionableTeam(team));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 4, , 5]);
                        if (!project) return [3 /*break*/, 3];
                        return [4 /*yield*/, addTeamToProject(api, organization.slug, project.slug, team)];
                    case 2:
                        _b.sent();
                        newOptions = options.map(function (option) {
                            if (option.actor.id === team.id) {
                                option.disabled = false;
                                option.label = <IdBadge team={team}/>;
                            }
                            return option;
                        });
                        this.setState({ options: newOptions });
                        _b.label = 3;
                    case 3: return [3 /*break*/, 5];
                    case 4:
                        err_1 = _b.sent();
                        // Unable to add team to project, revert select menu value
                        this.props.onChange(oldValue);
                        return [3 /*break*/, 5];
                    case 5:
                        this.closeSelectMenu();
                        return [2 /*return*/];
                }
            });
        });
    };
    SelectMembers.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, placeholder = _b.placeholder, styles = _b.styles;
        // If memberList is still loading we need to disable a placeholder Select,
        // otherwise `react-select` will call `loadOptions` and prematurely load
        // options
        if (this.state.memberListLoading) {
            return <StyledSelectControl isDisabled placeholder={t('Loading')}/>;
        }
        return (<StyledSelectControl ref={this.selectRef} filterOption={function (option, filterText) { var _a, _b; return ((_b = (_a = option === null || option === void 0 ? void 0 : option.data) === null || _a === void 0 ? void 0 : _a.searchKey) === null || _b === void 0 ? void 0 : _b.indexOf(filterText)) > -1; }} loadOptions={this.handleLoadOptions} isOptionDisabled={function (option) { return option.disabled; }} defaultOptions async isDisabled={this.props.disabled} cacheOptions={false} placeholder={placeholder} onInputChange={this.handleInputChange} onChange={this.handleChange} value={(_a = this.state.options) === null || _a === void 0 ? void 0 : _a.find(function (_a) {
            var value = _a.value;
            return value === _this.props.value;
        })} styles={styles}/>);
    };
    return SelectMembers;
}(React.Component));
var DisabledLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"], ["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"])));
var AddToProjectButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var UnmentionableTeam = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: flex-end;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: flex-end;\n"])));
var StyledSelectControl = styled(SelectControl)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  .Select-value {\n    display: flex;\n    align-items: center;\n  }\n  .Select-input {\n    margin-left: 32px;\n  }\n"], ["\n  .Select-value {\n    display: flex;\n    align-items: center;\n  }\n  .Select-input {\n    margin-left: 32px;\n  }\n"])));
export default withApi(SelectMembers);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map