import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { Client } from 'app/api';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * HoC that provides "api" client when mounted, and clears API requests when
 * component is unmounted
 */
var withApi = function (WrappedComponent, _a) {
    var _b;
    var persistInFlight = (_a === void 0 ? {} : _a).persistInFlight;
    return _b = /** @class */ (function (_super) {
            __extends(class_1, _super);
            function class_1(props) {
                var _this = _super.call(this, props) || this;
                _this.api = new Client();
                return _this;
            }
            class_1.prototype.componentWillUnmount = function () {
                if (!persistInFlight) {
                    this.api.clear();
                }
            };
            class_1.prototype.render = function () {
                var _a = this.props, api = _a.api, props = __rest(_a, ["api"]);
                return <WrappedComponent {...__assign({ api: api !== null && api !== void 0 ? api : this.api }, props)}/>;
            };
            return class_1;
        }(React.Component)),
        _b.displayName = "withApi(" + getDisplayName(WrappedComponent) + ")",
        _b;
};
export default withApi;
//# sourceMappingURL=withApi.jsx.map