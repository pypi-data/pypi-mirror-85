import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import SentryTypes from 'app/sentryTypes';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Currently wraps component with project from context
 */
var withProject = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
            return (<WrappedComponent {...__assign({ project: project !== null && project !== void 0 ? project : this.context.project }, props)}/>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withProject(" + getDisplayName(WrappedComponent) + ")",
    _a.contextTypes = {
        project: SentryTypes.Project,
    },
    _a; };
export default withProject;
//# sourceMappingURL=withProject.jsx.map