import { __extends } from "tslib";
import React from 'react';
import NoProjectMessage from 'app/components/noProjectMessage';
import withProjects from 'app/utils/withProjects';
var LightWeightNoProjectMessage = /** @class */ (function (_super) {
    __extends(LightWeightNoProjectMessage, _super);
    function LightWeightNoProjectMessage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LightWeightNoProjectMessage.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, loadingProjects = _a.loadingProjects;
        return (<NoProjectMessage {...this.props} projects={projects} loadingProjects={!('projects' in organization) && loadingProjects}/>);
    };
    return LightWeightNoProjectMessage;
}(React.Component));
export default withProjects(LightWeightNoProjectMessage);
//# sourceMappingURL=lightWeightNoProjectMessage.jsx.map