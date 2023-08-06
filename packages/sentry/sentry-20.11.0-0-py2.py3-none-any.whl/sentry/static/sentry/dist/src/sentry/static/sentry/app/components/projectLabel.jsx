import { __extends, __rest } from "tslib";
import React from 'react';
import { Project as ProjectPropType } from 'app/sentryTypes';
var ProjectLabel = /** @class */ (function (_super) {
    __extends(ProjectLabel, _super);
    function ProjectLabel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectLabel.prototype.render = function () {
        var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
        return (<span className="project-label" {...props}>
        <span className="project-name">{project.slug}</span>
      </span>);
    };
    ProjectLabel.propTypes = {
        project: ProjectPropType.isRequired,
    };
    return ProjectLabel;
}(React.PureComponent));
export default ProjectLabel;
//# sourceMappingURL=projectLabel.jsx.map