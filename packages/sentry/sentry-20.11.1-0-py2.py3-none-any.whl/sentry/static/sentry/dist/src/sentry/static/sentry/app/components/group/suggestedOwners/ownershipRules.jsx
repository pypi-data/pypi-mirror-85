import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { ClassNames } from '@emotion/core';
import { IconQuestion } from 'app/icons';
import { openCreateOwnershipRule } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import Button from 'app/components/button';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Hovercard from 'app/components/hovercard';
import space from 'app/styles/space';
import SidebarSection from '../sidebarSection';
var OwnershipRules = function (_a) {
    var project = _a.project, organization = _a.organization, issueId = _a.issueId;
    var handleOpenCreateOwnershipRule = function () {
        openCreateOwnershipRule({ project: project, organization: organization, issueId: issueId });
    };
    return (<SidebarSection title={<React.Fragment>
          {t('Ownership Rules')}
          <ClassNames>
            {function (_a) {
        var css = _a.css;
        return (<Hovercard body={<HelpfulBody>
                    <p>
                      {t('Ownership rules allow you to associate file paths and URLs to specific teams or users, so alerts can be routed to the right people.')}
                    </p>
                    <Button href="https://docs.sentry.io/workflow/issue-owners/" priority="primary">
                      {t('Learn more')}
                    </Button>
                  </HelpfulBody>} containerClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                  display: flex;\n                  align-items: center;\n                "], ["\n                  display: flex;\n                  align-items: center;\n                "])))}>
                <StyledIconQuestion size="xs"/>
              </Hovercard>);
    }}
          </ClassNames>
        </React.Fragment>}>
      <GuideAnchor target="owners" position="bottom" offset={space(3)}>
        <Button onClick={handleOpenCreateOwnershipRule} size="small">
          {t('Create Ownership Rule')}
        </Button>
      </GuideAnchor>
    </SidebarSection>);
};
export { OwnershipRules };
var StyledIconQuestion = styled(IconQuestion)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
var HelpfulBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n  text-align: center;\n"], ["\n  padding: ", ";\n  text-align: center;\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=ownershipRules.jsx.map