import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import map from 'lodash/map';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { IconWarning } from 'app/icons';
import { assert } from 'app/types/utils';
import { generateEventSlug, eventDetailsRoute } from 'app/utils/discover/urls';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import DiscoverButton from 'app/components/discoverButton';
import DateTime from 'app/components/dateTime';
import EventView from 'app/utils/discover/eventView';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pill from 'app/components/pill';
import Pills from 'app/components/pills';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { rawSpanKeys } from './types';
import { isGapSpan, isOrphanSpan, getTraceDateTimeRange } from './utils';
import * as SpanEntryContext from './context';
import InlineDocs from './inlineDocs';
var SpanDetail = /** @class */ (function (_super) {
    __extends(SpanDetail, _super);
    function SpanDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            transactionResults: undefined,
        };
        return _this;
    }
    SpanDetail.prototype.componentDidMount = function () {
        var _this = this;
        var span = this.props.span;
        if (isGapSpan(span)) {
            return;
        }
        this.fetchSpanDescendents(span.span_id, span.trace_id)
            .then(function (response) {
            if (!response.data || !Array.isArray(response.data)) {
                return;
            }
            _this.setState({
                transactionResults: response.data,
            });
        })
            .catch(function (error) {
            Sentry.captureException(error);
        });
    };
    SpanDetail.prototype.fetchSpanDescendents = function (spanID, traceID) {
        var _a = this.props, api = _a.api, organization = _a.organization, trace = _a.trace, event = _a.event;
        // Skip doing a request if the results will be behind a disabled button.
        if (!organization.features.includes('discover-basic')) {
            return new Promise(function (resolve) {
                resolve({ data: [] });
            });
        }
        var url = "/organizations/" + organization.slug + "/eventsv2/";
        var _b = getParams(getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        })), start = _b.start, end = _b.end;
        var query = {
            field: ['transaction', 'id', 'trace.span'],
            sort: ['-id'],
            query: "event.type:transaction trace:" + traceID + " trace.parent_span:" + spanID,
            project: organization.features.includes('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            start: start,
            end: end,
        };
        return api.requestPromise(url, {
            method: 'GET',
            query: query,
        });
    };
    SpanDetail.prototype.renderTraversalButton = function () {
        if (!this.state.transactionResults) {
            // TODO: Amend size to use theme when we evetually refactor LoadingIndicator
            // 12px is consistent with theme.iconSizes['xs'] but theme returns a string.
            return (<StyledDiscoverButton size="xsmall" disabled>
          <StyledLoadingIndicator size={12}/>
        </StyledDiscoverButton>);
        }
        if (this.state.transactionResults.length <= 0) {
            return (<StyledDiscoverButton size="xsmall" disabled>
          {t('No Children')}
        </StyledDiscoverButton>);
        }
        var _a = this.props, span = _a.span, orgId = _a.orgId, trace = _a.trace, event = _a.event, organization = _a.organization;
        assert(!isGapSpan(span));
        if (this.state.transactionResults.length === 1) {
            // Note: This is rendered by this.renderSpanChild() as a dedicated row
            return null;
        }
        var orgFeatures = new Set(organization.features);
        var _b = getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        var childrenEventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Children from Span ID " + span.span_id,
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            query: "event.type:transaction trace:" + span.trace_id + " trace.parent_span:" + span.span_id,
            projects: orgFeatures.has('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        return (<StyledDiscoverButton data-test-id="view-child-transactions" size="xsmall" to={childrenEventView.getResultsViewUrlTarget(orgId)}>
        {t('View Children')}
      </StyledDiscoverButton>);
    };
    SpanDetail.prototype.renderSpanChild = function () {
        var _this = this;
        if (!this.state.transactionResults || this.state.transactionResults.length !== 1) {
            return null;
        }
        var eventSlug = generateSlug(this.state.transactionResults[0]);
        var viewChildButton = (<SpanEntryContext.Consumer>
        {function (_a) {
            var getViewChildTransactionTarget = _a.getViewChildTransactionTarget;
            var to = getViewChildTransactionTarget(__assign(__assign({}, _this.state.transactionResults[0]), { eventSlug: eventSlug }));
            if (!to) {
                return null;
            }
            return (<StyledDiscoverButton data-test-id="view-child-transaction" size="xsmall" to={to}>
              {t('View Span')}
            </StyledDiscoverButton>);
        }}
      </SpanEntryContext.Consumer>);
        var results = this.state.transactionResults[0];
        return (<Row title="Child Span" extra={viewChildButton}>
        {results['trace.span'] + " - " + results.transaction + " (" + results['project.name'] + ")"}
      </Row>);
    };
    SpanDetail.prototype.renderTraceButton = function () {
        var _a = this.props, span = _a.span, orgId = _a.orgId, organization = _a.organization, trace = _a.trace, event = _a.event;
        var _b = getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        if (isGapSpan(span)) {
            return null;
        }
        var orgFeatures = new Set(organization.features);
        var traceEventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Transactions with Trace ID " + span.trace_id,
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            query: "event.type:transaction trace:" + span.trace_id,
            projects: orgFeatures.has('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        return (<StyledDiscoverButton size="xsmall" to={traceEventView.getResultsViewUrlTarget(orgId)}>
        {t('Search by Trace')}
      </StyledDiscoverButton>);
    };
    SpanDetail.prototype.renderOrphanSpanMessage = function () {
        var span = this.props.span;
        if (!isOrphanSpan(span)) {
            return null;
        }
        return (<Alert system type="info" icon={<IconWarning size="md"/>}>
        {t('This is a span that has no parent span within this transaction. It has been attached to the transaction root span by default.')}
      </Alert>);
    };
    SpanDetail.prototype.renderSpanErrorMessage = function () {
        var _a = this.props, orgId = _a.orgId, spanErrors = _a.spanErrors, totalNumberOfErrors = _a.totalNumberOfErrors, span = _a.span, trace = _a.trace, organization = _a.organization, event = _a.event;
        if (spanErrors.length === 0 || totalNumberOfErrors === 0 || isGapSpan(span)) {
            return null;
        }
        // invariant: spanErrors.length <= totalNumberOfErrors
        var eventSlug = generateEventSlug(spanErrors[0]);
        var _b = getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        var orgFeatures = new Set(organization.features);
        var errorsEventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Error events associated with span " + span.span_id,
            fields: ['title', 'project', 'issue', 'timestamp'],
            orderby: '-timestamp',
            query: "event.type:error trace:" + span.trace_id + " trace.span:" + span.span_id,
            projects: orgFeatures.has('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        var target = spanErrors.length === 1
            ? {
                pathname: eventDetailsRoute({
                    orgSlug: orgId,
                    eventSlug: eventSlug,
                }),
            }
            : errorsEventView.getResultsViewUrlTarget(orgId);
        var message = totalNumberOfErrors === 1 ? (<Link to={target}>
          <span>{t('An error event occurred in this span.')}</span>
        </Link>) : spanErrors.length === totalNumberOfErrors ? (<div>
          {tct('[link] occurred in this span.', {
            link: (<Link to={target}>
                <span>{t('%d error events', totalNumberOfErrors)}</span>
              </Link>),
        })}
        </div>) : (<div>
          {tct('[link] occurred in this span.', {
            link: (<Link to={target}>
                <span>
                  {t('%d out of %d error events', spanErrors.length, totalNumberOfErrors)}
                </span>
              </Link>),
        })}
        </div>);
        return (<Alert system type="error" icon={<IconWarning size="md"/>}>
        {message}
      </Alert>);
    };
    SpanDetail.prototype.renderSpanDetails = function () {
        var _a, _b, _c;
        var _d = this.props, span = _d.span, event = _d.event, organization = _d.organization;
        if (isGapSpan(span)) {
            return (<SpanDetails>
          <InlineDocs platform={((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name) || ''} orgSlug={organization.slug} projectSlug={event.projectSlug}/>
        </SpanDetails>);
        }
        var startTimestamp = span.start_timestamp;
        var endTimestamp = span.timestamp;
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        var unknownKeys = Object.keys(span).filter(function (key) {
            return !rawSpanKeys.has(key);
        });
        return (<React.Fragment>
        {this.renderOrphanSpanMessage()}
        {this.renderSpanErrorMessage()}
        <SpanDetails>
          <table className="table key-value">
            <tbody>
              <Row title="Span ID" extra={this.renderTraversalButton()}>
                {span.span_id}
              </Row>
              <Row title="Parent Span ID">{span.parent_span_id || ''}</Row>
              {this.renderSpanChild()}
              <Row title="Trace ID" extra={this.renderTraceButton()}>
                {span.trace_id}
              </Row>
              <Row title="Description">{(_b = span === null || span === void 0 ? void 0 : span.description) !== null && _b !== void 0 ? _b : ''}</Row>
              <Row title="Status">{span.status || ''}</Row>
              <Row title="Start Date">
                {getDynamicText({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                      <DateTime date={startTimestamp * 1000}/>
                      {" (" + startTimestamp + ")"}
                    </React.Fragment>),
        })}
              </Row>
              <Row title="End Date">
                {getDynamicText({
            fixed: 'Mar 16, 2020 9:10:13 AM UTC',
            value: (<React.Fragment>
                      <DateTime date={endTimestamp * 1000}/>
                      {" (" + endTimestamp + ")"}
                    </React.Fragment>),
        })}
              </Row>
              <Row title="Duration">{durationString}</Row>
              <Row title="Operation">{span.op || ''}</Row>
              <Row title="Same Process as Parent">
                {span.same_process_as_parent !== undefined
            ? String(span.same_process_as_parent)
            : null}
              </Row>
              <Tags span={span}/>
              {map((_c = span === null || span === void 0 ? void 0 : span.data) !== null && _c !== void 0 ? _c : {}, function (value, key) { return (<Row title={key} key={key}>
                  {JSON.stringify(value, null, 4) || ''}
                </Row>); })}
              {unknownKeys.map(function (key) { return (<Row title={key} key={key}>
                  {JSON.stringify(span[key], null, 4) || ''}
                </Row>); })}
            </tbody>
          </table>
        </SpanDetails>
      </React.Fragment>);
    };
    SpanDetail.prototype.render = function () {
        return (<SpanDetailContainer data-component="span-detail" onClick={function (event) {
            // prevent toggling the span detail
            event.stopPropagation();
        }}>
        {this.renderSpanDetails()}
      </SpanDetailContainer>);
    };
    return SpanDetail;
}(React.Component));
var StyledDiscoverButton = styled(DiscoverButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
export var SpanDetailContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"], ["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"])), function (p) { return p.theme.border; });
export var SpanDetails = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var ValueTd = styled('td')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"])), space(2));
export var Row = function (_a) {
    var title = _a.title, keep = _a.keep, children = _a.children, _b = _a.extra, extra = _b === void 0 ? null : _b;
    if (!keep && !children) {
        return null;
    }
    return (<tr>
      <td className="key">{title}</td>
      <ValueTd className="value">
        <pre className="val">
          <span className="val-string">{children}</span>
        </pre>
        {extra}
      </ValueTd>
    </tr>);
};
export var Tags = function (_a) {
    var span = _a.span;
    var tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return null;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <Pills style={{ padding: '8px' }}>
          {keys.map(function (key, index) { return (<Pill key={index} name={key} value={String(tags[key]) || ''}/>); })}
        </Pills>
      </td>
    </tr>);
};
function generateSlug(result) {
    return generateEventSlug({
        id: result.id,
        'project.name': result['project.name'],
    });
}
export default withApi(SpanDetail);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=spanDetail.jsx.map