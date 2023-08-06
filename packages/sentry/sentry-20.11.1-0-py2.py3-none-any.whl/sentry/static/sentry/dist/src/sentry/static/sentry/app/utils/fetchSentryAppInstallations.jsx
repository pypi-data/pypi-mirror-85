import { __awaiter, __generator } from "tslib";
import SentryAppInstallationStore from 'app/stores/sentryAppInstallationsStore';
var fetchSentryAppInstallations = function (api, orgSlug) { return __awaiter(void 0, void 0, void 0, function () {
    var installsUri, installs;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                installsUri = "/organizations/" + orgSlug + "/sentry-app-installations/";
                return [4 /*yield*/, api.requestPromise(installsUri)];
            case 1:
                installs = _a.sent();
                SentryAppInstallationStore.load(installs);
                return [2 /*return*/];
        }
    });
}); };
export default fetchSentryAppInstallations;
//# sourceMappingURL=fetchSentryAppInstallations.jsx.map