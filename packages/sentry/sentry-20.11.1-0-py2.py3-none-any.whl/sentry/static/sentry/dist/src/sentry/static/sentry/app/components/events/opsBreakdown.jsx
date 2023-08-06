import { __extends, __makeTemplateObject, __read, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isFinite from 'lodash/isFinite';
import QuestionTooltip from 'app/components/questionTooltip';
import { SectionHeading } from 'app/components/charts/styles';
import { pickSpanBarColour } from 'app/components/events/interfaces/spans/utils';
import { t } from 'app/locale';
import space from 'app/styles/space';
var OtherOperation = Symbol('Other');
var TOP_N_SPANS = 4;
var OpsBreakdown = /** @class */ (function (_super) {
    __extends(OpsBreakdown, _super);
    function OpsBreakdown() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OpsBreakdown.prototype.getTransactionEvent = function () {
        var event = this.props.event;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    };
    OpsBreakdown.prototype.generateStats = function () {
        var _a, _b;
        var event = this.getTransactionEvent();
        if (!event) {
            return [];
        }
        var traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        if (!traceContext) {
            return [];
        }
        var spanEntry = event.entries.find(function (entry) { return entry.type === 'spans'; });
        var spans = (_b = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _b !== void 0 ? _b : [];
        spans =
            spans.length > 0
                ? spans
                : // if there are no descendent spans, then use the transaction root span
                    [
                        {
                            op: traceContext.op,
                            timestamp: event.endTimestamp,
                            start_timestamp: event.startTimestamp,
                            trace_id: traceContext.trace_id || '',
                            span_id: traceContext.span_id || '',
                            data: {},
                        },
                    ];
        var operationNameIntervals = spans.reduce(function (intervals, span) {
            var startTimestamp = span.start_timestamp;
            var endTimestamp = span.timestamp;
            if (endTimestamp < startTimestamp) {
                // reverse timestamps
                startTimestamp = span.timestamp;
                endTimestamp = span.start_timestamp;
            }
            // invariant: startTimestamp <= endTimestamp
            var operationName = span.op;
            if (typeof operationName !== 'string') {
                // a span with no operation name is considered an 'unknown' op
                operationName = 'unknown';
            }
            var cover = [startTimestamp, endTimestamp];
            var operationNameInterval = intervals[operationName];
            if (!Array.isArray(operationNameInterval)) {
                intervals[operationName] = [cover];
                return intervals;
            }
            operationNameInterval.push(cover);
            intervals[operationName] = mergeInterval(operationNameInterval);
            return intervals;
        }, {});
        var operationNameCoverage = Object.entries(operationNameIntervals).reduce(function (acc, _a) {
            var _b = __read(_a, 2), operationName = _b[0], intervals = _b[1];
            var duration = intervals.reduce(function (sum, _a) {
                var _b = __read(_a, 2), start = _b[0], end = _b[1];
                return sum + Math.abs(end - start);
            }, 0);
            acc[operationName] = duration;
            return acc;
        }, {});
        var sortedOpsBreakdown = Object.entries(operationNameCoverage).sort(function (first, second) {
            var firstDuration = first[1];
            var secondDuration = second[1];
            if (firstDuration === secondDuration) {
                return 0;
            }
            if (firstDuration < secondDuration) {
                // sort second before first
                return 1;
            }
            // otherwise, sort first before second
            return -1;
        });
        var breakdown = sortedOpsBreakdown.slice(0, TOP_N_SPANS).map(function (_a) {
            var _b = __read(_a, 2), operationName = _b[0], duration = _b[1];
            return {
                name: operationName,
                // percentage to be recalculated after the ops breakdown group is decided
                percentage: 0,
                totalInterval: duration,
            };
        });
        var other = sortedOpsBreakdown.slice(TOP_N_SPANS).reduce(function (accOther, _a) {
            var _b = __read(_a, 2), _operationName = _b[0], duration = _b[1];
            accOther.totalInterval += duration;
            return accOther;
        }, {
            name: OtherOperation,
            // percentage to be recalculated after the ops breakdown group is decided
            percentage: 0,
            totalInterval: 0,
        });
        if (other.totalInterval > 0) {
            breakdown.push(other);
        }
        // calculate breakdown total duration
        var total = breakdown.reduce(function (sum, operationNameGroup) {
            return sum + operationNameGroup.totalInterval;
        }, 0);
        // recalculate percentage values
        breakdown.forEach(function (operationNameGroup) {
            operationNameGroup.percentage = operationNameGroup.totalInterval / total;
        });
        return breakdown;
    };
    OpsBreakdown.prototype.render = function () {
        var event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        var breakdown = this.generateStats();
        return (<StyledBreakdown>
        <SectionHeading>
          {t('Operation Breakdown')}
          <QuestionTooltip position="top" size="sm" containerDisplayMode="block" title={t('Durations are calculated by summing span durations over the course of the transaction. Percentages are then calculated by dividing the individual op duration by the sum of total op durations. Overlapping/parallel spans are only counted once.')}/>
        </SectionHeading>
        {breakdown.map(function (currOp) {
            var name = currOp.name, percentage = currOp.percentage, totalInterval = currOp.totalInterval;
            var isOther = name === OtherOperation;
            var operationName = typeof name === 'string' ? name : t('Other');
            var durLabel = Math.round(totalInterval * 1000 * 100) / 100;
            var pctLabel = isFinite(percentage) ? Math.round(percentage * 100) : '∞';
            var opsColor = pickSpanBarColour(operationName);
            return (<OpsLine key={operationName}>
              <OpsNameContainer>
                <OpsDot style={{ backgroundColor: isOther ? 'transparent' : opsColor }}/>
                <OpsName>{operationName}</OpsName>
              </OpsNameContainer>
              <OpsContent>
                <Dur>{durLabel}ms</Dur>
                <Pct>{pctLabel}%</Pct>
              </OpsContent>
            </OpsLine>);
        })}
      </StyledBreakdown>);
    };
    return OpsBreakdown;
}(React.Component));
var StyledBreakdown = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(4));
var OpsLine = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  * + * {\n    margin-left: ", ";\n  }\n"])), space(0.5), space(0.5));
var OpsDot = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n"])), space(1));
var OpsContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var OpsNameContainer = styled(OpsContent)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var OpsName = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])));
var Dur = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Pct = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  min-width: 40px;\n  text-align: right;\n"], ["\n  min-width: 40px;\n  text-align: right;\n"])));
function mergeInterval(intervals) {
    var e_1, _a;
    // sort intervals by start timestamps
    intervals.sort(function (first, second) {
        if (first[0] < second[0]) {
            // sort first before second
            return -1;
        }
        if (second[0] < first[0]) {
            // sort second before first
            return 1;
        }
        return 0;
    });
    // array of disjoint intervals
    var merged = [];
    try {
        for (var intervals_1 = __values(intervals), intervals_1_1 = intervals_1.next(); !intervals_1_1.done; intervals_1_1 = intervals_1.next()) {
            var currentInterval = intervals_1_1.value;
            if (merged.length === 0) {
                merged.push(currentInterval);
                continue;
            }
            var lastInterval = merged[merged.length - 1];
            var lastIntervalEnd = lastInterval[1];
            var _b = __read(currentInterval, 2), currentIntervalStart = _b[0], currentIntervalEnd = _b[1];
            if (lastIntervalEnd < currentIntervalStart) {
                // if currentInterval does not overlap with lastInterval,
                // then add currentInterval
                merged.push(currentInterval);
                continue;
            }
            // currentInterval and lastInterval overlaps; so we merge these intervals
            // invariant: lastIntervalStart <= currentIntervalStart
            lastInterval[1] = Math.max(lastIntervalEnd, currentIntervalEnd);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (intervals_1_1 && !intervals_1_1.done && (_a = intervals_1.return)) _a.call(intervals_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return merged;
}
export default OpsBreakdown;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=opsBreakdown.jsx.map