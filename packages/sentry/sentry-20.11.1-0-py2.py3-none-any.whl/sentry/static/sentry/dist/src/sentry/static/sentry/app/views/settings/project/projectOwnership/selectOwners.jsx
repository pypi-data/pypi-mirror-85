import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import debounce from 'lodash/debounce';
import React from 'react';
import ReactDOM from 'react-dom';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { addTeamToProject } from 'app/actionCreators/projects';
import { t } from 'app/locale';
import { buildUserId, buildTeamId } from 'app/utils';
import MemberListStore from 'app/stores/memberListStore';
import ProjectsStore from 'app/stores/projectsStore';
import TeamStore from 'app/stores/teamStore';
import IdBadge from 'app/components/idBadge';
import MultiSelectControl from 'app/components/forms/multiSelectControl';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import withProjects from 'app/utils/withProjects';
import withApi from 'app/utils/withApi';
function ValueComponent(_a) {
    var value = _a.value, onRemove = _a.onRemove;
    return (<a onClick={function () { return onRemove(value); }}>
      <ActorAvatar actor={value.actor} size={28}/>
    </a>);
}
var getSearchKeyForUser = function (user) {
    return (user.email && user.email.toLowerCase()) + " " + (user.name && user.name.toLowerCase());
};
var SelectOwners = /** @class */ (function (_super) {
    __extends(SelectOwners, _super);
    function SelectOwners() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            inputValue: '',
        };
        _this.selectRef = React.createRef();
        _this.renderUserBadge = function (user) { return (<IdBadge avatarSize={24} user={user} hideEmail useLink={false}/>); };
        _this.createMentionableUser = function (user) { return ({
            value: buildUserId(user.id),
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
            value: buildTeamId(team.id),
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
            return __assign(__assign({}, _this.createMentionableTeam(team)), { disabled: true, label: (<Container>
          <DisabledLabel>
            <Tooltip position="left" title={t('%s is not a member of project', "#" + team.slug)}>
              <IdBadge team={team}/>
            </Tooltip>
          </DisabledLabel>
          <Tooltip title={canAddTeam
                    ? t('Add %s to project', "#" + team.slug)
                    : t('You do not have permission to add team to project.')}>
            <AddToProjectButton size="zero" borderless disabled={!canAddTeam} onClick={_this.handleAddTeamToProject.bind(_this, team)} icon={<IconAdd isCircled/>}/>
          </Tooltip>
        </Container>) });
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
            // unmounted before this fires, in which case, `this.api` is null
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
            var usersInProject = _this.getMentionableUsers();
            var teamsInProject = _this.getMentionableTeams();
            var teamsNotInProject = _this.getTeamsNotInProject(teamsInProject);
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
                return members
                    ? members
                        .filter(function (_a) {
                        var user = _a.user;
                        return user && usersInProjectById.indexOf(user.id) === -1;
                    })
                        .map(_this.createUnmentionableUser)
                    : [];
            })
                .then(function (members) { return ({
                options: __spread(usersInProject, teamsInProject, teamsNotInProject, members),
            }); });
        };
        return _this;
    }
    SelectOwners.prototype.componentDidUpdate = function (prevProps) {
        // Once a team has been added to the project the menu can be closed.
        if (!isEqual(this.props.projects, prevProps.projects)) {
            this.closeSelectMenu();
        }
    };
    SelectOwners.prototype.getMentionableUsers = function () {
        return MemberListStore.getAll().map(this.createMentionableUser);
    };
    SelectOwners.prototype.getMentionableTeams = function () {
        var project = this.props.project;
        var projectData = ProjectsStore.getBySlug(project.slug);
        if (!projectData) {
            return [];
        }
        return projectData.teams.map(this.createMentionableTeam);
    };
    /**
     * Get list of teams that are not in the current project, for use in `MultiSelectMenu`
     */
    SelectOwners.prototype.getTeamsNotInProject = function (teamsInProject) {
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
    SelectOwners.prototype.closeSelectMenu = function () {
        var _a;
        // Close select menu
        if (this.selectRef.current) {
            // eslint-disable-next-line react/no-find-dom-node
            var node = ReactDOM.findDOMNode(this.selectRef.current);
            var input = (_a = node) === null || _a === void 0 ? void 0 : _a.querySelector('.Select-input input');
            if (input) {
                // I don't think there's another way to close `react-select`
                input.blur();
            }
        }
    };
    SelectOwners.prototype.handleAddTeamToProject = function (team) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, project, value, oldValue, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, value = _a.value;
                        oldValue = __spread(value);
                        // Optimistic update
                        this.props.onChange(__spread(this.props.value, [this.createMentionableTeam(team)]));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        // Try to add team to project
                        // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
                        // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
                        // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
                        // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
                        return [4 /*yield*/, addTeamToProject(api, organization.slug, project.slug, team)];
                    case 2:
                        // Try to add team to project
                        // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
                        // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
                        // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
                        // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        // Unable to add team to project, revert select menu value
                        this.props.onChange(oldValue);
                        this.closeSelectMenu();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SelectOwners.prototype.render = function () {
        return (<MultiSelectControl deprecatedSelectControl filterOptions={function (options, filterText) {
            return options.filter(function (_a) {
                var searchKey = _a.searchKey;
                return searchKey.indexOf(filterText) > -1;
            });
        }} ref={this.selectRef} loadOptions={this.handleLoadOptions} defaultOptions async clearable disabled={this.props.disabled} cache={false} valueComponent={ValueComponent} placeholder={t('owners')} onInputChange={this.handleInputChange} onChange={this.handleChange} value={this.props.value} css={{ width: 200 }}/>);
    };
    return SelectOwners;
}(React.Component));
export default withApi(withProjects(SelectOwners));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var DisabledLabel = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"], ["\n  opacity: 0.5;\n  overflow: hidden; /* Needed so that \"Add to team\" button can fit */\n"])));
var AddToProjectButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=selectOwners.jsx.map