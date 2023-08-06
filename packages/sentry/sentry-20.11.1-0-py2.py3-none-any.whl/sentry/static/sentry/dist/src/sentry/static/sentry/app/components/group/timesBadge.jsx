import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconClock } from 'app/icons';
import TimeSince from 'app/components/timeSince';
import Tag from 'app/components/tag';
var TimesBadge = function (_a) {
    var lastSeen = _a.lastSeen, firstSeen = _a.firstSeen;
    return (<Tag icon={lastSeen ? <IconClock /> : undefined}>
      {lastSeen && <TimeSince date={lastSeen} suffix={t('ago')} shorten/>}
      {firstSeen && lastSeen && (<Seperator className="hidden-xs hidden-sm">&nbsp;|&nbsp;</Seperator>)}
      {firstSeen && (<TimeSince date={firstSeen} suffix={t('old')} className="hidden-xs hidden-sm" shorten/>)}
    </Tag>);
};
var Seperator = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export default TimesBadge;
var templateObject_1;
//# sourceMappingURL=timesBadge.jsx.map