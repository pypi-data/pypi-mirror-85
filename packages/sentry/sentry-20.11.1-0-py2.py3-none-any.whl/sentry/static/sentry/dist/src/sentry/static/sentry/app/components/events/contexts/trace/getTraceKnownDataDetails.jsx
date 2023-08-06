import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment-timezone';
import { t } from 'app/locale';
import Button from 'app/components/button';
import space from 'app/styles/space';
import EventView from 'app/utils/discover/eventView';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { TraceKnownDataType } from './types';
function getUserKnownDataDetails(data, type, event, organization) {
    switch (type) {
        case TraceKnownDataType.TRACE_ID: {
            var traceId = data.trace_id || '';
            if (!traceId) {
                return undefined;
            }
            if (!organization.features.includes('discover-basic')) {
                return {
                    subject: t('Trace ID'),
                    value: traceId,
                };
            }
            var dateCreated = moment(event.dateCreated).valueOf() / 1000;
            var pointInTime = (event === null || event === void 0 ? void 0 : event.dateReceived) ? moment(event.dateReceived).valueOf() / 1000
                : dateCreated;
            var _a = getTraceDateTimeRange({ start: pointInTime, end: pointInTime }), start = _a.start, end = _a.end;
            var orgFeatures = new Set(organization.features);
            var traceEventView = EventView.fromSavedQuery({
                id: undefined,
                name: "Events with Trace ID " + traceId,
                fields: ['title', 'event.type', 'project', 'trace.span', 'timestamp'],
                orderby: '-timestamp',
                query: "trace:" + traceId,
                projects: orgFeatures.has('global-views')
                    ? [ALL_ACCESS_PROJECTS]
                    : [Number(event.projectID)],
                version: 2,
                start: start,
                end: end,
            });
            return {
                subject: t('Trace ID'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{traceId}</span>
            </pre>
            <StyledButton size="xsmall" to={traceEventView.getResultsViewUrlTarget(organization.slug)}>
              {t('Search by Trace')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        case TraceKnownDataType.SPAN_ID: {
            return {
                subject: t('Span ID'),
                value: data.span_id || '',
            };
        }
        case TraceKnownDataType.PARENT_SPAN_ID: {
            return {
                subject: t('Parent Span ID'),
                value: data.parent_span_id || '',
            };
        }
        case TraceKnownDataType.OP_NAME: {
            return {
                subject: t('Operation Name'),
                value: data.op || '',
            };
        }
        case TraceKnownDataType.STATUS: {
            return {
                subject: t('Status'),
                value: data.status || '',
            };
        }
        case TraceKnownDataType.TRANSACTION_NAME: {
            var eventTag = event === null || event === void 0 ? void 0 : event.tags.find(function (tag) {
                return tag.key === 'transaction';
            });
            if (!eventTag || typeof eventTag.value !== 'string') {
                return undefined;
            }
            var transactionName = eventTag.value;
            var to = transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: {},
            });
            if (!organization.features.includes('performance-view')) {
                return {
                    subject: t('Transaction'),
                    value: transactionName,
                };
            }
            return {
                subject: t('Transaction'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{transactionName}</span>
            </pre>
            <StyledButton size="xsmall" to={to}>
              {t('View Summary')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        default:
            return undefined;
    }
}
var ButtonWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
export default getUserKnownDataDetails;
var templateObject_1, templateObject_2;
//# sourceMappingURL=getTraceKnownDataDetails.jsx.map