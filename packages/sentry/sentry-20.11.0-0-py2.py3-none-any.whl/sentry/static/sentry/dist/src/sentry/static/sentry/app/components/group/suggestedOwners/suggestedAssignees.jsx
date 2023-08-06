import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import SuggestedOwnerHovercard from 'app/components/group/suggestedOwnerHovercard';
import space from 'app/styles/space';
import SidebarSection from '../sidebarSection';
var SuggestedAssignees = function (_a) {
    var owners = _a.owners, onAssign = _a.onAssign;
    return (<SidebarSection title={<React.Fragment>
        {t('Suggested Assignees')}
        <Subheading>{t('Click to assign')}</Subheading>
      </React.Fragment>}>
    <Content>
      {owners.map(function (owner, i) { return (<SuggestedOwnerHovercard key={owner.actor.id + ":" + owner.actor.email + ":" + owner.actor.name + ":" + i} {...owner}>
          <ActorAvatar css={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n              cursor: pointer;\n            "], ["\n              cursor: pointer;\n            "])))} onClick={onAssign(owner.actor)} hasTooltip={false} actor={owner.actor}/>
        </SuggestedOwnerHovercard>); })}
    </Content>
  </SidebarSection>);
};
export { SuggestedAssignees };
var Subheading = styled('small')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  line-height: 100%;\n  font-weight: 400;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  line-height: 100%;\n  font-weight: 400;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.gray300; }, space(0.5));
var Content = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 20px);\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 20px);\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=suggestedAssignees.jsx.map