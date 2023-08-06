import React from 'react';
import SelectControl from 'app/components/forms/selectControl';
import SelectMembers from 'app/components/selectMembers';
import Input from 'app/views/settings/components/forms/controls/input';
import { ActionType, TargetType, } from 'app/views/settings/incidentRules/types';
var getPlaceholderForType = function (type) {
    switch (type) {
        case ActionType.SLACK:
            return '@username or #channel';
        case ActionType.MSTEAMS:
            //no prefixes for msteams
            return 'username or channel';
        case ActionType.PAGERDUTY:
            return 'service';
        default:
            throw Error('Not implemented');
    }
};
export default function ActionTargetSelector(props) {
    var action = props.action, availableAction = props.availableAction, disabled = props.disabled, loading = props.loading, onChange = props.onChange, organization = props.organization, project = props.project;
    var handleChangeTargetIdentifier = function (value) {
        onChange(value.value);
    };
    var handleChangeSpecificTargetIdentifier = function (e) {
        onChange(e.target.value);
    };
    switch (action.targetType) {
        case TargetType.TEAM:
        case TargetType.USER:
            var isTeam = action.targetType === TargetType.TEAM;
            return (<SelectMembers disabled={disabled} key={isTeam ? 'team' : 'member'} showTeam={isTeam} project={project} organization={organization} value={action.targetIdentifier} onChange={handleChangeTargetIdentifier}/>);
        case TargetType.SPECIFIC:
            return (availableAction === null || availableAction === void 0 ? void 0 : availableAction.options) ? (<SelectControl isDisabled={disabled || loading} value={action.targetIdentifier} options={availableAction.options} onChange={handleChangeTargetIdentifier}/>) : (<Input disabled={disabled} key={action.type} value={action.targetIdentifier || ''} onChange={handleChangeSpecificTargetIdentifier} placeholder={getPlaceholderForType(action.type)}/>);
        default:
            return null;
    }
}
//# sourceMappingURL=actionTargetSelector.jsx.map