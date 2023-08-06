import { __extends } from "tslib";
import React from 'react';
import BasePlugin from 'app/plugins/basePlugin';
import IssueActions from 'app/plugins/components/issueActions';
var DefaultIssuePlugin = /** @class */ (function (_super) {
    __extends(DefaultIssuePlugin, _super);
    function DefaultIssuePlugin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DefaultIssuePlugin.prototype.renderGroupActions = function (props) {
        return <IssueActions {...props}/>;
    };
    return DefaultIssuePlugin;
}(BasePlugin));
export { DefaultIssuePlugin };
export default DefaultIssuePlugin;
//# sourceMappingURL=defaultIssuePlugin.jsx.map