import { __extends } from "tslib";
import React from 'react';
import BasePlugin from 'app/plugins/basePlugin';
import Settings from './components/settings';
var SessionStackPlugin = /** @class */ (function (_super) {
    __extends(SessionStackPlugin, _super);
    function SessionStackPlugin() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.displayName = 'SessionStack';
        return _this;
    }
    //should never be be called since this is a non-issue plugin
    SessionStackPlugin.prototype.renderGroupActions = function () {
        return null;
    };
    SessionStackPlugin.prototype.renderSettings = function (props) {
        return <Settings plugin={this.plugin} {...props}/>;
    };
    return SessionStackPlugin;
}(BasePlugin));
export default SessionStackPlugin;
//# sourceMappingURL=index.jsx.map