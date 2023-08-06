import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import { IconClock } from 'app/icons';
import space from 'app/styles/space';
import TimeSince from 'app/components/timeSince';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var Times = function (_a) {
    var lastSeen = _a.lastSeen, firstSeen = _a.firstSeen;
    return (<Container>
    <FlexWrapper>
      {lastSeen && (<React.Fragment>
          <StyledIconClock size="11px"/>
          <TimeSince date={lastSeen} suffix={t('ago')}/>
        </React.Fragment>)}
      {firstSeen && lastSeen && (<span className="hidden-xs hidden-sm">&nbsp;—&nbsp;</span>)}
      {firstSeen && (<TimeSince date={firstSeen} suffix={t('old')} className="hidden-xs hidden-sm"/>)}
    </FlexWrapper>
  </Container>);
};
Times.propTypes = {
    lastSeen: PropTypes.string,
    firstSeen: PropTypes.string,
};
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0; /* flex-hack for overflow-ellipsised children */\n"], ["\n  flex-shrink: 1;\n  min-width: 0; /* flex-hack for overflow-ellipsised children */\n"])));
var FlexWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n\n  /* The following aligns the icon with the text, fixes bug in Firefox */\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n\n  /* The following aligns the icon with the text, fixes bug in Firefox */\n  display: flex;\n  align-items: center;\n"])), overflowEllipsis);
var StyledIconClock = styled(IconClock)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* this is solely for optics, since TimeSince always begins\n  with a number, and numbers do not have descenders */\n  margin-right: ", ";\n"], ["\n  /* this is solely for optics, since TimeSince always begins\n  with a number, and numbers do not have descenders */\n  margin-right: ", ";\n"])), space(0.5));
export default Times;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=times.jsx.map