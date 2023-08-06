import React from 'react';
import ErrorBoundary from 'app/components/errorBoundary';
import RawExceptionContent from 'app/components/events/interfaces/rawExceptionContent';
import ExceptionContent from 'app/components/events/interfaces/exceptionContent';
import { STACK_VIEW } from 'app/types/stacktrace';
var Exception = function (_a) {
    var stackView = _a.stackView, stackType = _a.stackType, projectId = _a.projectId, values = _a.values, event = _a.event, newestFirst = _a.newestFirst, _b = _a.platform, platform = _b === void 0 ? 'other' : _b;
    return (<ErrorBoundary mini>
    {stackView === STACK_VIEW.RAW ? (<RawExceptionContent eventId={event.id} projectId={projectId} type={stackType} values={values} platform={platform}/>) : (<ExceptionContent type={stackType} stackView={stackView} values={values} platform={platform} newestFirst={newestFirst} event={event}/>)}
  </ErrorBoundary>);
};
export default Exception;
//# sourceMappingURL=exception.jsx.map