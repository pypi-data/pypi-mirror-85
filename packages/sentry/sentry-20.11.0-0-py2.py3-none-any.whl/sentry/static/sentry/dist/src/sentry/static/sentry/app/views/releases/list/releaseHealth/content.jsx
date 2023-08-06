import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PanelBody } from 'app/components/panels';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import Count from 'app/components/count';
import { defined } from 'app/utils';
import theme from 'app/utils/theme';
import ScoreBar from 'app/components/scoreBar';
import Tooltip from 'app/components/tooltip';
import TextOverflow from 'app/components/textOverflow';
import Placeholder from 'app/components/placeholder';
import Link from 'app/components/links/link';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import HealthStatsChart from '../healthStatsChart';
import { convertAdoptionToProgress, getReleaseNewIssuesUrl } from '../../utils';
import HealthStatsSubject from '../healthStatsSubject';
import HealthStatsPeriod from '../healthStatsPeriod';
import AdoptionTooltip from '../adoptionTooltip';
import NotAvailable from '../notAvailable';
import ClippedHealthRows from '../clippedHealthRows';
import CrashFree from '../crashFree';
import Header from './header';
import Item from './item';
import ProjectName from './projectName';
var Content = function (_a) {
    var projects = _a.projects, releaseVersion = _a.releaseVersion, location = _a.location, orgSlug = _a.orgSlug, showPlaceholders = _a.showPlaceholders;
    var activeStatsPeriod = (location.query.healthStatsPeriod || '24h');
    var activeStatsSubject = (location.query.healthStat || 'sessions');
    return (<React.Fragment>
      <Header>
        <HeaderLayout>
          <ProjectColumn>{t('Project name')}</ProjectColumn>
          <AdoptionColumn>{t('Release adoption')}</AdoptionColumn>
          <CrashFreeUsersColumn>{t('Crash free users')}</CrashFreeUsersColumn>
          <CrashFreeSessionsColumn>{t('Crash free sessions')}</CrashFreeSessionsColumn>
          <DailyUsersColumn>
            <HealthStatsSubject location={location} activeSubject={activeStatsSubject}/>
            <HealthStatsPeriod location={location} activePeriod={activeStatsPeriod}/>
          </DailyUsersColumn>
          <CrashesColumn>{t('Crashes')}</CrashesColumn>
          <NewIssuesColumn>{t('New Issues')}</NewIssuesColumn>
        </HeaderLayout>
      </Header>

      <PanelBody>
        <StyledClippedHealthRows>
          {projects.map(function (project) {
        var slug = project.slug, healthData = project.healthData, newGroups = project.newGroups;
        var _a = healthData || {}, hasHealthData = _a.hasHealthData, adoption = _a.adoption, stats = _a.stats, crashFreeUsers = _a.crashFreeUsers, crashFreeSessions = _a.crashFreeSessions, sessionsCrashed = _a.sessionsCrashed, totalUsers = _a.totalUsers, totalUsers24h = _a.totalUsers24h, totalSessions = _a.totalSessions, totalSessions24h = _a.totalSessions24h;
        return (<Item key={releaseVersion + "-" + slug + "-health"}>
                <Layout>
                  <ProjectColumn>
                    <ProjectName orgSlug={orgSlug} project={project} releaseVersion={releaseVersion}/>
                  </ProjectColumn>

                  <AdoptionColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="150px"/>) : defined(adoption) ? (<AdoptionWrapper>
                        <Tooltip title={<AdoptionTooltip totalUsers={totalUsers} totalSessions={totalSessions} totalUsers24h={totalUsers24h} totalSessions24h={totalSessions24h}/>}>
                          <StyledScoreBar score={convertAdoptionToProgress(adoption)} size={20} thickness={5} radius={0} palette={Array(10).fill(theme.purple300)}/>
                        </Tooltip>
                        <TextOverflow>
                          <Count value={totalUsers24h !== null && totalUsers24h !== void 0 ? totalUsers24h : 0}/>{' '}
                          {tn('user', 'users', totalUsers24h)}
                        </TextOverflow>
                      </AdoptionWrapper>) : (<NotAvailable />)}
                  </AdoptionColumn>

                  <CrashFreeUsersColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeUsers) ? (<CrashFree percent={crashFreeUsers}/>) : (<NotAvailable />)}
                  </CrashFreeUsersColumn>

                  <CrashFreeSessionsColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeSessions) ? (<CrashFree percent={crashFreeSessions}/>) : (<NotAvailable />)}
                  </CrashFreeSessionsColumn>

                  <DailyUsersColumn>
                    {showPlaceholders ? (<StyledPlaceholder />) : hasHealthData && defined(stats) ? (<ChartWrapper>
                        <HealthStatsChart data={stats} height={20} period={activeStatsPeriod} subject={activeStatsSubject}/>
                      </ChartWrapper>) : (<NotAvailable />)}
                  </DailyUsersColumn>

                  <CrashesColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : hasHealthData && defined(sessionsCrashed) ? (<Count value={sessionsCrashed}/>) : (<NotAvailable />)}
                  </CrashesColumn>

                  <NewIssuesColumn>
                    <Tooltip title={t('Open in Issues')}>
                      <Link to={getReleaseNewIssuesUrl(orgSlug, project.id, releaseVersion)}>
                        <Count value={newGroups || 0}/>
                      </Link>
                    </Tooltip>
                  </NewIssuesColumn>
                </Layout>
              </Item>);
    })}
        </StyledClippedHealthRows>
      </PanelBody>
    </React.Fragment>);
};
export default Content;
var StyledClippedHealthRows = styled(ClippedHealthRows)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -1px;\n"], ["\n  margin-bottom: -1px;\n"])));
var Layout = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-areas: 'project adoption crash-free-users crash-free-sessions daily-users crashes new-issues';\n  grid-template-columns: 2fr 2fr 1.4fr 1.4fr 2.1fr 0.7fr 0.8fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'project adoption crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-sessions new-issues';\n    grid-template-columns: 2fr 1.6fr 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-areas: 'project adoption crash-free-users crash-free-sessions daily-users crashes new-issues';\n  grid-template-columns: 2fr 2fr 1.4fr 1.4fr 2.1fr 0.7fr 0.8fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'project adoption crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-sessions new-issues';\n    grid-template-columns: 2fr 1.6fr 1fr;\n  }\n"])), space(1.5), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[0]; });
var HeaderLayout = styled(Layout)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: flex-end;\n"], ["\n  align-items: flex-end;\n"])));
var Column = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var RightColumn = styled(Column)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var CenterColumn = styled(Column)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: center;\n"], ["\n  text-align: center;\n"])));
var ProjectColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: project;\n"], ["\n  grid-area: project;\n"])));
var DailyUsersColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: daily-users;\n  display: flex;\n  align-items: flex-end;\n  /* Chart tooltips need overflow */\n  overflow: visible;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: daily-users;\n  display: flex;\n  align-items: flex-end;\n  /* Chart tooltips need overflow */\n  overflow: visible;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var AdoptionColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-area: adoption;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: adoption;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var CrashFreeUsersColumn = styled(CenterColumn)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  grid-area: crash-free-users;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: crash-free-users;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[0]; });
var CrashFreeSessionsColumn = styled(CenterColumn)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  grid-area: crash-free-sessions;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"], ["\n  grid-area: crash-free-sessions;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var CrashesColumn = styled(RightColumn)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  grid-area: crashes;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: crashes;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var NewIssuesColumn = styled(RightColumn)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  grid-area: new-issues;\n"], ["\n  grid-area: new-issues;\n"])));
var AdoptionWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n"])));
var StyledScoreBar = styled(ScoreBar)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ChartWrapper = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"], ["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var StyledPlaceholder = styled(Placeholder)(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"], ["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=content.jsx.map