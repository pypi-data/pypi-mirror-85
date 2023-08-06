import { __awaiter, __generator } from "tslib";
import PlatformExternalIssueActions from 'app/actions/platformExternalIssueActions';
export function deleteExternalIssue(api, groupId, externalIssueId) {
    return __awaiter(this, void 0, void 0, function () {
        var data, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    PlatformExternalIssueActions.delete(groupId, externalIssueId);
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/external-issues/" + externalIssueId + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    data = _a.sent();
                    PlatformExternalIssueActions.deleteSuccess(data);
                    return [2 /*return*/, data];
                case 3:
                    error_1 = _a.sent();
                    PlatformExternalIssueActions.deleteError(error_1);
                    throw error_1;
                case 4: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=platformExternalIssues.jsx.map