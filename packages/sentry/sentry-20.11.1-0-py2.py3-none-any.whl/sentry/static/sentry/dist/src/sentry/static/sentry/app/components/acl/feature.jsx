import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import HookStore from 'app/stores/hookStore';
import SentryTypes from 'app/sentryTypes';
import withConfig from 'app/utils/withConfig';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import { isRenderFunc } from 'app/utils/isRenderFunc';
import ComingSoon from './comingSoon';
/**
 * Component to handle feature flags.
 */
var Feature = /** @class */ (function (_super) {
    __extends(Feature, _super);
    function Feature() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Feature.prototype.getAllFeatures = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, config = _a.config;
        return {
            configFeatures: config.features ? Array.from(config.features) : [],
            organization: (organization && organization.features) || [],
            project: (project && project.features) || [],
        };
    };
    Feature.prototype.hasFeature = function (feature, features) {
        var shouldMatchOnlyProject = feature.match(/^projects:(.+)/);
        var shouldMatchOnlyOrg = feature.match(/^organizations:(.+)/);
        // Array of feature strings
        var configFeatures = features.configFeatures, organization = features.organization, project = features.project;
        // Check config store first as this overrides features scoped to org or
        // project contexts.
        if (configFeatures.includes(feature)) {
            return true;
        }
        if (shouldMatchOnlyProject) {
            return project.includes(shouldMatchOnlyProject[1]);
        }
        if (shouldMatchOnlyOrg) {
            return organization.includes(shouldMatchOnlyOrg[1]);
        }
        // default, check all feature arrays
        return organization.includes(feature) || project.includes(feature);
    };
    Feature.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, features = _a.features, renderDisabled = _a.renderDisabled, hookName = _a.hookName, organization = _a.organization, project = _a.project, requireAll = _a.requireAll;
        var allFeatures = this.getAllFeatures();
        var method = requireAll ? 'every' : 'some';
        var hasFeature = !features || features[method](function (feat) { return _this.hasFeature(feat, allFeatures); });
        // Default renderDisabled to the ComingSoon component
        var customDisabledRender = renderDisabled === false
            ? false
            : typeof renderDisabled === 'function'
                ? renderDisabled
                : function () { return <ComingSoon />; };
        // Override the renderDisabled function with a hook store function if there
        // is one registered for the feature.
        if (hookName) {
            var hooks = HookStore.get(hookName);
            if (hooks.length > 0) {
                customDisabledRender = hooks[0];
            }
        }
        var renderProps = {
            organization: organization,
            project: project,
            features: features,
            hasFeature: hasFeature,
        };
        if (!hasFeature && customDisabledRender !== false) {
            return customDisabledRender(__assign({ children: children }, renderProps));
        }
        if (isRenderFunc(children)) {
            return children(__assign({ renderDisabled: renderDisabled }, renderProps));
        }
        return hasFeature && children ? children : null;
    };
    Feature.propTypes = {
        organization: SentryTypes.Organization,
        project: SentryTypes.Project,
        config: SentryTypes.Config.isRequired,
        features: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
        requireAll: PropTypes.bool,
        renderDisabled: PropTypes.oneOfType([PropTypes.func, PropTypes.bool]),
        hookName: PropTypes.string,
        children: PropTypes.oneOfType([PropTypes.func, PropTypes.node]),
    };
    Feature.defaultProps = {
        renderDisabled: false,
        requireAll: true,
    };
    return Feature;
}(React.Component));
export default withOrganization(withProject(withConfig(Feature)));
//# sourceMappingURL=feature.jsx.map