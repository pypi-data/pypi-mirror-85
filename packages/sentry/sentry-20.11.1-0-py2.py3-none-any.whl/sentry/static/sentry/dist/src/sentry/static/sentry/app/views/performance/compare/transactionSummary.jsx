import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
import { getHumanDuration, parseTrace } from 'app/components/events/interfaces/spans/utils';
import { getTransactionDetailsUrl } from '../utils';
import { isTransactionEvent } from './utils';
var TransactionSummary = /** @class */ (function (_super) {
    __extends(TransactionSummary, _super);
    function TransactionSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionSummary.prototype.render = function () {
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent, organization = _a.organization, location = _a.location, params = _a.params;
        var baselineEventSlug = params.baselineEventSlug, regressionEventSlug = params.regressionEventSlug;
        if (!isTransactionEvent(baselineEvent) || !isTransactionEvent(regressionEvent)) {
            return null;
        }
        var baselineTrace = parseTrace(baselineEvent);
        var regressionTrace = parseTrace(regressionEvent);
        var baselineDuration = Math.abs(baselineTrace.traceStartTimestamp - baselineTrace.traceEndTimestamp);
        var regressionDuration = Math.abs(regressionTrace.traceStartTimestamp - regressionTrace.traceEndTimestamp);
        return (<Container>
        <EventRow>
          <Baseline />
          <EventRowContent>
            <Content>
              <ContentTitle>{t('Baseline Event')}</ContentTitle>
              <EventId>
                <span>{t('ID')}: </span>
                <StyledLink to={getTransactionDetailsUrl(organization, baselineEventSlug.trim(), baselineEvent.title, location.query)}>
                  {shortEventId(baselineEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{getHumanDuration(baselineDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
        <EventRow>
          <Regression />
          <EventRowContent>
            <Content>
              <ContentTitle>{t('This Event')}</ContentTitle>
              <EventId>
                <span>{t('ID')}: </span>
                <StyledLink to={getTransactionDetailsUrl(organization, regressionEventSlug.trim(), regressionEvent.title, location.query)}>
                  {shortEventId(regressionEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{getHumanDuration(regressionDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
      </Container>);
    };
    return TransactionSummary;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  justify-content: space-between;\n  align-content: space-between;\n\n  padding-bottom: ", ";\n\n  > * + * {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  justify-content: space-between;\n  align-content: space-between;\n\n  padding-bottom: ", ";\n\n  > * + * {\n    margin-top: ", ";\n  }\n"])), space(1), space(0.75));
var EventRow = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Baseline = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"], ["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"])), function (p) { return p.theme.textColor; }, space(1));
var Regression = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"], ["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"])), function (p) { return p.theme.purple200; }, space(1));
var EventRowContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n  display: flex;\n"], ["\n  flex-grow: 1;\n  display: flex;\n"])));
var TimeDuration = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  line-height: 1.2;\n\n  margin-left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  line-height: 1.2;\n\n  margin-left: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space(1));
var Content = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex-grow: 1;\n  width: 150px;\n\n  font-size: ", ";\n"], ["\n  flex-grow: 1;\n  width: 150px;\n\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ContentTitle = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-weight: 600;\n"], ["\n  font-weight: 600;\n"])));
var EventId = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var StyledLink = styled(Link)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
function shortEventId(value) {
    return value.substring(0, 8);
}
export default TransactionSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=transactionSummary.jsx.map