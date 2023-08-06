import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openCreateTeamModal } from 'app/actionCreators/modal';
import { tct } from 'app/locale';
import TextBlock from 'app/views/settings/components/text/textBlock';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import AllTeamsRow from './allTeamsRow';
function AllTeamsList(_a) {
    var organization = _a.organization, urlPrefix = _a.urlPrefix, openMembership = _a.openMembership, teamList = _a.teamList, access = _a.access;
    var teamNodes = teamList.map(function (team) { return (<AllTeamsRow urlPrefix={urlPrefix} access={access} team={team} organization={organization} openMembership={openMembership} key={team.slug}/>); });
    if (!teamNodes.length) {
        var canCreateTeam = access.has('project:admin');
        return (<EmptyMessage>
        {tct('No teams here. [teamCreate]', {
            root: <TextBlock noMargin/>,
            teamCreate: canCreateTeam
                ? tct('You can always [link:create one].', {
                    link: (<StyledButton priority="link" onClick={function () {
                        return openCreateTeamModal({
                            organization: organization,
                        });
                    }}/>),
                })
                : null,
        })}
      </EmptyMessage>);
    }
    return <React.Fragment>{teamNodes}</React.Fragment>;
}
export default AllTeamsList;
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1;
//# sourceMappingURL=allTeamsList.jsx.map