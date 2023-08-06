import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import Count from 'app/components/count';
import Version from 'app/components/version';
import { Panel, PanelBody, PanelItem } from 'app/components/panels';
import ReleaseStats from 'app/components/releaseStats';
import TimeSince from 'app/components/timeSince';
import { t, tn } from 'app/locale';
import { AvatarListWrapper } from 'app/components/avatar/avatarList';
import TextOverflow from 'app/components/textOverflow';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import DeployBadge from 'app/components/deployBadge';
import Link from 'app/components/links/link';
import Feature from 'app/components/acl/feature';
import Tooltip from 'app/components/tooltip';
import ReleaseHealth from './releaseHealth';
import NotAvailable from './notAvailable';
import { getReleaseNewIssuesUrl } from '../utils';
var ReleaseCard = function (_a) {
    var release = _a.release, orgSlug = _a.orgSlug, location = _a.location, reloading = _a.reloading, selection = _a.selection, showHealthPlaceholders = _a.showHealthPlaceholders;
    var version = release.version, commitCount = release.commitCount, lastDeploy = release.lastDeploy, authors = release.authors, dateCreated = release.dateCreated;
    return (<StyledPanel reloading={reloading ? 1 : 0}>
      <PanelBody>
        <StyledPanelItem>
          <HeaderLayout>
            <VersionColumn>
              <ColumnTitle>{t('Release Version')}</ColumnTitle>
            </VersionColumn>

            <CreatedColumn>
              <ColumnTitle>
                {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Last Deploy') : t('Date Created')}
              </ColumnTitle>
            </CreatedColumn>

            <CommitsColumn>
              <ColumnTitle>
                {commitCount > 0
        ? [
            tn('%s commit', '%s commits', commitCount || 0),
            t('by'),
            tn('%s author', '%s authors', authors.length || 0),
        ].join(' ')
        : t('Commits')}
              </ColumnTitle>
            </CommitsColumn>

            <NewIssuesColumn>
              <ColumnTitle>{t('New issues')}</ColumnTitle>
            </NewIssuesColumn>
          </HeaderLayout>

          <Layout>
            <VersionColumn>
              <VersionWrapper>
                <Version version={version} tooltipRawVersion truncate anchor={false}/>
              </VersionWrapper>
            </VersionColumn>

            <CreatedColumn>
              <TextOverflow>
                {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) && <StyledDeployBadge deploy={lastDeploy}/>}
                <TimeSince date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated}/>
              </TextOverflow>
            </CreatedColumn>

            <CommitsColumn>
              <CommitsWrapper>
                {commitCount > 0 ? (<ReleaseStats release={release} withHeading={false}/>) : (<NotAvailable />)}
              </CommitsWrapper>
            </CommitsColumn>

            <NewIssuesColumn>
              <Feature features={['global-views']}>
                {function (_a) {
        var hasFeature = _a.hasFeature;
        return hasFeature ? (<Tooltip title={t('Open in Issues')}>
                      <Link to={getReleaseNewIssuesUrl(orgSlug, null, version)}>
                        <Count value={release.newGroups || 0}/>
                      </Link>
                    </Tooltip>) : (<Count value={release.newGroups || 0}/>);
    }}
              </Feature>
            </NewIssuesColumn>
          </Layout>
        </StyledPanelItem>
      </PanelBody>

      <ReleaseHealth release={release} orgSlug={orgSlug} location={location} showPlaceholders={showHealthPlaceholders} selection={selection}/>
    </StyledPanel>);
};
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  opacity: ", ";\n  pointer-events: ", ";\n  overflow: hidden;\n"], ["\n  opacity: ", ";\n  pointer-events: ", ";\n  overflow: hidden;\n"])), function (p) { return (p.reloading ? 0.5 : 1); }, function (p) { return (p.reloading ? 'none' : 'auto'); });
var StyledPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var Layout = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  /* 0fr a,b,c are here to match the health grid layout (offset because of gap on fewer columns) */\n  grid-template-areas: 'version created a b commits c new-issues';\n  grid-template-columns: 2fr 4.8fr 0fr 0fr 2.1fr 0fr 1.5fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created a commits b new-issues';\n    grid-template-columns: 2fr 3.5fr 0fr 2.5fr 0fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created a b new-issues';\n    grid-template-columns: 2fr 3fr 0fr 0fr 2fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created new-issues';\n    grid-template-columns: 2fr 1.6fr 1fr;\n  }\n"], ["\n  display: grid;\n  /* 0fr a,b,c are here to match the health grid layout (offset because of gap on fewer columns) */\n  grid-template-areas: 'version created a b commits c new-issues';\n  grid-template-columns: 2fr 4.8fr 0fr 0fr 2.1fr 0fr 1.5fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created a commits b new-issues';\n    grid-template-columns: 2fr 3.5fr 0fr 2.5fr 0fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created a b new-issues';\n    grid-template-columns: 2fr 3fr 0fr 0fr 2fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'version created new-issues';\n    grid-template-columns: 2fr 1.6fr 1fr;\n  }\n"])), space(1.5), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[0]; });
var HeaderLayout = styled(Layout)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-items: flex-end;\n"], ["\n  align-items: flex-end;\n"])));
var Column = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  ", " {\n    padding-left: ", ";\n  }\n"], ["\n  overflow: hidden;\n  ", " {\n    padding-left: ", ";\n  }\n"])), AvatarListWrapper, space(0.75));
var RightAlignedColumn = styled(Column)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var VersionColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: version;\n  display: flex;\n  align-items: center;\n"], ["\n  grid-area: version;\n  display: flex;\n  align-items: center;\n"])));
var CommitsColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: commits;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: commits;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var CreatedColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-area: created;\n"], ["\n  grid-area: created;\n"])));
var NewIssuesColumn = styled(RightAlignedColumn)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  grid-area: new-issues;\n"], ["\n  grid-area: new-issues;\n"])));
var ColumnTitle = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  text-transform: uppercase;\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: ", ";\n  line-height: 1.2;\n  ", ";\n"], ["\n  text-transform: uppercase;\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: ", ";\n  line-height: 1.2;\n  ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space(0.75), overflowEllipsis);
var VersionWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"], ["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"])), overflowEllipsis);
var StyledDeployBadge = styled(DeployBadge)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  position: relative;\n  bottom: ", ";\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  position: relative;\n  bottom: ", ";\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(0.25), space(1), function (p) { return p.theme.breakpoints[0]; });
var CommitsWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  position: relative;\n  bottom: ", ";\n"], ["\n  position: relative;\n  bottom: ", ";\n"])), space(0.25));
export default ReleaseCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=releaseCard.jsx.map