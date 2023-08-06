export function fetchProcessingIssues(api, orgId, projectIds) {
    if (projectIds === void 0) { projectIds = null; }
    return api.requestPromise("/organizations/" + orgId + "/processingissues/", {
        method: 'GET',
        query: projectIds ? { project: projectIds } : [],
    });
}
//# sourceMappingURL=processingIssues.jsx.map