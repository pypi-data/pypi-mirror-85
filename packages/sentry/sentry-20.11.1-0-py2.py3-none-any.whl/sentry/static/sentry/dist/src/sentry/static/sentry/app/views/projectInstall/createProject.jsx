import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import PlatformIcon from 'platformicons';
import { inputStyles } from 'app/styles/input';
import { openCreateTeamModal } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import PageHeading from 'app/components/pageHeading';
import PlatformPicker from 'app/components/platformPicker';
import ProjectActions from 'app/actions/projectActions';
import SelectControl from 'app/components/forms/selectControl';
import Tooltip from 'app/components/tooltip';
import getPlatformName from 'app/utils/getPlatformName';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withTeams from 'app/utils/withTeams';
import IssueAlertOptions from 'app/views/projectInstall/issueAlertOptions';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import slugify from 'app/utils/slugify';
import { IconAdd } from 'app/icons';
var CreateProject = /** @class */ (function (_super) {
    __extends(CreateProject, _super);
    function CreateProject(props) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        var _this = _super.apply(this, __spread([props], args)) || this;
        _this.createProject = function (e) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, api, _b, projectName, platform, team, dataFragment, slug, _c, shouldCreateCustomRule, name, conditions, actions, actionMatch, frequency, defaultRules, projectData, ruleId, ruleData, platformKey, nextUrl, err_1;
            var _this = this;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        e.preventDefault();
                        _a = this.props, organization = _a.organization, api = _a.api;
                        _b = this.state, projectName = _b.projectName, platform = _b.platform, team = _b.team, dataFragment = _b.dataFragment;
                        slug = organization.slug;
                        _c = dataFragment || {}, shouldCreateCustomRule = _c.shouldCreateCustomRule, name = _c.name, conditions = _c.conditions, actions = _c.actions, actionMatch = _c.actionMatch, frequency = _c.frequency, defaultRules = _c.defaultRules;
                        this.setState({ inFlight: true });
                        if (!projectName) {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('No project name');
                            });
                        }
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 5, , 6]);
                        return [4 /*yield*/, api.requestPromise("/teams/" + slug + "/" + team + "/projects/", {
                                method: 'POST',
                                data: {
                                    name: projectName,
                                    platform: platform,
                                    default_rules: defaultRules !== null && defaultRules !== void 0 ? defaultRules : true,
                                },
                            })];
                    case 2:
                        projectData = _d.sent();
                        ruleId = void 0;
                        if (!shouldCreateCustomRule) return [3 /*break*/, 4];
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectData.slug + "/rules/", {
                                method: 'POST',
                                data: {
                                    name: name,
                                    conditions: conditions,
                                    actions: actions,
                                    actionMatch: actionMatch,
                                    frequency: frequency,
                                },
                            })];
                    case 3:
                        ruleData = _d.sent();
                        ruleId = ruleData.id;
                        _d.label = 4;
                    case 4:
                        this.trackIssueAlertOptionSelectedEvent(projectData, defaultRules, shouldCreateCustomRule, ruleId);
                        ProjectActions.createSuccess(projectData);
                        platformKey = platform || 'other';
                        nextUrl = "/" + organization.slug + "/" + projectData.slug + "/getting-started/" + platformKey + "/";
                        browserHistory.push(nextUrl);
                        return [3 /*break*/, 6];
                    case 5:
                        err_1 = _d.sent();
                        this.setState({
                            inFlight: false,
                            error: err_1.responseJSON.detail,
                        });
                        // Only log this if the error is something other than:
                        // * The user not having access to create a project, or,
                        // * A project with that slug already exists
                        if (err_1.status !== 403 && err_1.status !== 409) {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('err', err_1);
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('Project creation failed');
                            });
                        }
                        return [3 /*break*/, 6];
                    case 6: return [2 /*return*/];
                }
            });
        }); };
        _this.setPlatform = function (platformId) {
            return _this.setState(function (_a) {
                var projectName = _a.projectName, platform = _a.platform;
                return ({
                    platform: platformId,
                    projectName: !projectName || (platform && getPlatformName(platform) === projectName)
                        ? getPlatformName(platformId) || ''
                        : projectName,
                });
            });
        };
        var query = _this.context.location.query;
        var teams = props.organization.teams;
        var accessTeams = teams.filter(function (team) { return team.hasAccess; });
        var team = query.team || (accessTeams.length && accessTeams[0].slug);
        var platform = getPlatformName(query.platform) ? query.platform : '';
        _this.state = {
            error: false,
            projectName: getPlatformName(platform) || '',
            team: team,
            platform: platform,
            inFlight: false,
            dataFragment: undefined,
        };
        return _this;
    }
    CreateProject.prototype.renderProjectForm = function () {
        var _this = this;
        var organization = this.props.organization;
        var _a = this.state, projectName = _a.projectName, platform = _a.platform, team = _a.team;
        var teams = this.props.teams.filter(function (filterTeam) { return filterTeam.hasAccess; });
        var createProjectForm = (<CreateProjectForm onSubmit={this.createProject}>
        <div>
          <FormLabel>{t('Project name')}</FormLabel>
          <ProjectNameInput theme={theme}>
            <StyledPlatformIcon platform={platform}/>
            <input type="text" name="name" placeholder={t('Project name')} autoComplete="off" value={projectName} onChange={function (e) { return _this.setState({ projectName: slugify(e.target.value) }); }}/>
          </ProjectNameInput>
        </div>
        <div>
          <FormLabel>{t('Team')}</FormLabel>
          <TeamSelectInput>
            <SelectControl deprecatedSelectControl name="select-team" clearable={false} value={team} placeholder={t('Select a Team')} onChange={function (choice) { return _this.setState({ team: choice.value }); }} options={teams.map(function (_a) {
            var slug = _a.slug;
            return ({
                label: "#" + slug,
                value: slug,
            });
        })}/>
            <Tooltip title={t('Create a team')}>
              <Button borderless data-test-id="create-team" type="button" icon={<IconAdd isCircled/>} onClick={function () {
            return openCreateTeamModal({
                organization: organization,
                onClose: function (_a) {
                    var slug = _a.slug;
                    return _this.setState({ team: slug });
                },
            });
        }}/>
            </Tooltip>
          </TeamSelectInput>
        </div>
        <div>
          <Button data-test-id="create-project" priority="primary" disabled={!this.canSubmitForm}>
            {t('Create Project')}
          </Button>
        </div>
      </CreateProjectForm>);
        return (<React.Fragment>
        <PageHeading withMargins>{t('Give your project a name')}</PageHeading>
        {createProjectForm}
      </React.Fragment>);
    };
    Object.defineProperty(CreateProject.prototype, "canSubmitForm", {
        get: function () {
            var _a;
            var _b = this.state, projectName = _b.projectName, team = _b.team, inFlight = _b.inFlight;
            var _c = this.state.dataFragment || {}, shouldCreateCustomRule = _c.shouldCreateCustomRule, conditions = _c.conditions;
            return (!inFlight &&
                team &&
                projectName !== '' &&
                (!shouldCreateCustomRule || ((_a = conditions === null || conditions === void 0 ? void 0 : conditions.every) === null || _a === void 0 ? void 0 : _a.call(conditions, function (condition) { return condition.value; }))));
        },
        enumerable: false,
        configurable: true
    });
    CreateProject.prototype.trackIssueAlertOptionSelectedEvent = function (projectData, isDefaultRules, shouldCreateCustomRule, ruleId) {
        var organization = this.props.organization;
        var data = {
            eventKey: 'new_project.alert_rule_selected',
            eventName: 'New Project Alert Rule Selected',
            organization_id: organization.id,
            project_id: projectData.id,
            rule_type: isDefaultRules
                ? 'Default'
                : shouldCreateCustomRule
                    ? 'Custom'
                    : 'No Rule',
        };
        if (ruleId !== undefined) {
            data = __assign(__assign({}, data), { custom_rule_id: ruleId });
        }
        trackAnalyticsEvent(data);
    };
    CreateProject.prototype.render = function () {
        var _this = this;
        var _a = this.state, platform = _a.platform, error = _a.error;
        return (<React.Fragment>
        {error && <Alert type="error">{error}</Alert>}

        <div data-test-id="onboarding-info">
          <PageHeading withMargins>{t('Create a new Project')}</PageHeading>
          <HelpText>
            {t("Projects allow you to scope events to a specific application in\n               your organization. For example, you might have separate projects\n               for your API server and frontend client.")}
          </HelpText>
          <PageHeading withMargins>{t('Choose a platform')}</PageHeading>
          <PlatformPicker platform={platform} setPlatform={this.setPlatform} showOther/>
          <IssueAlertOptions onChange={function (updatedData) {
            _this.setState({ dataFragment: updatedData });
        }}/>
          {this.renderProjectForm()}
        </div>
      </React.Fragment>);
    };
    CreateProject.contextTypes = {
        location: PropTypes.object,
    };
    return CreateProject;
}(React.Component));
export default withApi(withTeams(withOrganization(CreateProject)));
export { CreateProject };
var CreateProjectForm = styled('form')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 300px 250px max-content;\n  grid-gap: ", ";\n  align-items: end;\n  padding: ", " 0;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n  background: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 300px 250px max-content;\n  grid-gap: ", ";\n  align-items: end;\n  padding: ", " 0;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n  background: ", ";\n"])), space(2), space(3), function (p) { return p.theme.background; });
var FormLabel = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ProjectNameInput = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n  padding: 5px 10px;\n  display: flex;\n  align-items: center;\n\n  input {\n    border: 0;\n    outline: 0;\n    flex: 1;\n  }\n"], ["\n  ", ";\n  padding: 5px 10px;\n  display: flex;\n  align-items: center;\n\n  input {\n    border: 0;\n    outline: 0;\n    flex: 1;\n  }\n"])), inputStyles);
var TeamSelectInput = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n  align-items: center;\n"])));
var HelpText = styled('p')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  max-width: 700px;\n"], ["\n  color: ", ";\n  max-width: 700px;\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=createProject.jsx.map