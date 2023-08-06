import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import rrwebPlayer from 'rrweb-player';
import * as Sentry from '@sentry/react';
import { Panel } from 'app/components/panels';
var RRWebReplayer = /** @class */ (function (_super) {
    __extends(RRWebReplayer, _super);
    function RRWebReplayer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.wrapperRef = React.createRef();
        _this.rrwebPlayer = function () { return __awaiter(_this, void 0, void 0, function () {
            var element, url, resp, payload, err_1;
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        element = (_a = this.wrapperRef) === null || _a === void 0 ? void 0 : _a.current;
                        if (!element) {
                            return [2 /*return*/];
                        }
                        url = this.props.url;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 4, , 5]);
                        return [4 /*yield*/, fetch(url)];
                    case 2:
                        resp = _b.sent();
                        return [4 /*yield*/, resp.json()];
                    case 3:
                        payload = _b.sent();
                        this.newRRWebPlayer = new rrwebPlayer({
                            target: element,
                            data: payload,
                            autoplay: false,
                        });
                        return [3 /*break*/, 5];
                    case 4:
                        err_1 = _b.sent();
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    RRWebReplayer.prototype.componentDidMount = function () {
        this.rrwebPlayer();
    };
    RRWebReplayer.prototype.render = function () {
        var className = this.props.className;
        var content = <div ref={this.wrapperRef} className={className}/>;
        if (this.newRRWebPlayer) {
            return <Panel>{content}</Panel>;
        }
        return content;
    };
    return RRWebReplayer;
}(React.Component));
export default RRWebReplayer;
//# sourceMappingURL=rrWebReplayer.jsx.map