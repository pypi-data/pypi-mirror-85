import { __assign } from "tslib";
import Reflux from 'reflux';
import OrganizationActions from 'app/actions/organizationActions';
import ProjectActions from 'app/actions/projectActions';
import TeamActions from 'app/actions/teamActions';
import { ORGANIZATION_FETCH_ERROR_TYPES } from 'app/constants';
var storeConfig = {
    init: function () {
        this.reset();
        this.listenTo(OrganizationActions.update, this.onUpdate);
        this.listenTo(OrganizationActions.fetchOrg, this.reset);
        this.listenTo(OrganizationActions.fetchOrgError, this.onFetchOrgError);
        // fill in teams and projects if they are loaded
        this.listenTo(ProjectActions.loadProjects, this.onLoadProjects);
        this.listenTo(TeamActions.loadTeams, this.onLoadTeams);
        // mark the store as dirty if projects or teams change
        this.listenTo(ProjectActions.createSuccess, this.onProjectOrTeamChange);
        this.listenTo(ProjectActions.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(ProjectActions.changeSlug, this.onProjectOrTeamChange);
        this.listenTo(ProjectActions.addTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(ProjectActions.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(TeamActions.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(TeamActions.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(TeamActions.createTeamSuccess, this.onProjectOrTeamChange);
    },
    reset: function () {
        this.loading = true;
        this.error = null;
        this.errorType = null;
        this.organization = null;
        this.dirty = false;
        this.trigger(this.get());
    },
    onUpdate: function (updatedOrg, _a) {
        var _b = (_a === void 0 ? {} : _a).replace, replace = _b === void 0 ? false : _b;
        this.loading = false;
        this.error = null;
        this.errorType = null;
        this.organization = replace ? updatedOrg : __assign(__assign({}, this.organization), updatedOrg);
        this.dirty = false;
        this.trigger(this.get());
    },
    onFetchOrgError: function (err) {
        this.organization = null;
        this.errorType = null;
        switch (err === null || err === void 0 ? void 0 : err.status) {
            case 404:
                this.errorType = ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND;
                break;
            default:
        }
        this.loading = false;
        this.error = err;
        this.dirty = false;
        this.trigger(this.get());
    },
    onProjectOrTeamChange: function () {
        // mark the store as dirty so the next fetch will trigger an org details refetch
        this.dirty = true;
    },
    onLoadProjects: function (projects) {
        if (this.organization) {
            // sort projects to mimic how they are received from backend
            projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); });
            this.organization = __assign(__assign({}, this.organization), { projects: projects });
            this.trigger(this.get());
        }
    },
    onLoadTeams: function (teams) {
        if (this.organization) {
            // sort teams to mimic how they are received from backend
            teams.sort(function (a, b) { return a.slug.localeCompare(b.slug); });
            this.organization = __assign(__assign({}, this.organization), { teams: teams });
            this.trigger(this.get());
        }
    },
    get: function () {
        return {
            organization: this.organization,
            error: this.error,
            loading: this.loading,
            errorType: this.errorType,
            dirty: this.dirty,
        };
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=organizationStore.jsx.map