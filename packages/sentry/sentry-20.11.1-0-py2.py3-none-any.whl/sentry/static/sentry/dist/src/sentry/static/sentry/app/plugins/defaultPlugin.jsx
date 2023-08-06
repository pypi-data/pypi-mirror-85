import { __extends } from "tslib";
import BasePlugin from 'app/plugins/basePlugin';
var DefaultPlugin = /** @class */ (function (_super) {
    __extends(DefaultPlugin, _super);
    function DefaultPlugin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    //should never be be called since this is a non-issue plugin
    DefaultPlugin.prototype.renderGroupActions = function () {
        return null;
    };
    DefaultPlugin.displayName = 'DefaultPlugin';
    return DefaultPlugin;
}(BasePlugin));
export { DefaultPlugin };
//# sourceMappingURL=defaultPlugin.jsx.map