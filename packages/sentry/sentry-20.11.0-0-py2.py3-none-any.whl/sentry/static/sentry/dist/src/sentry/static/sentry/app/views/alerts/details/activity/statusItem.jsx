import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import ActivityItem from 'app/components/activity/item';
import getDynamicText from 'app/utils/getDynamicText';
import { IncidentActivityType, IncidentStatus, IncidentStatusMethod, } from '../../types';
/**
 * StatusItem renders status changes for Alerts
 *
 * For example: incident detected, or closed
 *
 * Note `activity.dateCreated` refers to when the activity was created vs.
 * `incident.dateStarted` which is when an incident was first detected or created
 */
var StatusItem = /** @class */ (function (_super) {
    __extends(StatusItem, _super);
    function StatusItem() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StatusItem.prototype.render = function () {
        var _a = this.props, activity = _a.activity, authorName = _a.authorName, incident = _a.incident, showTime = _a.showTime;
        var isDetected = activity.type === IncidentActivityType.DETECTED;
        var isStarted = activity.type === IncidentActivityType.STARTED;
        var isClosed = activity.type === IncidentActivityType.STATUS_CHANGE &&
            activity.value === "" + IncidentStatus.CLOSED;
        var isTriggerChange = activity.type === IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if (!isStarted && !isDetected && !isClosed && !isTriggerChange) {
            return null;
        }
        var currentTrigger = getTriggerName(activity.value);
        var previousTrigger = getTriggerName(activity.previousValue);
        return (<ActivityItem showTime={showTime} author={{
            type: activity.user ? 'user' : 'system',
            user: activity.user || undefined,
        }} header={<div>
            {isTriggerChange &&
            previousTrigger &&
            tct('Alert status changed from [previousTrigger] to [currentTrigger]', {
                previousTrigger: previousTrigger,
                currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
            })}
            {isTriggerChange &&
            !previousTrigger &&
            tct('Alert status changed to [currentTrigger]', {
                currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
            })}
            {isClosed &&
            (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === IncidentStatusMethod.RULE_UPDATED &&
            t('This alert has been auto-resolved because the rule that triggered it has been modified or deleted.')}
            {isClosed &&
            (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== IncidentStatusMethod.RULE_UPDATED &&
            tct('[user] resolved the alert', {
                user: <StatusValue>{authorName}</StatusValue>,
            })}
            {isDetected &&
            ((incident === null || incident === void 0 ? void 0 : incident.alertRule) ? t('Alert was created')
                : tct('[user] created an alert', {
                    user: <StatusValue>{authorName}</StatusValue>,
                }))}
            {isStarted && t('Trigger conditions were met for the interval')}
          </div>} date={getDynamicText({ value: activity.dateCreated, fixed: new Date(0) })} interval={isStarted ? incident === null || incident === void 0 ? void 0 : incident.alertRule.timeWindow : undefined}/>);
    };
    return StatusItem;
}(React.Component));
export default StatusItem;
var StatusValue = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
function getTriggerName(value) {
    if (value === "" + IncidentStatus.WARNING) {
        return t('Warning');
    }
    if (value === "" + IncidentStatus.CRITICAL) {
        return t('Critical');
    }
    // Otherwise, activity type is not status change
    return '';
}
var templateObject_1;
//# sourceMappingURL=statusItem.jsx.map