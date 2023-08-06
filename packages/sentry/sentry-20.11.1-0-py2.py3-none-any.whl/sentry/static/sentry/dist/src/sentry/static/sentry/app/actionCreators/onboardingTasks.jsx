import { __assign, __awaiter, __generator, __read, __spread } from "tslib";
import OrganizationActions from 'app/actions/organizationActions';
import ConfigStore from 'app/stores/configStore';
/**
 * Update an onboarding task.
 *
 * If no API client is provided the task will not be updated on the server side
 * and will only update in the organization store.
 */
export function updateOnboardingTask(api, organization, updatedTask) {
    return __awaiter(this, void 0, void 0, function () {
        var hasExistingTask, user, onboardingTasks;
        return __generator(this, function (_a) {
            if (api !== null) {
                api.requestPromise("/organizations/" + organization.slug + "/onboarding-tasks/", {
                    method: 'POST',
                    data: updatedTask,
                });
            }
            hasExistingTask = organization.onboardingTasks.find(function (task) { return task.task === updatedTask.task; });
            user = ConfigStore.get('user');
            onboardingTasks = hasExistingTask
                ? organization.onboardingTasks.map(function (task) {
                    return task.task === updatedTask.task ? __assign(__assign({}, task), updatedTask) : task;
                })
                : __spread(organization.onboardingTasks, [__assign(__assign({}, updatedTask), { user: user })]);
            OrganizationActions.update({ onboardingTasks: onboardingTasks });
            return [2 /*return*/];
        });
    });
}
//# sourceMappingURL=onboardingTasks.jsx.map