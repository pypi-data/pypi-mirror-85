export function promptsUpdate(api, params) {
    return api.requestPromise('/promptsactivity/', {
        method: 'PUT',
        data: {
            organization_id: params.organizationId,
            project_id: params.projectId,
            feature: params.feature,
            status: params.status,
        },
    });
}
//# sourceMappingURL=prompts.jsx.map