import React from 'react';
import { t } from 'app/locale';
import { IconWarning } from 'app/icons';
import { getTraceContext } from 'app/components/events/interfaces/spans/utils';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { isTransactionEvent } from './utils';
import SpanTree from './spanTree';
var TraceView = function (props) {
    var baselineEvent = props.baselineEvent, regressionEvent = props.regressionEvent;
    if (!isTransactionEvent(baselineEvent) || !isTransactionEvent(regressionEvent)) {
        return (<EmptyMessage>
        <IconWarning color="gray300" size="lg"/>
        <p>{t('One of the given events is not a transaction.')}</p>
      </EmptyMessage>);
    }
    var baselineTraceContext = getTraceContext(baselineEvent);
    var regressionTraceContext = getTraceContext(regressionEvent);
    if (!baselineTraceContext || !regressionTraceContext) {
        return (<EmptyMessage>
        <IconWarning color="gray300" size="lg"/>
        <p>{t('There is no trace found in either of the given transactions.')}</p>
      </EmptyMessage>);
    }
    return <SpanTree baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>;
};
export default TraceView;
//# sourceMappingURL=traceView.jsx.map