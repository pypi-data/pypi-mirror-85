import React from 'react';
import Exception from './exception';
import Stacktrace from './stacktrace';
var CrashContent = function (_a) {
    var _b;
    var event = _a.event, stackView = _a.stackView, stackType = _a.stackType, newestFirst = _a.newestFirst, projectId = _a.projectId, exception = _a.exception, stacktrace = _a.stacktrace;
    var platform = ((_b = event.platform) !== null && _b !== void 0 ? _b : 'other');
    if (exception) {
        return (<Exception stackType={stackType} stackView={stackView} projectId={projectId} newestFirst={newestFirst} event={event} platform={platform} values={exception.values}/>);
    }
    if (stacktrace) {
        return (<Stacktrace stacktrace={stacktrace} stackView={stackView} newestFirst={newestFirst} event={event} platform={platform}/>);
    }
    return null;
};
export default CrashContent;
//# sourceMappingURL=index.jsx.map