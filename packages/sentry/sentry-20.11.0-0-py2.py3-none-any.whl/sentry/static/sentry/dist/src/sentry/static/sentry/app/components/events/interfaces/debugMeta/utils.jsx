function getStatusWeight(status) {
    switch (status) {
        case null:
        case undefined:
        case 'unused':
            return 0;
        case 'found':
            return 1;
        default:
            return 2;
    }
}
function combineStatus(debugStatus, unwindStatus) {
    var debugWeight = getStatusWeight(debugStatus);
    var unwindWeight = getStatusWeight(unwindStatus);
    var combined = debugWeight >= unwindWeight ? debugStatus : unwindStatus;
    return combined || 'unused';
}
function getFileName(path) {
    var directorySeparator = /^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/';
    return path.split(directorySeparator).pop();
}
export { getFileName, combineStatus };
//# sourceMappingURL=utils.jsx.map