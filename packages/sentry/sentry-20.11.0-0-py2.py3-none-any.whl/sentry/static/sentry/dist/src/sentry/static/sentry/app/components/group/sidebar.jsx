import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import isObject from 'lodash/isObject';
import keyBy from 'lodash/keyBy';
import pickBy from 'lodash/pickBy';
import styled from '@emotion/styled';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import ErrorBoundary from 'app/components/errorBoundary';
import ExternalIssueList from 'app/components/group/externalIssuesList';
import GroupParticipants from 'app/components/group/participants';
import GroupReleaseStats from 'app/components/group/releaseStats';
import GroupTagDistributionMeter from 'app/components/group/tagDistributionMeter';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import LoadingError from 'app/components/loadingError';
import Placeholder from 'app/components/placeholder';
import SuggestedOwners from 'app/components/group/suggestedOwners/suggestedOwners';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import SidebarSection from './sidebarSection';
var GroupSidebar = /** @class */ (function (_super) {
    __extends(GroupSidebar, _super);
    function GroupSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            participants: [],
            environments: _this.props.environments,
        };
        return _this;
    }
    GroupSidebar.prototype.componentDidMount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, group, api, allEnvironmentsGroupData, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, group = _a.group, api = _a.api;
                        this.fetchParticipants();
                        this.fetchTagData();
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/")];
                    case 2:
                        allEnvironmentsGroupData = _c.sent();
                        // eslint-disable-next-line react/no-did-mount-set-state
                        this.setState({
                            allEnvironmentsGroupData: allEnvironmentsGroupData,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        // eslint-disable-next-line react/no-did-mount-set-state
                        this.setState({
                            error: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (!isEqual(nextProps.environments, this.props.environments)) {
            this.setState({ environments: nextProps.environments }, this.fetchTagData);
        }
    };
    GroupSidebar.prototype.fetchParticipants = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, group, api, participants, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, group = _a.group, api = _a.api;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/participants/")];
                    case 2:
                        participants = _c.sent();
                        this.setState({
                            participants: participants,
                            error: false,
                        });
                        return [2 /*return*/, participants];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            error: true,
                        });
                        return [2 /*return*/, []];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.fetchTagData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, group, data, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/tags/", {
                                query: pickBy({
                                    key: group.tags.map(function (tag) { return tag.key; }),
                                    environment: this.state.environments.map(function (env) { return env.name; }),
                                }),
                            })];
                    case 2:
                        data = _c.sent();
                        this.setState({ tagsWithTopValues: keyBy(data, 'key') });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            tagsWithTopValues: {},
                            error: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.toggleSubscription = function () {
        var _this = this;
        var _a = this.props, api = _a.api, group = _a.group, project = _a.project, organization = _a.organization;
        addLoadingMessage(t('Saving changes\u2026'));
        // Typecasting to make TS happy
        var groupId = Number(group.id);
        if (isNaN(groupId)) {
            this.setState({ error: true });
            return;
        }
        api.bulkUpdate({
            orgId: organization.slug,
            projectId: project.slug,
            itemIds: [groupId],
            data: {
                isSubscribed: !group.isSubscribed,
            },
        }, {
            complete: function () { return __awaiter(_this, void 0, void 0, function () {
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.fetchParticipants()];
                        case 1:
                            _a.sent();
                            clearIndicators();
                            return [2 /*return*/];
                    }
                });
            }); },
        });
    };
    GroupSidebar.prototype.renderPluginIssue = function () {
        var issues = [];
        (this.props.group.pluginIssues || []).forEach(function (plugin) {
            var issue = plugin.issue;
            // # TODO(dcramer): remove plugin.title check in Sentry 8.22+
            if (issue) {
                issues.push(<React.Fragment key={plugin.slug}>
            <span>{(plugin.shortName || plugin.name || plugin.title) + ": "}</span>
            <a href={issue.url}>{isObject(issue.label) ? issue.label.id : issue.label}</a>
          </React.Fragment>);
            }
        });
        if (!issues.length) {
            return null;
        }
        return (<SidebarSection title={t('External Issues')}>
        <ExternalIssues>{issues}</ExternalIssues>
      </SidebarSection>);
    };
    GroupSidebar.prototype.renderParticipantData = function () {
        var _a = this.state, error = _a.error, _b = _a.participants, participants = _b === void 0 ? [] : _b;
        if (error) {
            return (<LoadingError message={t('There was an error while trying to load participants.')}/>);
        }
        return participants.length !== 0 && <GroupParticipants participants={participants}/>;
    };
    GroupSidebar.prototype.render = function () {
        var _a = this.props, className = _a.className, event = _a.event, group = _a.group, organization = _a.organization, project = _a.project, environments = _a.environments;
        var _b = this.state, allEnvironmentsGroupData = _b.allEnvironmentsGroupData, tagsWithTopValues = _b.tagsWithTopValues;
        var projectId = project.slug;
        return (<div className={className}>
        {event && <SuggestedOwners project={project} group={group} event={event}/>}

        <GroupReleaseStats organization={organization} project={project} environments={environments} allEnvironments={allEnvironmentsGroupData} group={group}/>

        {event && (<ErrorBoundary mini>
            <ExternalIssueList project={project} group={group} event={event}/>
          </ErrorBoundary>)}

        {this.renderPluginIssue()}

        <SidebarSection title={<GuideAnchor target="tags" position="bottom">
              {t('Tags')}
            </GuideAnchor>}>
          {!tagsWithTopValues ? (<TagPlaceholders>
              <Placeholder height="40px"/>
              <Placeholder height="40px"/>
              <Placeholder height="40px"/>
              <Placeholder height="40px"/>
            </TagPlaceholders>) : (group.tags.map(function (tag) {
            var tagWithTopValues = tagsWithTopValues[tag.key];
            var topValues = tagWithTopValues ? tagWithTopValues.topValues : [];
            var topValuesTotal = tagWithTopValues ? tagWithTopValues.totalValues : 0;
            return (<GroupTagDistributionMeter key={tag.key} tag={tag.key} totalValues={topValuesTotal} topValues={topValues} name={tag.name} organization={organization} projectId={projectId} group={group}/>);
        }))}
          {group.tags.length === 0 && (<p data-test-id="no-tags">
              {environments.length
            ? t('No tags found in the selected environments')
            : t('No tags found')}
            </p>)}
        </SidebarSection>

        {this.renderParticipantData()}
      </div>);
    };
    return GroupSidebar;
}(React.Component));
var TagPlaceholders = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: row;\n"], ["\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: row;\n"])), space(1));
var StyledGroupSidebar = styled(GroupSidebar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ExternalIssues = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  gap: ", ";\n"])), space(2));
export default withApi(StyledGroupSidebar);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sidebar.jsx.map