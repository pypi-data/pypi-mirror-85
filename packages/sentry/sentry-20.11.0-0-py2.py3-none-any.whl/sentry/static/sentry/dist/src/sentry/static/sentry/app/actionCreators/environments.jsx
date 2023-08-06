import { __awaiter, __generator } from "tslib";
import EnvironmentActions from 'app/actions/environmentActions';
/**
 * Fetches all environments for an organization
 *
 * @param organizationSlug The organization slug
 */
export function fetchOrganizationEnvironments(api, organizationSlug) {
    return __awaiter(this, void 0, void 0, function () {
        var environments, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    EnvironmentActions.fetchEnvironments();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + organizationSlug + "/environments/")];
                case 2:
                    environments = _a.sent();
                    if (!environments) {
                        EnvironmentActions.fetchEnvironmentsError(new Error('retrieved environments is falsey'));
                        return [2 /*return*/];
                    }
                    EnvironmentActions.fetchEnvironmentsSuccess(environments);
                    return [3 /*break*/, 4];
                case 3:
                    err_1 = _a.sent();
                    EnvironmentActions.fetchEnvironmentsError(err_1);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=environments.jsx.map