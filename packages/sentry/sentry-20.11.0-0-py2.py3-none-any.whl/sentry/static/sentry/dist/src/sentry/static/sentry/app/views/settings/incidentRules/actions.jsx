import { __awaiter, __generator } from "tslib";
function isSavedRule(rule) {
    return !!rule.id;
}
/**
 * Add a new rule or update an existing rule
 *
 * @param api API Client
 * @param orgId Organization slug
 * @param rule Saved or Unsaved Metric Rule
 * @param query Query parameters for the request eg - referrer
 */
export function addOrUpdateRule(api, orgId, projectId, rule, query) {
    return __awaiter(this, void 0, void 0, function () {
        var isExisting, endpoint, method;
        return __generator(this, function (_a) {
            isExisting = isSavedRule(rule);
            endpoint = "/projects/" + orgId + "/" + projectId + "/alert-rules/" + (isSavedRule(rule) ? rule.id + "/" : '');
            method = isExisting ? 'PUT' : 'POST';
            return [2 /*return*/, api.requestPromise(endpoint, {
                    method: method,
                    data: rule,
                    query: query,
                    includeAllArgs: true,
                })];
        });
    });
}
/**
 * Delete an existing rule
 *
 * @param api API Client
 * @param orgId Organization slug
 * @param rule Saved or Unsaved Metric Rule
 */
export function deleteRule(api, orgId, rule) {
    return api.requestPromise("/organizations/" + orgId + "/alert-rules/" + rule.id + "/", {
        method: 'DELETE',
    });
}
//# sourceMappingURL=actions.jsx.map