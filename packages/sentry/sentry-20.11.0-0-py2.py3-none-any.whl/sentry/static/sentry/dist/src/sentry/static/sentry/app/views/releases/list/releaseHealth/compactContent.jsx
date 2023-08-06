import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { PanelBody } from 'app/components/panels';
import space from 'app/styles/space';
import ClippedHealthRows from '../clippedHealthRows';
import Header from './header';
import Item from './item';
import ProjectName from './projectName';
import IssuesQuantity from './issuesQuantity';
var CompactContent = function (_a) {
    var projects = _a.projects, releaseVersion = _a.releaseVersion, orgSlug = _a.orgSlug;
    return (<React.Fragment>
    <Header>{t('Projects')}</Header>
    <PanelBody>
      <StyledClippedHealthRows maxVisibleItems={12}>
        {projects.map(function (project) {
        var id = project.id, slug = project.slug, _a = project.newGroups, newGroups = _a === void 0 ? 0 : _a;
        return (<StyledItem key={releaseVersion + "-" + slug + "-health"}>
              <ProjectName orgSlug={orgSlug} project={project} releaseVersion={releaseVersion}/>
              <IssuesQuantity orgSlug={orgSlug} releaseVersion={releaseVersion} projectId={id} newGroups={newGroups} isCompact/>
            </StyledItem>);
    })}
      </StyledClippedHealthRows>
    </PanelBody>
  </React.Fragment>);
};
export default CompactContent;
var StyledItem = styled(Item)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  border-right: 1px solid ", ";\n  display: grid;\n  grid-template-columns: minmax(100px, max-content) auto;\n  grid-column-gap: ", ";\n  justify-content: space-between;\n  :last-child {\n    border-right: 1px solid ", ";\n  }\n"], ["\n  align-items: center;\n  border-right: 1px solid ", ";\n  display: grid;\n  grid-template-columns: minmax(100px, max-content) auto;\n  grid-column-gap: ", ";\n  justify-content: space-between;\n  :last-child {\n    border-right: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; }, space(2), function (p) { return p.theme.border; });
var StyledClippedHealthRows = styled(ClippedHealthRows)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  margin-right: -1px;\n  margin-bottom: -1px;\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  margin-right: -1px;\n  margin-bottom: -1px;\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=compactContent.jsx.map