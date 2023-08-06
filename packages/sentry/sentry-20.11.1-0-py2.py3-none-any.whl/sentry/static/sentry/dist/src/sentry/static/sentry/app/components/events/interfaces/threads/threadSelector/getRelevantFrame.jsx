// TODO(ts): define correct stack trace type
function getRelevantFrame(stacktrace) {
    if (!stacktrace.hasSystemFrames) {
        return stacktrace.frames[stacktrace.frames.length - 1];
    }
    for (var i = stacktrace.frames.length - 1; i >= 0; i--) {
        var frame = stacktrace.frames[i];
        if (frame.inApp) {
            return frame;
        }
    }
    // this should not happen
    return stacktrace.frames[stacktrace.frames.length - 1];
}
export default getRelevantFrame;
//# sourceMappingURL=getRelevantFrame.jsx.map