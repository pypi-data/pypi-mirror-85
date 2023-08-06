import React from 'react';
import ErrorBoundary from 'app/components/errorBoundary';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import rawStacktraceContent from 'app/components/events/interfaces/rawStacktraceContent';
import { STACK_VIEW } from 'app/types/stacktrace';
var Stacktrace = function (_a) {
    var stackView = _a.stackView, stacktrace = _a.stacktrace, event = _a.event, newestFirst = _a.newestFirst, platform = _a.platform;
    return (<ErrorBoundary mini>
    {stackView === STACK_VIEW.RAW ? (<pre className="traceback plain">
        {rawStacktraceContent(stacktrace, event.platform)}
      </pre>) : (<StacktraceContent data={stacktrace} className="no-exception" includeSystemFrames={stackView === STACK_VIEW.FULL} platform={platform} event={event} newestFirst={newestFirst}/>)}
  </ErrorBoundary>);
};
export default Stacktrace;
//# sourceMappingURL=stacktrace.jsx.map