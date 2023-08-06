import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import HookOrDefault from 'app/components/hookOrDefault';
import Tag from 'app/components/tagDeprecated';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import SelectControl from 'app/components/forms/selectControl';
import RoleSelectControl from 'app/components/roleSelectControl';
var InviteModalHook = HookOrDefault({
    hookName: 'member-invite-modal:customization',
    defaultComponent: function (_a) {
        var onSendInvites = _a.onSendInvites, children = _a.children;
        return children({ sendInvites: onSendInvites, canSend: true });
    },
});
var InviteRequestRow = function (_a) {
    var inviteRequest = _a.inviteRequest, inviteRequestBusy = _a.inviteRequestBusy, organization = _a.organization, onApprove = _a.onApprove, onDeny = _a.onDeny, onUpdate = _a.onUpdate, allTeams = _a.allTeams, allRoles = _a.allRoles;
    var role = allRoles.find(function (r) { return r.id === inviteRequest.role; });
    var roleDisallowed = !(role && role.allowed);
    // eslint-disable-next-line react/prop-types
    var hookRenderer = function (_a) {
        var sendInvites = _a.sendInvites, canSend = _a.canSend, headerInfo = _a.headerInfo;
        return (<StyledPanelItem>
      <div>
        <h5 style={{ marginBottom: '3px' }}>
          <UserName>{inviteRequest.email}</UserName>
        </h5>
        {inviteRequest.inviteStatus === 'requested_to_be_invited' ? (inviteRequest.inviterName && (<Description>
              <Tooltip title={t('An existing member has asked to invite this user to your organization')}>
                {tct('Requested by [inviterName]', {
            inviterName: inviteRequest.inviterName,
        })}
              </Tooltip>
            </Description>)) : (<Tooltip title={t('This user has asked to join your organization.')}>
            <JoinRequestIndicator size="small">{t('Join request')}</JoinRequestIndicator>
          </Tooltip>)}
      </div>

      <StyledRoleSelectControl name="role" disableUnallowed onChange={function (r) { return onUpdate({ role: r.value }); }} value={inviteRequest.role} roles={allRoles}/>

      <TeamSelectControl deprecatedSelectControl name="teams" placeholder={t('Add to teams...')} onChange={function (teams) { return onUpdate({ teams: teams.map(function (team) { return team.value; }) }); }} value={inviteRequest.teams} options={allTeams.map(function (_a) {
            var slug = _a.slug;
            return ({
                value: slug,
                label: "#" + slug,
            });
        })} multiple clearable/>

      <ButtonGroup>
        <Confirm onConfirm={sendInvites} disableConfirmButton={!canSend} disabled={roleDisallowed} message={<React.Fragment>
              {tct('Are you sure you want to invite [email] to your organization?', {
            email: inviteRequest.email,
        })}
              {headerInfo}
            </React.Fragment>}>
          <Button priority="primary" size="small" busy={inviteRequestBusy[inviteRequest.id]} title={roleDisallowed
            ? t("You do not have permission to approve a user of this role.\n                     Select a different role to approve this user.")
            : undefined}>
            {t('Approve')}
          </Button>
        </Confirm>
        <Button size="small" busy={inviteRequestBusy[inviteRequest.id]} onClick={function () { return onDeny(inviteRequest); }}>
          {t('Deny')}
        </Button>
      </ButtonGroup>
    </StyledPanelItem>);
    };
    return (<InviteModalHook willInvite organization={organization} onSendInvites={function () { return onApprove(inviteRequest); }}>
      {hookRenderer}
    </InviteModalHook>);
};
InviteRequestRow.propTypes = {
    inviteRequest: PropTypes.shape({
        email: PropTypes.string,
        id: PropTypes.string,
        inviterName: PropTypes.string,
        inviteStatus: PropTypes.string,
        role: PropTypes.string,
        teams: PropTypes.arrayOf(PropTypes.string),
    }),
    onApprove: PropTypes.func,
    onDeny: PropTypes.func,
    inviteRequestBusy: PropTypes.object,
    allRoles: PropTypes.arrayOf(PropTypes.object),
    allTeams: PropTypes.arrayOf(PropTypes.object),
};
var JoinRequestIndicator = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-size: 10px;\n  text-transform: uppercase;\n"], ["\n  padding: ", " ", ";\n  font-size: 10px;\n  text-transform: uppercase;\n"])), space(0.5), space(0.75));
var StyledPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 220px max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 220px max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(2));
var UserName = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.fontSizeLarge; });
var Description = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.subText; });
var StyledRoleSelectControl = styled(RoleSelectControl)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  max-width: 140px;\n"], ["\n  max-width: 140px;\n"])));
var TeamSelectControl = styled(SelectControl)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-width: 220px;\n  .Select-value-label {\n    max-width: 150px;\n    word-break: break-all;\n  }\n"], ["\n  max-width: 220px;\n  .Select-value-label {\n    max-width: 150px;\n    word-break: break-all;\n  }\n"])));
var ButtonGroup = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n"])), space(1));
export default InviteRequestRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=inviteRequestRow.jsx.map