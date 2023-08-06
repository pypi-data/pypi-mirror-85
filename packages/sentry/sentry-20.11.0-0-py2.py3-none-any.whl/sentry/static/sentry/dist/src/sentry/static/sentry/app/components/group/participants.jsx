import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { tn } from 'app/locale';
import UserAvatar from 'app/components/avatar/userAvatar';
import space from 'app/styles/space';
import SidebarSection from './sidebarSection';
var GroupParticipants = function (_a) {
    var participants = _a.participants;
    return (<SidebarSection title={tn('%s Participant', '%s Participants', participants.length)}>
    <Faces>
      {participants.map(function (user) { return (<Face key={user.username}>
          <UserAvatar size={28} user={user} hasTooltip/>
        </Face>); })}
    </Faces>
  </SidebarSection>);
};
export default GroupParticipants;
var Faces = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var Face = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-right: ", ";\n  margin-bottom: ", ";\n"])), space(0.5), space(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=participants.jsx.map