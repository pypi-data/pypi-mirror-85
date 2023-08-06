import { __assign, __extends, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import PlatformList from 'app/components/platformList';
import Tooltip from 'app/components/tooltip';
import SentryTypes from 'app/sentryTypes';
var ProjectAvatar = /** @class */ (function (_super) {
    __extends(ProjectAvatar, _super);
    function ProjectAvatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getPlatforms = function (project) {
            // `platform` is a user selectable option that is performed during the onboarding process. The reason why this
            // is not the default is because there currently is no way to update it. Fallback to this if project does not
            // have recent events with a platform.
            if (project && project.platform) {
                return [project.platform];
            }
            return [];
        };
        return _this;
    }
    ProjectAvatar.prototype.render = function () {
        var _a = this.props, project = _a.project, hasTooltip = _a.hasTooltip, tooltip = _a.tooltip, props = __rest(_a, ["project", "hasTooltip", "tooltip"]);
        return (<Tooltip disabled={!hasTooltip} title={tooltip}>
        <PlatformList platforms={this.getPlatforms(project)} {...props} max={1}/>
      </Tooltip>);
    };
    ProjectAvatar.propTypes = __assign({ project: PropTypes.oneOfType([
            PropTypes.shape({ slug: PropTypes.string }),
            SentryTypes.Project,
        ]).isRequired }, BaseAvatar.propTypes);
    return ProjectAvatar;
}(React.Component));
export default ProjectAvatar;
//# sourceMappingURL=projectAvatar.jsx.map