import { __read, __spread } from "tslib";
import React from 'react';
import withOrganization from 'app/utils/withOrganization';
import ErrorBoundary from 'app/components/errorBoundary';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueListV2';
import { TraceKnownDataType } from './types';
import getTraceKnownData from './getTraceKnownData';
import getUnknownData from '../getUnknownData';
var traceKnownDataValues = [
    TraceKnownDataType.STATUS,
    TraceKnownDataType.TRACE_ID,
    TraceKnownDataType.SPAN_ID,
    TraceKnownDataType.PARENT_SPAN_ID,
    TraceKnownDataType.TRANSACTION_NAME,
    TraceKnownDataType.OP_NAME,
];
var traceIgnoredDataValues = [];
var InnerTrace = withOrganization(function (_a) {
    var organization = _a.organization, event = _a.event, data = _a.data;
    return (<ErrorBoundary mini>
      <KeyValueList data={getTraceKnownData(data, traceKnownDataValues, event, organization)} isSorted={false} raw={false}/>
      <KeyValueList data={getUnknownData(data, __spread(traceKnownDataValues, traceIgnoredDataValues))} isSorted={false} raw={false}/>
    </ErrorBoundary>);
});
var Trace = function (props) {
    return <InnerTrace {...props}/>;
};
export default Trace;
//# sourceMappingURL=trace.jsx.map