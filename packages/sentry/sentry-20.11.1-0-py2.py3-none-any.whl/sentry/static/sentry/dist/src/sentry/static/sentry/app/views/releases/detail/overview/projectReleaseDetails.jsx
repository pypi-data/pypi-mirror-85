import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import Version from 'app/components/version';
import TimeSince from 'app/components/timeSince';
import DateTime from 'app/components/dateTime';
import Link from 'app/components/links/link';
import Count from 'app/components/count';
import { SectionHeading, Wrapper } from './styles';
var ProjectReleaseDetails = function (_a) {
    var release = _a.release, releaseMeta = _a.releaseMeta, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
    var version = release.version, dateCreated = release.dateCreated, firstEvent = release.firstEvent, lastEvent = release.lastEvent;
    return (<Wrapper>
      <SectionHeading>{t('Project Release Details')}</SectionHeading>
      <StyledTable>
        <tbody>
          <StyledTr>
            <TagKey>{t('Created')}</TagKey>
            <TagValue>
              <DateTime date={dateCreated} seconds={false}/>
            </TagValue>
          </StyledTr>

          <StyledTr>
            <TagKey>{t('Version')}</TagKey>
            <TagValue>
              <Version version={version} anchor={false}/>
            </TagValue>
          </StyledTr>

          <StyledTr>
            <TagKey>{t('First Event')}</TagKey>
            <TagValue>{firstEvent ? <TimeSince date={firstEvent}/> : '-'}</TagValue>
          </StyledTr>

          <StyledTr>
            <TagKey>{t('Last Event')}</TagKey>
            <TagValue>{lastEvent ? <TimeSince date={lastEvent}/> : '-'}</TagValue>
          </StyledTr>

          <StyledTr>
            <TagKey>{t('Source Maps')}</TagKey>
            <TagValue>
              <Link to={"/settings/" + orgSlug + "/projects/" + projectSlug + "/source-maps/" + encodeURIComponent(version) + "/"}>
                <Count value={releaseMeta.releaseFileCount}/>{' '}
                {tn('artifact', 'artifacts', releaseMeta.releaseFileCount)}
              </Link>
            </TagValue>
          </StyledTr>
        </tbody>
      </StyledTable>
    </Wrapper>);
};
var StyledTable = styled('table')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  table-layout: fixed;\n  width: 100%;\n  max-width: 100%;\n"], ["\n  table-layout: fixed;\n  width: 100%;\n  max-width: 100%;\n"])));
var StyledTr = styled('tr')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  &:nth-child(2n + 1) td {\n    background-color: ", ";\n  }\n"], ["\n  &:nth-child(2n + 1) td {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; });
var TagKey = styled('td')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.textColor; }, space(0.5), space(1), function (p) { return p.theme.fontSizeMedium; });
var TagValue = styled(TagKey)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: right;\n  color: ", ";\n  @media (min-width: ", ") {\n    width: 160px;\n  }\n"], ["\n  text-align: right;\n  color: ", ";\n  @media (min-width: ", ") {\n    width: 160px;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.breakpoints[0]; });
export default ProjectReleaseDetails;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectReleaseDetails.jsx.map