import { __awaiter, __generator } from "tslib";
import { isWebpackChunkLoadingError } from 'app/utils';
var MAX_RETRIES = 2;
export default function retryableImport(fn) {
    return __awaiter(this, void 0, void 0, function () {
        var retries, tryLoad;
        var _this = this;
        return __generator(this, function (_a) {
            retries = 0;
            tryLoad = function () { return __awaiter(_this, void 0, void 0, function () {
                var module_1, err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            return [4 /*yield*/, fn()];
                        case 1:
                            module_1 = _a.sent();
                            return [2 /*return*/, module_1.default || module_1];
                        case 2:
                            err_1 = _a.sent();
                            if (isWebpackChunkLoadingError(err_1) && retries < MAX_RETRIES) {
                                retries++;
                                return [2 /*return*/, tryLoad()];
                            }
                            throw err_1;
                        case 3: return [2 /*return*/];
                    }
                });
            }); };
            return [2 /*return*/, tryLoad()];
        });
    });
}
//# sourceMappingURL=retryableImport.jsx.map