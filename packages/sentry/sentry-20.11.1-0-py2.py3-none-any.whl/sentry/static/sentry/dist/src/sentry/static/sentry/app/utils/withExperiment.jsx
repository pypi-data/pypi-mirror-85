import { __assign, __extends } from "tslib";
import React from 'react';
import ConfigStore from 'app/stores/configStore';
import { experimentConfig, unassignedValue } from 'app/data/experimentConfig';
import getDisplayName from 'app/utils/getDisplayName';
import { logExperiment } from 'app/utils/analytics';
import { ExperimentType, } from 'app/types/experiments';
/**
 * A HoC wrapper that injects `experimentAssignment` into a component
 *
 * This wrapper will automatically log exposure of the experiment upon
 * receiving the componentDidMount lifecycle event.
 *
 * For organization experiments, an organization object must be provided to the
 * component. You may wish to use the withOrganization HoC for this.
 *
 * If exposure logging upon mount is not desirable, The `injectLogExperiment`
 * option may be of use.
 *
 * NOTE: When using this you will have to type the `experimentAssignment` prop
 *       on your component. For this you should use the `ExperimentAssignment`
 *       mapped type.
 */
function withExperiment(Component, _a) {
    var _b;
    var experiment = _a.experiment, injectLogExperiment = _a.injectLogExperiment;
    return _b = /** @class */ (function (_super) {
            __extends(class_1, _super);
            function class_1() {
                var _this = _super !== null && _super.apply(this, arguments) || this;
                _this.logExperiment = function () {
                    return logExperiment({
                        key: experiment,
                        organization: _this.getProps().organization,
                    });
                };
                return _this;
            }
            // NOTE(ts): Because of the type complexity of this HoC, typescript
            // has a hard time understanding how to narrow Experiments[E]['type']
            // when we type assert on it.
            //
            // This means we have to do some typecasting to massage things into working
            // as expected.
            //
            // We DO guarantee the external API of this HoC is typed accurately.
            class_1.prototype.componentDidMount = function () {
                if (!injectLogExperiment) {
                    this.logExperiment();
                }
            };
            class_1.prototype.getProps = function () {
                return this.props;
            };
            Object.defineProperty(class_1.prototype, "config", {
                get: function () {
                    return experimentConfig[experiment];
                },
                enumerable: false,
                configurable: true
            });
            Object.defineProperty(class_1.prototype, "experimentAssignment", {
                get: function () {
                    var type = this.config.type;
                    if (type === ExperimentType.Organization) {
                        var key = experiment;
                        return this.getProps().organization.experiments[key];
                    }
                    if (type === ExperimentType.User) {
                        var key = experiment;
                        return ConfigStore.get('user').experiments[key];
                    }
                    return unassignedValue;
                },
                enumerable: false,
                configurable: true
            });
            class_1.prototype.render = function () {
                var WrappedComponent = Component;
                var props = __assign(__assign({ experimentAssignment: this.experimentAssignment }, (injectLogExperiment ? { logExperiment: this.logExperiment } : {})), this.props);
                return <WrappedComponent {...props}/>;
            };
            return class_1;
        }(React.Component)),
        _b.displayName = "withExperiment[" + experiment + "](" + getDisplayName(Component) + ")",
        _b;
}
export default withExperiment;
//# sourceMappingURL=withExperiment.jsx.map