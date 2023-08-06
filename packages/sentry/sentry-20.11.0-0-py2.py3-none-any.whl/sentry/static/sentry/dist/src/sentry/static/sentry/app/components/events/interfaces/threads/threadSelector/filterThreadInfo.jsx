import { trimPackage } from 'app/components/events/interfaces/frame/utils';
import getThreadStacktrace from './getThreadStacktrace';
import getRelevantFrame from './getRelevantFrame';
import trimFilename from './trimFilename';
function filterThreadInfo(thread, event) {
    var stacktrace = getThreadStacktrace(thread, event, false);
    var threadInfo = {};
    if (!stacktrace) {
        return threadInfo;
    }
    var relevantFrame = getRelevantFrame(stacktrace);
    if (relevantFrame.filename) {
        threadInfo.filename = trimFilename(relevantFrame.filename);
    }
    if (relevantFrame.function) {
        threadInfo.label = relevantFrame.function;
        return threadInfo;
    }
    if (relevantFrame.package) {
        threadInfo.label = trimPackage(relevantFrame.package);
        return threadInfo;
    }
    if (relevantFrame.module) {
        threadInfo.label = relevantFrame.module;
        return threadInfo;
    }
    return threadInfo;
}
export default filterThreadInfo;
//# sourceMappingURL=filterThreadInfo.jsx.map