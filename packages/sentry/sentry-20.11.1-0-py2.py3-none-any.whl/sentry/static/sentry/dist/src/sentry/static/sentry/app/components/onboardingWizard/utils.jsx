export var taskIsDone = function (task) {
    return ['complete', 'skipped'].includes(task.status);
};
export var findCompleteTasks = function (task) {
    return task.completionSeen && ['complete', 'skipped'].includes(task.status);
};
export var findActiveTasks = function (task) {
    return task.requisiteTasks.length === 0 && !findCompleteTasks(task);
};
export var findUpcomingTasks = function (task) {
    return task.requisiteTasks.length > 0 && !findCompleteTasks(task);
};
//# sourceMappingURL=utils.jsx.map