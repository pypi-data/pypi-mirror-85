import { __awaiter, __generator } from "tslib";
import { addErrorMessage, clearIndicators } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
/**
 * Fetches a list of activities for an incident
 */
export function fetchIncidentActivities(api, orgId, alertId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/activity/")];
        });
    });
}
/**
 * Creates a note for an incident
 */
export function createIncidentNote(api, orgId, alertId, note) {
    return __awaiter(this, void 0, void 0, function () {
        var result, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/", {
                            method: 'POST',
                            data: {
                                mentions: note.mentions,
                                comment: note.text,
                            },
                        })];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, result];
                case 2:
                    err_1 = _a.sent();
                    addErrorMessage(t('Unable to post comment'));
                    throw err_1;
                case 3: return [2 /*return*/];
            }
        });
    });
}
/**
 * Deletes a note for an incident
 */
export function deleteIncidentNote(api, orgId, alertId, noteId) {
    return __awaiter(this, void 0, void 0, function () {
        var result, err_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/" + noteId + "/", {
                            method: 'DELETE',
                        })];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, result];
                case 2:
                    err_2 = _a.sent();
                    addErrorMessage(t('Failed to delete comment'));
                    throw err_2;
                case 3: return [2 /*return*/];
            }
        });
    });
}
/**
 * Updates a note for an incident
 */
export function updateIncidentNote(api, orgId, alertId, noteId, note) {
    return __awaiter(this, void 0, void 0, function () {
        var result, err_3;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/" + noteId + "/", {
                            method: 'PUT',
                            data: {
                                mentions: note.mentions,
                                comment: note.text,
                            },
                        })];
                case 1:
                    result = _a.sent();
                    clearIndicators();
                    return [2 /*return*/, result];
                case 2:
                    err_3 = _a.sent();
                    addErrorMessage(t('Unable to update comment'));
                    throw err_3;
                case 3: return [2 /*return*/];
            }
        });
    });
}
// This doesn't return anything because you shouldn't need to do anything with
// the result success or fail
export function markIncidentAsSeen(api, orgId, incident) {
    return __awaiter(this, void 0, void 0, function () {
        var err_4;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!incident || incident.hasSeen) {
                        return [2 /*return*/];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + incident.identifier + "/seen/", {
                            method: 'POST',
                            data: {
                                hasSeen: true,
                            },
                        })];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 4];
                case 3:
                    err_4 = _a.sent();
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=incident.jsx.map