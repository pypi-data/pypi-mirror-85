import React from 'react';
import { defined } from 'app/utils';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import { Panel } from 'app/components/panels';
import { IconWarning } from 'app/icons';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { STACK_VIEW } from 'app/types/stacktrace';
var ExceptionStacktraceContent = function (_a) {
    var stackView = _a.stackView, stacktrace = _a.stacktrace, chainedException = _a.chainedException, platform = _a.platform, newestFirst = _a.newestFirst, data = _a.data, expandFirstFrame = _a.expandFirstFrame, event = _a.event;
    if (!defined(stacktrace)) {
        return null;
    }
    if (stackView === STACK_VIEW.APP &&
        stacktrace.frames.filter(function (frame) { return frame.inApp; }).length === 0 &&
        !chainedException) {
        return (<Panel dashedBorder>
        <EmptyMessage icon={<IconWarning size="xs"/>} title="No app only stack trace has been found!"/>
      </Panel>);
    }
    if (!data) {
        return null;
    }
    /**
     * Armin, Markus:
     * If all frames are in app, then no frame is in app.
     * This normally does not matter for the UI but when chained exceptions
     * are used this causes weird behavior where one exception appears to not have a stack trace.
     *
     * It is easier to fix the UI logic to show a non-empty stack trace for chained exceptions
     */
    return (<StacktraceContent data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={stackView === STACK_VIEW.FULL ||
        (chainedException && stacktrace.frames.every(function (frame) { return !frame.inApp; }))} platform={platform} newestFirst={newestFirst} event={event}/>);
};
export default ExceptionStacktraceContent;
//# sourceMappingURL=exceptionStacktraceContent.jsx.map