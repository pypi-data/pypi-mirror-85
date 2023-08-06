import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { createDefaultRule, createRuleFromEventView, } from 'app/views/settings/incidentRules/constants';
import RuleForm from './ruleForm';
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
var IncidentRulesCreate = /** @class */ (function (_super) {
    __extends(IncidentRulesCreate, _super);
    function IncidentRulesCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var router = _this.props.router;
            var orgId = _this.props.params.orgId;
            router.push("/organizations/" + orgId + "/alerts/rules/");
        };
        return _this;
    }
    IncidentRulesCreate.prototype.render = function () {
        var _a = this.props, project = _a.project, eventView = _a.eventView, sessionId = _a.sessionId, props = __rest(_a, ["project", "eventView", "sessionId"]);
        var defaultRule = eventView
            ? createRuleFromEventView(eventView)
            : createDefaultRule();
        return (<RuleForm onSubmitSuccess={this.handleSubmitSuccess} rule={__assign(__assign({}, defaultRule), { projects: [project.slug] })} sessionId={sessionId} project={project} {...props}/>);
    };
    return IncidentRulesCreate;
}(React.Component));
export default IncidentRulesCreate;
//# sourceMappingURL=create.jsx.map