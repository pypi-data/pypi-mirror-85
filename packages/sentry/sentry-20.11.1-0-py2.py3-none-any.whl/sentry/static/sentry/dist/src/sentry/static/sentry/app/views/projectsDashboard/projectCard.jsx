import { __assign, __extends, __makeTemplateObject, __read, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import styled from '@emotion/styled';
import BookmarkStar from 'app/components/projects/bookmarkStar';
import { loadStatsForProject } from 'app/actionCreators/projects';
import { t, tn } from 'app/locale';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import ProjectsStatsStore from 'app/stores/projectsStatsStore';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withApi from 'app/utils/withApi';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import QuestionTooltip from 'app/components/questionTooltip';
import Chart from './chart';
import Deploys from './deploys';
var ProjectCard = /** @class */ (function (_super) {
    __extends(ProjectCard, _super);
    function ProjectCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectCard.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, api = _a.api;
        // fetch project stats
        loadStatsForProject(api, project.id, {
            orgId: organization.slug,
            projectId: project.id,
            query: {
                transactionStats: this.hasPerformance ? '1' : undefined,
            },
        });
    };
    Object.defineProperty(ProjectCard.prototype, "hasPerformance", {
        get: function () {
            return this.props.organization.features.includes('performance-view');
        },
        enumerable: false,
        configurable: true
    });
    ProjectCard.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, hasProjectAccess = _a.hasProjectAccess;
        var id = project.id, stats = project.stats, slug = project.slug, transactionStats = project.transactionStats;
        var totalErrors = stats !== undefined
            ? formatAbbreviatedNumber(stats.reduce(function (sum, _a) {
                var _b = __read(_a, 2), _ = _b[0], value = _b[1];
                return sum + value;
            }, 0))
            : '0';
        var totalTransactions = transactionStats !== undefined
            ? formatAbbreviatedNumber(transactionStats.reduce(function (sum, _a) {
                var _b = __read(_a, 2), _ = _b[0], value = _b[1];
                return sum + value;
            }, 0))
            : '0';
        var zeroTransactions = totalTransactions === '0';
        var hasFirstEvent = Boolean(project.firstEvent || project.firstTransactionEvent);
        return (<div data-test-id={slug}>
        {stats ? (<StyledProjectCard>
            <CardHeader>
              <HeaderRow>
                <StyledIdBadge project={project} avatarSize={18} displayName={hasProjectAccess ? (<Link to={"/organizations/" + organization.slug + "/issues/?project=" + id}>
                        <strong>{slug}</strong>
                      </Link>) : (<span>{slug}</span>)}/>
                <BookmarkStar organization={organization} project={project}/>
              </HeaderRow>
              <SummaryLinks>
                <Link data-test-id="project-errors" to={"/organizations/" + organization.slug + "/issues/?project=" + project.id}>
                  {tn('%s error', '%s errors', totalErrors)}
                </Link>
                {this.hasPerformance && (<React.Fragment>
                    <em>|</em>
                    <TransactionsLink data-test-id="project-transactions" to={"/organizations/" + organization.slug + "/performance/?project=" + project.id}>
                      {tn('%s transaction', '%s transactions', totalTransactions)}

                      {zeroTransactions && (<QuestionTooltip title={t('Click here to learn more about performance monitoring')} position="top" size="xs"/>)}
                    </TransactionsLink>
                  </React.Fragment>)}
              </SummaryLinks>
            </CardHeader>
            <ChartContainer>
              <Chart firstEvent={hasFirstEvent} stats={stats} transactionStats={transactionStats}/>
            </ChartContainer>
            <Deploys project={project}/>
          </StyledProjectCard>) : (<LoadingCard />)}
      </div>);
    };
    ProjectCard.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        project: SentryTypes.Project.isRequired,
        hasProjectAccess: PropTypes.bool,
    };
    return ProjectCard;
}(React.Component));
var ProjectCardContainer = createReactClass({
    propTypes: {
        project: SentryTypes.Project,
    },
    mixins: [Reflux.listenTo(ProjectsStatsStore, 'onProjectStoreUpdate')],
    getInitialState: function () {
        var project = this.props.project;
        var initialState = ProjectsStatsStore.getInitialState() || {};
        return {
            projectDetails: initialState[project.slug] || null,
        };
    },
    onProjectStoreUpdate: function (itemsBySlug) {
        var project = this.props.project;
        // Don't update state if we already have stats
        if (!itemsBySlug[project.slug]) {
            return;
        }
        if (itemsBySlug[project.slug] === this.state.projectDetails) {
            return;
        }
        this.setState({
            projectDetails: itemsBySlug[project.slug],
        });
    },
    render: function () {
        var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
        var projectDetails = this.state.projectDetails;
        return (<ProjectCard {...props} project={__assign(__assign({}, project), (projectDetails || {}))}/>);
    },
});
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  background: ", ";\n"], ["\n  position: relative;\n  background: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; });
var CardHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", " ", ";\n"], ["\n  margin: ", " ", ";\n"])), space(1.5), space(2));
var HeaderRow = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var StyledProjectCard = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"], ["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowLight; });
var LoadingCard = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border: 1px solid transparent;\n  background-color: ", ";\n  height: 334px;\n"], ["\n  border: 1px solid transparent;\n  background-color: ", ";\n  height: 334px;\n"])), function (p) { return p.theme.backgroundSecondary; });
var StyledIdBadge = styled(IdBadge)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n"])));
var SummaryLinks = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.formText; }, function (p) { return p.theme.subText; }, space(0.5));
var TransactionsLink = styled(Link)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"])), space(0.5));
export { ProjectCard };
export default withOrganization(withApi(ProjectCardContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=projectCard.jsx.map