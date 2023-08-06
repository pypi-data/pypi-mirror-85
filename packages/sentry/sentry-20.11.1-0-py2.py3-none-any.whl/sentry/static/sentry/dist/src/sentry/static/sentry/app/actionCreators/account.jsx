import { __awaiter, __generator } from "tslib";
import { Client } from 'app/api';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import ConfigStore from 'app/stores/configStore';
export function disconnectIdentity(identity) {
    return __awaiter(this, void 0, void 0, function () {
        var api, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new Client();
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/users/me/social-identities/" + identity.id + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    _b.sent();
                    addSuccessMessage("Disconnected " + identity.providerLabel);
                    return [3 /*break*/, 4];
                case 3:
                    _a = _b.sent();
                    addErrorMessage('Error disconnecting identity');
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
export function updateUser(user) {
    // Ideally we'd fire an action but this is gonna get refactored soon anyway
    ConfigStore.set('user', user);
}
export function logout(api) {
    return api.requestPromise('/auth/', { method: 'DELETE' });
}
export function removeAuthenticator(api, userId, authId) {
    return api.requestPromise("/users/" + userId + "/authenticators/" + authId + "/", {
        method: 'DELETE',
    });
}
//# sourceMappingURL=account.jsx.map