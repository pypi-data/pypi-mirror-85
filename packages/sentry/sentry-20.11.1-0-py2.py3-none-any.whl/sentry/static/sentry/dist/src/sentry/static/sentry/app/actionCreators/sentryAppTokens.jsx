import { __awaiter, __generator } from "tslib";
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
/**
 * Install a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
export function addSentryAppToken(client, app) {
    return __awaiter(this, void 0, void 0, function () {
        var token, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    addLoadingMessage();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, client.requestPromise("/sentry-apps/" + app.slug + "/api-tokens/", {
                            method: 'POST',
                        })];
                case 2:
                    token = _a.sent();
                    addSuccessMessage(t('Token successfully added.'));
                    return [2 /*return*/, token];
                case 3:
                    err_1 = _a.sent();
                    addErrorMessage(t('Unable to create token'));
                    throw err_1;
                case 4: return [2 /*return*/];
            }
        });
    });
}
/**
 * Uninstall a sentry application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 * @param {String} token Token string
 */
export function removeSentryAppToken(client, app, token) {
    return __awaiter(this, void 0, void 0, function () {
        var err_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    addLoadingMessage();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, client.requestPromise("/sentry-apps/" + app.slug + "/api-tokens/" + token + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    _a.sent();
                    addSuccessMessage(t('Token successfully deleted.'));
                    return [2 /*return*/];
                case 3:
                    err_2 = _a.sent();
                    addErrorMessage(t('Unable to delete token'));
                    throw err_2;
                case 4: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=sentryAppTokens.jsx.map