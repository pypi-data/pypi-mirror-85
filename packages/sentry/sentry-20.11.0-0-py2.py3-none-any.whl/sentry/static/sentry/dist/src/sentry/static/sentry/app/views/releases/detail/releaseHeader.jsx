import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import space from 'app/styles/space';
import { t } from 'app/locale';
import Feature from 'app/components/acl/feature';
import ListLink from 'app/components/links/listLink';
import ExternalLink from 'app/components/links/externalLink';
import NavTabs from 'app/components/navTabs';
import Version from 'app/components/version';
import Clipboard from 'app/components/clipboard';
import { IconCopy, IconOpen } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import Count from 'app/components/count';
import TimeSince from 'app/components/timeSince';
import { formatVersion, formatAbbreviatedNumber } from 'app/utils/formatters';
import Breadcrumbs from 'app/components/breadcrumbs';
import DeployBadge from 'app/components/deployBadge';
import Badge from 'app/components/badge';
import * as Layout from 'app/components/layouts/thirds';
import { getTermHelp } from 'app/views/performance/data';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import ReleaseStat from './releaseStat';
import ReleaseActions from './releaseActions';
var ReleaseHeader = function (_a) {
    var location = _a.location, organization = _a.organization, releaseEventView = _a.releaseEventView, release = _a.release, project = _a.project, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    var version = release.version, newGroups = release.newGroups, url = release.url, lastDeploy = release.lastDeploy, dateCreated = release.dateCreated;
    var commitCount = releaseMeta.commitCount, commitFilesChanged = releaseMeta.commitFilesChanged, releaseFileCount = releaseMeta.releaseFileCount;
    var _b = project.healthData, hasHealthData = _b.hasHealthData, sessionsCrashed = _b.sessionsCrashed;
    var releasePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(version) + "/";
    var tabs = [
        { title: t('Overview'), to: releasePath },
        {
            title: (<React.Fragment>
          {t('Commits')} <NavTabsBadge text={formatAbbreviatedNumber(commitCount)}/>
        </React.Fragment>),
            to: releasePath + "commits/",
        },
        {
            title: (<React.Fragment>
          {t('Files Changed')}
          <NavTabsBadge text={formatAbbreviatedNumber(commitFilesChanged)}/>
        </React.Fragment>),
            to: releasePath + "files-changed/",
        },
        {
            title: (<React.Fragment>
          {t('Artifacts')}
          <NavTabsBadge text={formatAbbreviatedNumber(releaseFileCount)}/>
        </React.Fragment>),
            to: releasePath + "artifacts/",
        },
    ];
    var getCurrentTabUrl = function (path) { return ({
        pathname: path,
        query: pick(location.query, Object.values(URL_PARAM)),
    }); };
    return (<StyledHeader>
      <HeaderInfoContainer>
        <Breadcrumbs crumbs={[
        {
            to: "/organizations/" + organization.slug + "/releases/",
            label: t('Releases'),
            preserveGlobalSelection: true,
        },
        { label: formatVersion(version) },
    ]}/>

        <StatsWrapper>
          <ReleaseStat label={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Last Deploy') : t('Date Created')}>
            <DeploysWrapper>
              <TimeSince date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated}/>
              {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) && <StyledDeployBadge deploy={lastDeploy}/>}
            </DeploysWrapper>
          </ReleaseStat>
          {hasHealthData && (<ReleaseStat label={t('Crashes')} help={t('Crash means that user experienced an unhandled error')}>
              <Count value={sessionsCrashed}/>
            </ReleaseStat>)}
          <Feature features={['release-performance-views']}>
            <ReleaseStat label={t('Apdex')} help={getTermHelp(organization, 'apdex')}>
              <DiscoverQuery eventView={releaseEventView} location={location} orgSlug={organization.slug}>
                {function (_a) {
        var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
        if (isLoading || error || !tableData || tableData.data.length === 0) {
            return '\u2014';
        }
        return (<Count value={tableData.data[0][getAggregateAlias("apdex(" + organization.apdexThreshold + ")")]}/>);
    }}
              </DiscoverQuery>
            </ReleaseStat>
          </Feature>
          <ReleaseStat label={t('New Issues')}>
            <Count value={newGroups}/>
          </ReleaseStat>
          <ReleaseActions orgSlug={organization.slug} projectSlug={project.slug} release={release} releaseMeta={releaseMeta} refetchData={refetchData}/>
        </StatsWrapper>
      </HeaderInfoContainer>

      <Layout.HeaderContent>
        <ReleaseName>
          <Version version={version} anchor={false}/>

          <IconWrapper>
            <Clipboard value={version}>
              <Tooltip title={version} containerDisplayMode="flex">
                <IconCopy size="xs"/>
              </Tooltip>
            </Clipboard>
          </IconWrapper>

          {!!url && (<IconWrapper>
              <Tooltip title={url}>
                <ExternalLink href={url}>
                  <IconOpen size="xs"/>
                </ExternalLink>
              </Tooltip>
            </IconWrapper>)}
        </ReleaseName>
      </Layout.HeaderContent>

      <StyledNavTabs>
        {tabs.map(function (tab) { return (<ListLink key={tab.to} to={getCurrentTabUrl(tab.to)} isActive={function () { return tab.to === location.pathname; }}>
            {tab.title}
          </ListLink>); })}
      </StyledNavTabs>
    </StyledHeader>);
};
var StyledHeader = styled(Layout.Header)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var HeaderInfoContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    display: grid;\n    grid-column-gap: ", ";\n    grid-template-columns: 1fr 1fr;\n    margin-bottom: 0;\n    align-items: flex-start;\n  }\n"], ["\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    display: grid;\n    grid-column-gap: ", ";\n    grid-template-columns: 1fr 1fr;\n    margin-bottom: 0;\n    align-items: flex-start;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[1]; }, space(3));
var StatsWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  @media (min-width: ", ") {\n    display: grid;\n    padding: ", " 0;\n    grid-auto-flow: column;\n    grid-gap: ", ";\n  }\n  @media (min-width: ", ") {\n    justify-content: flex-end;\n    text-align: right;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  @media (min-width: ", ") {\n    display: grid;\n    padding: ", " 0;\n    grid-auto-flow: column;\n    grid-gap: ", ";\n  }\n  @media (min-width: ", ") {\n    justify-content: flex-end;\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1.5), space(4), function (p) { return p.theme.breakpoints[1]; });
var DeploysWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var StyledDeployBadge = styled(DeployBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  bottom: ", ";\n"], ["\n  margin-left: ", ";\n  bottom: ", ";\n"])), space(1), space(0.25));
var ReleaseName = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  display: flex;\n  align-items: center;\n"], ["\n  font-size: ", ";\n  color: ", ";\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; });
var IconWrapper = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"], ["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"])), space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
var StyledNavTabs = styled(NavTabs)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-bottom: 0;\n  grid-column: 1 / 2;\n"], ["\n  margin-bottom: 0;\n  grid-column: 1 / 2;\n"])));
var NavTabsBadge = styled(Badge)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default ReleaseHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=releaseHeader.jsx.map