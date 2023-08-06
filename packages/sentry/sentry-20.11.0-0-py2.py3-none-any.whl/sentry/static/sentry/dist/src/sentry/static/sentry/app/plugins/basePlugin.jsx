import React from 'react';
import Settings from 'app/plugins/components/settings';
var BasePlugin = /** @class */ (function () {
    function BasePlugin(data) {
        this.plugin = data;
    }
    BasePlugin.prototype.renderSettings = function (props) {
        return <Settings plugin={this.plugin} {...props}/>;
    };
    return BasePlugin;
}());
export default BasePlugin;
//# sourceMappingURL=basePlugin.jsx.map