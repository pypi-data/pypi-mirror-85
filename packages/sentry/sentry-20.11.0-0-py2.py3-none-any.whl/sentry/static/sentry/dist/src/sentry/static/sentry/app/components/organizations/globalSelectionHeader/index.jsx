import { __extends, __read, __rest } from "tslib";
import * as ReactRouter from 'react-router';
import React from 'react';
import partition from 'lodash/partition';
import ConfigStore from 'app/stores/configStore';
import withOrganization from 'app/utils/withOrganization';
import withProjectsSpecified from 'app/utils/withProjectsSpecified';
import GlobalSelectionHeader from './globalSelectionHeader';
import InitializeGlobalSelectionHeader from './initializeGlobalSelectionHeader';
var GlobalSelectionHeaderContainer = /** @class */ (function (_super) {
    __extends(GlobalSelectionHeaderContainer, _super);
    function GlobalSelectionHeaderContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getProjects = function () {
            var _a = _this.props, organization = _a.organization, projects = _a.projects;
            var isSuperuser = ConfigStore.get('user').isSuperuser;
            var isOrgAdmin = organization.access.includes('org:admin');
            var _b = __read(partition(projects, function (project) { return project.isMember; }), 2), memberProjects = _b[0], nonMemberProjects = _b[1];
            if (isSuperuser || isOrgAdmin) {
                return [memberProjects, nonMemberProjects];
            }
            return [memberProjects, []];
        };
        return _this;
    }
    GlobalSelectionHeaderContainer.prototype.render = function () {
        var _a = this.props, loadingProjects = _a.loadingProjects, location = _a.location, organization = _a.organization, router = _a.router, routes = _a.routes, defaultSelection = _a.defaultSelection, forceProject = _a.forceProject, shouldForceProject = _a.shouldForceProject, hasCustomRouting = _a.hasCustomRouting, skipLoadLastUsed = _a.skipLoadLastUsed, showAbsolute = _a.showAbsolute, props = __rest(_a, ["loadingProjects", "location", "organization", "router", "routes", "defaultSelection", "forceProject", "shouldForceProject", "hasCustomRouting", "skipLoadLastUsed", "showAbsolute"]);
        var enforceSingleProject = !organization.features.includes('global-views');
        var _b = __read(this.getProjects(), 2), memberProjects = _b[0], nonMemberProjects = _b[1];
        // We can initialize before ProjectsStore is fully loaded if we don't need to enforce single project.
        return (<React.Fragment>
        {(!loadingProjects || (!shouldForceProject && !enforceSingleProject)) && (<InitializeGlobalSelectionHeader location={location} skipLoadLastUsed={!!skipLoadLastUsed} router={router} organization={organization} defaultSelection={defaultSelection} forceProject={forceProject} isDisabled={!!hasCustomRouting} shouldForceProject={!!shouldForceProject} shouldEnforceSingleProject={!hasCustomRouting && enforceSingleProject} memberProjects={memberProjects} showAbsolute={showAbsolute}/>)}
        <GlobalSelectionHeader {...props} loadingProjects={loadingProjects} location={location} organization={organization} router={!hasCustomRouting ? router : null} routes={routes} shouldForceProject={!!shouldForceProject} defaultSelection={defaultSelection} forceProject={forceProject} memberProjects={memberProjects} nonMemberProjects={nonMemberProjects} showAbsolute={showAbsolute}/>
      </React.Fragment>);
    };
    return GlobalSelectionHeaderContainer;
}(React.Component));
export default withOrganization(withProjectsSpecified(ReactRouter.withRouter(GlobalSelectionHeaderContainer)));
//# sourceMappingURL=index.jsx.map