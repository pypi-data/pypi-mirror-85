import { __read, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import RoleSelectControl from 'app/components/roleSelectControl';
import { IconClose } from 'app/icons/iconClose';
import renderEmailValue from './renderEmailValue';
var InviteRowControl = function (_a) {
    var className = _a.className, disabled = _a.disabled, emails = _a.emails, role = _a.role, teams = _a.teams, roleOptions = _a.roleOptions, roleDisabledUnallowed = _a.roleDisabledUnallowed, teamOptions = _a.teamOptions, inviteStatus = _a.inviteStatus, onRemove = _a.onRemove, onChangeEmails = _a.onChangeEmails, onChangeRole = _a.onChangeRole, onChangeTeams = _a.onChangeTeams, disableRemove = _a.disableRemove;
    return (<div className={className}>
    <div>
      <SelectControl deprecatedSelectControl data-test-id="select-emails" disabled={disabled} placeholder={t('Enter one or more email')} value={emails} options={emails.map(function (value) { return ({
        value: value,
        label: value,
    }); })} valueComponent={function (props) { return renderEmailValue(inviteStatus[props.value.value], props); }} onBlur={function (e) {
        return e.target.value &&
            onChangeEmails(__spread(emails.map(function (value) { return ({ value: value }); }), [{ value: e.target.value }]));
    }} shouldKeyDownEventCreateNewOption={function (_a) {
        var keyCode = _a.keyCode;
        // Keycodes are ENTER, SPACE, TAB, COMMA
        return [13, 32, 9, 188].includes(keyCode);
    }} onBlurResetsInput={false} onCloseResetsInput={false} onChange={onChangeEmails} multiple creatable clearable noMenu/>
    </div>
    <div>
      <RoleSelectControl deprecatedSelectControl data-test-id="select-role" disabled={disabled} value={role} roles={roleOptions} disableUnallowed={roleDisabledUnallowed} onChange={onChangeRole}/>
    </div>
    <div>
      <SelectControl deprecatedSelectControl data-test-id="select-teams" disabled={disabled} placeholder={t('Add to teams...')} value={teams} options={teamOptions.map(function (_a) {
        var slug = _a.slug;
        return ({
            value: slug,
            label: "#" + slug,
        });
    })} onChange={onChangeTeams} multiple clearable/>
    </div>
    <Button borderless icon={<IconClose />} size="zero" onClick={onRemove} disabled={disableRemove}/>
  </div>);
};
export default InviteRowControl;
//# sourceMappingURL=inviteRowControl.jsx.map