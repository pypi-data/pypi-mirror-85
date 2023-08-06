import { __extends } from "tslib";
import React from 'react';
import DefaultIssuePlugin from 'app/plugins/defaultIssuePlugin';
import Settings from './components/settings';
import IssueActions from './components/issueActions';
var Jira = /** @class */ (function (_super) {
    __extends(Jira, _super);
    function Jira() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.displayName = 'Jira';
        return _this;
    }
    Jira.prototype.renderSettings = function (props) {
        return <Settings plugin={this.plugin} {...props}/>;
    };
    Jira.prototype.renderGroupActions = function (props) {
        return <IssueActions {...props}/>;
    };
    return Jira;
}(DefaultIssuePlugin));
export default Jira;
//# sourceMappingURL=index.jsx.map