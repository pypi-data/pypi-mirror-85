import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TimeSince from 'app/components/timeSince';
import DeployBadge from 'app/components/deployBadge';
import TextOverflow from 'app/components/textOverflow';
import { SectionHeading, Wrapper } from './styles';
var Deploys = function (_a) {
    var version = _a.version, orgSlug = _a.orgSlug, projectId = _a.projectId, deploys = _a.deploys;
    return (<Wrapper>
      <SectionHeading>{t('Deploys')}</SectionHeading>

      {deploys.map(function (deploy) { return (<Row key={deploy.id}>
          <StyledDeployBadge deploy={deploy} orgSlug={orgSlug} version={version} projectId={projectId}/>
          <TextOverflow>
            <TimeSince date={deploy.dateFinished}/>
          </TextOverflow>
        </Row>); })}
    </Wrapper>);
};
var Row = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
var StyledDeployBadge = styled(DeployBadge)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
export default Deploys;
var templateObject_1, templateObject_2;
//# sourceMappingURL=deploys.jsx.map