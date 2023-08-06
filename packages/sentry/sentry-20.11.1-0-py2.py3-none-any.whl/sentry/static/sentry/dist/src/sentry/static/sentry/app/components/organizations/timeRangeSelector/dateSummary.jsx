import { __extends, __makeTemplateObject } from "tslib";
/**
 * Displays and formats absolute DateTime ranges
 */
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import { DEFAULT_DAY_END_TIME, DEFAULT_DAY_START_TIME } from 'app/utils/dates';
import { t } from 'app/locale';
import space from 'app/styles/space';
var DateSummary = /** @class */ (function (_super) {
    __extends(DateSummary, _super);
    function DateSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DateSummary.prototype.getFormattedDate = function (date, format) {
        return moment(date).local().format(format);
    };
    DateSummary.prototype.formatDate = function (date) {
        return this.getFormattedDate(date, 'll');
    };
    DateSummary.prototype.formatTime = function (date, withSeconds) {
        if (withSeconds === void 0) { withSeconds = false; }
        return this.getFormattedDate(date, "HH:mm" + (withSeconds ? ':ss' : ''));
    };
    DateSummary.prototype.render = function () {
        var _a = this.props, start = _a.start, end = _a.end;
        var startTimeFormatted = this.formatTime(start, true);
        var endTimeFormatted = this.formatTime(end, true);
        // Show times if either start or end date contain a time that is not midnight
        var shouldShowTimes = startTimeFormatted !== DEFAULT_DAY_START_TIME ||
            endTimeFormatted !== DEFAULT_DAY_END_TIME;
        return (<DateGroupWrapper hasTime={shouldShowTimes}>
        <DateGroup>
          <Date hasTime={shouldShowTimes}>
            {this.formatDate(start)}
            {shouldShowTimes && <Time>{this.formatTime(start)}</Time>}
          </Date>
        </DateGroup>
        <React.Fragment>
          <DateRangeDivider>{t('to')}</DateRangeDivider>

          <DateGroup>
            <Date hasTime={shouldShowTimes}>
              {this.formatDate(end)}
              {shouldShowTimes && <Time>{this.formatTime(end)}</Time>}
            </Date>
          </DateGroup>
        </React.Fragment>
      </DateGroupWrapper>);
    };
    return DateSummary;
}(React.Component));
var DateGroupWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transform: translateY(", ");\n"], ["\n  display: flex;\n  align-items: center;\n  transform: translateY(", ");\n"])), function (p) { return (p.hasTime ? '-5px' : '0'); });
var DateGroup = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  min-width: 110px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  min-width: 110px;\n"])));
var Date = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  display: flex;\n  flex-direction: column;\n  align-items: flex-end;\n"], ["\n  ", ";\n  display: flex;\n  flex-direction: column;\n  align-items: flex-end;\n"])), function (p) { return p.hasTime && 'margin-top: 9px'; });
var Time = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 0.7em;\n  line-height: 0.7em;\n  opacity: 0.5;\n"], ["\n  font-size: 0.7em;\n  line-height: 0.7em;\n  opacity: 0.5;\n"])));
var DateRangeDivider = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space(0.5));
export default DateSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=dateSummary.jsx.map