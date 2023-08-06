import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Highlight from 'app/components/highlight';
import { defined } from 'app/utils';
import Tooltip from 'app/components/tooltip';
import getDynamicText from 'app/utils/getDynamicText';
import TextOverflow from 'app/components/textOverflow';
import { getFormattedTimestamp } from './utils';
var Time = React.memo(function (_a) {
    var timestamp = _a.timestamp, relativeTime = _a.relativeTime, displayRelativeTime = _a.displayRelativeTime, searchTerm = _a.searchTerm;
    if (!(defined(timestamp) && defined(relativeTime))) {
        return null;
    }
    var _b = getFormattedTimestamp(timestamp, relativeTime, displayRelativeTime), date = _b.date, time = _b.time, displayTime = _b.displayTime;
    return (<Wrapper>
        <Tooltip title={<div>
              <div>{date}</div>
              {time !== '\u2014' && <div>{time}</div>}
            </div>} containerDisplayMode="inline-flex" disableForVisualTest>
          <TextOverflow>
            {getDynamicText({
        value: <Highlight text={searchTerm}>{displayTime}</Highlight>,
        fixed: '00:00:00',
    })}
          </TextOverflow>
        </Tooltip>
      </Wrapper>);
});
export default Time;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.textColor; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map