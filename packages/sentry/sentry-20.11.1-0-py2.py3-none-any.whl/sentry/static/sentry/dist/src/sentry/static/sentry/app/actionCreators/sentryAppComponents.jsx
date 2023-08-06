import { __awaiter, __generator } from "tslib";
import SentryAppComponentsActions from 'app/actions/sentryAppComponentActions';
export function fetchSentryAppComponents(api, orgSlug, projectId) {
    return __awaiter(this, void 0, void 0, function () {
        var componentsUri, res;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    componentsUri = "/organizations/" + orgSlug + "/sentry-app-components/?projectId=" + projectId;
                    return [4 /*yield*/, api.requestPromise(componentsUri)];
                case 1:
                    res = _a.sent();
                    SentryAppComponentsActions.loadComponents(res);
                    return [2 /*return*/, res];
            }
        });
    });
}
//# sourceMappingURL=sentryAppComponents.jsx.map