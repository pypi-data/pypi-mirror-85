import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { defined } from 'app/utils';
import { t } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
var ENDPOINT = '/users/me/authenticators/';
var AccountSecurityWrapper = /** @class */ (function (_super) {
    __extends(AccountSecurityWrapper, _super);
    function AccountSecurityWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisable = function (auth) { return __awaiter(_this, void 0, void 0, function () {
            var _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!auth || !auth.authId) {
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + auth.authId + "/", { method: 'DELETE' })];
                    case 2:
                        _a.sent();
                        this.remountComponent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        this.setState({ loading: false });
                        addErrorMessage(t('Error disabling %s', auth.name));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRegenerateBackupCodes = function () { return __awaiter(_this, void 0, void 0, function () {
            var _err_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + this.props.params.authId + "/", {
                                method: 'PUT',
                            })];
                    case 2:
                        _a.sent();
                        this.remountComponent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _a.sent();
                        this.setState({ loading: false });
                        addErrorMessage(t('Error regenerating backup codes'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountSecurityWrapper.prototype.getEndpoints = function () {
        return [
            ['authenticators', ENDPOINT],
            ['organizations', '/organizations/'],
        ];
    };
    AccountSecurityWrapper.prototype.renderBody = function () {
        var children = this.props.children;
        var _a = this.state, authenticators = _a.authenticators, organizations = _a.organizations;
        var enrolled = (authenticators === null || authenticators === void 0 ? void 0 : authenticators.filter(function (auth) { return auth.isEnrolled && !auth.isBackupInterface; })) || [];
        var countEnrolled = enrolled.length;
        var orgsRequire2fa = (organizations === null || organizations === void 0 ? void 0 : organizations.filter(function (org) { return org.require2FA; })) || [];
        var deleteDisabled = orgsRequire2fa.length > 0 && countEnrolled === 1;
        // This happens when you switch between children views and the next child
        // view is lazy loaded, it can potentially be `null` while the code split
        // package is being fetched
        if (!defined(children)) {
            return null;
        }
        return React.cloneElement(this.props.children, {
            onDisable: this.handleDisable,
            onRegenerateBackupCodes: this.handleRegenerateBackupCodes,
            authenticators: authenticators,
            deleteDisabled: deleteDisabled,
            orgsRequire2fa: orgsRequire2fa,
            countEnrolled: countEnrolled,
        });
    };
    return AccountSecurityWrapper;
}(AsyncComponent));
export default AccountSecurityWrapper;
//# sourceMappingURL=accountSecurityWrapper.jsx.map