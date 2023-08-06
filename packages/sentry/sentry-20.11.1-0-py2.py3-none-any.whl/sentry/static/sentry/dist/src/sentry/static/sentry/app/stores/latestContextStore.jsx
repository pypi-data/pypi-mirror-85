import { __assign } from "tslib";
import Reflux from 'reflux';
import ProjectActions from 'app/actions/projectActions';
import OrganizationActions from 'app/actions/organizationActions';
import OrganizationsActions from 'app/actions/organizationsActions';
import NavigationActions from 'app/actions/navigationActions';
// Keeps track of last usable project/org
// this currently won't track when users navigate out of a org/project completely,
// it tracks only if a user switches into a new org/project
//
// Only keep slug so that people don't get the idea to access org/project data here
// Org/project data is currently in organizationsStore/projectsStore
var storeConfig = {
    state: {
        project: null,
        lastProject: null,
        organization: null,
        environment: null,
        lastRoute: null,
    },
    getInitialState: function () {
        return this.state;
    },
    init: function () {
        this.reset();
        this.listenTo(ProjectActions.setActive, this.onSetActiveProject);
        this.listenTo(ProjectActions.updateSuccess, this.onUpdateProject);
        this.listenTo(OrganizationsActions.setActive, this.onSetActiveOrganization);
        this.listenTo(OrganizationsActions.update, this.onUpdateOrganization);
        this.listenTo(OrganizationActions.update, this.onUpdateOrganization);
        this.listenTo(NavigationActions.setLastRoute, this.onSetLastRoute);
    },
    reset: function () {
        this.state = {
            project: null,
            lastProject: null,
            organization: null,
            environment: null,
            lastRoute: null,
        };
        return this.state;
    },
    onSetLastRoute: function (route) {
        this.state = __assign(__assign({}, this.state), { lastRoute: route });
        this.trigger(this.state);
    },
    onUpdateOrganization: function (org) {
        // Don't do anything if base/target orgs are falsey
        if (!this.state.organization) {
            return;
        }
        if (!org) {
            return;
        }
        // Check to make sure current active org is what has been updated
        if (org.slug !== this.state.organization.slug) {
            return;
        }
        this.state = __assign(__assign({}, this.state), { organization: org });
        this.trigger(this.state);
    },
    onSetActiveOrganization: function (org) {
        if (!org) {
            this.state = __assign(__assign({}, this.state), { organization: null, project: null });
        }
        else if (!this.state.organization || this.state.organization.slug !== org.slug) {
            // Update only if different
            this.state = __assign(__assign({}, this.state), { organization: org, project: null });
        }
        this.trigger(this.state);
    },
    onSetActiveProject: function (project) {
        if (!project) {
            this.state = __assign(__assign({}, this.state), { lastProject: this.state.project, project: null });
        }
        else if (!this.state.project || this.state.project.slug !== project.slug) {
            // Update only if different
            this.state = __assign(__assign({}, this.state), { lastProject: this.state.project, project: project });
        }
        this.trigger(this.state);
    },
    onUpdateProject: function (project) {
        this.state = __assign(__assign({}, this.state), { project: project });
        this.trigger(this.state);
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=latestContextStore.jsx.map