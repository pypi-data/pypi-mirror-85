import { __makeTemplateObject } from "tslib";
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconSound, IconSwitch, IconSync, IconWarning } from 'app/icons';
import Tag from 'app/components/tag';
import DateTime from 'app/components/dateTime';
var GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
};
var InboxReason = function (_a) {
    var inbox = _a.inbox;
    var reason = inbox.reason, reason_details = inbox.reason_details, dateAdded = inbox.date_added;
    var reasonIcon;
    var reasonBadgeText;
    var tooltipText;
    if (reason === GroupInboxReason.UNIGNORED) {
        reasonIcon = <IconSound />;
        reasonBadgeText = t('Unignored');
        tooltipText = t('%(count)s events within %(window)s', {
            count: (reason_details === null || reason_details === void 0 ? void 0 : reason_details.count) || 0,
            window: moment.duration((reason_details === null || reason_details === void 0 ? void 0 : reason_details.window) || 0, 'minutes').humanize(),
        });
    }
    else if (reason === GroupInboxReason.REGRESSION) {
        reasonIcon = <IconSync />;
        reasonBadgeText = t('Regression');
        tooltipText = t('Issue was previously resolved.');
    }
    else if (reason === GroupInboxReason.MANUAL) {
        reasonIcon = <IconSwitch />;
        reasonBadgeText = t('Manual');
        // TODO(scttcper): Add tooltip text for a manual move
        // Moved to inbox by {full_name}.
    }
    else {
        reasonIcon = <IconWarning />;
        reasonBadgeText = t('New Issue');
    }
    var tooltip = (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {dateAdded && (<DateWrapper>
          <DateTime date={dateAdded}/>
        </DateWrapper>)}
    </TooltipWrapper>);
    return (<Tag icon={reasonIcon} tooltipText={tooltip}>
      {reasonBadgeText}
    </Tag>);
};
export default InboxReason;
var DateWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
var TooltipWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=inboxReason.jsx.map