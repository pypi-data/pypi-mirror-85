import { __assign, __awaiter, __generator } from "tslib";
import { Client } from 'app/api';
export var recordInteraction = function (sentryAppSlug, field, data) { return __awaiter(void 0, void 0, void 0, function () {
    var api, endpoint;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                api = new Client();
                endpoint = "/sentry-apps/" + sentryAppSlug + "/interaction/";
                return [4 /*yield*/, api.requestPromise(endpoint, {
                        method: 'POST',
                        data: __assign({ tsdbField: field }, data),
                    })];
            case 1: return [2 /*return*/, _a.sent()];
        }
    });
}); };
//# sourceMappingURL=recordSentryAppInteraction.jsx.map