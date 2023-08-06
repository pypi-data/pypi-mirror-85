import { __awaiter, __extends, __generator, __rest } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
import U2fSign from './u2fsign';
var U2fContainer = /** @class */ (function (_super) {
    __extends(U2fContainer, _super);
    function U2fContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            authenticators: [],
        };
        return _this;
    }
    U2fContainer.prototype.componentDidMount = function () {
        this.getAuthenticators();
    };
    U2fContainer.prototype.getAuthenticators = function () {
        return __awaiter(this, void 0, void 0, function () {
            var api, authenticators, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = this.props.api;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/authenticators/')];
                    case 2:
                        authenticators = _b.sent();
                        this.setState({ authenticators: authenticators !== null && authenticators !== void 0 ? authenticators : [] });
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    U2fContainer.prototype.render = function () {
        var _this = this;
        var className = this.props.className;
        var authenticators = this.state.authenticators;
        if (!authenticators.length) {
            return null;
        }
        return (<div className={className}>
        {authenticators.map(function (_a) {
            var id = _a.id, other = __rest(_a, ["id"]);
            if (id === 'u2f' && other.challenge) {
                return <U2fSign key={id} {..._this.props} challengeData={other.challenge}/>;
            }
            return null;
        })}
      </div>);
    };
    return U2fContainer;
}(React.Component));
export default withApi(U2fContainer);
//# sourceMappingURL=u2fContainer.jsx.map