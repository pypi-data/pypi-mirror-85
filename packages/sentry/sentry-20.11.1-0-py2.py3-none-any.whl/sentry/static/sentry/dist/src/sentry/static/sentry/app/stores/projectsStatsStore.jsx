import { __assign } from "tslib";
import Reflux from 'reflux';
import ProjectActions from 'app/actions/projectActions';
/**
 * This is a store specifically used by the dashboard, so that we can
 * clear the store when the Dashboard unmounts
 * (as to not disrupt ProjectsStore which a lot more components use)
 */
var projectsStatsStore = {
    itemsBySlug: {},
    init: function () {
        this.reset();
        this.listenTo(ProjectActions.loadStatsForProjectSuccess, this.onStatsLoadSuccess);
        this.listenTo(ProjectActions.update, this.onUpdate);
        this.listenTo(ProjectActions.updateError, this.onUpdateError);
    },
    getInitialState: function () {
        return this.itemsBySlug;
    },
    reset: function () {
        this.itemsBySlug = {};
        this.updatingItems = new Map();
    },
    onStatsLoadSuccess: function (projects) {
        var _this = this;
        projects.forEach(function (project) {
            _this.itemsBySlug[project.slug] = project;
        });
        this.trigger(this.itemsBySlug);
    },
    /**
     * Optimistic updates
     * @param projectSlug Project slug
     * @param data Project data
     */
    onUpdate: function (projectSlug, data) {
        var _a;
        var project = this.getBySlug(projectSlug);
        this.updatingItems.set(projectSlug, project);
        if (!project) {
            return;
        }
        var newProject = __assign(__assign({}, project), data);
        this.itemsBySlug = __assign(__assign({}, this.itemsBySlug), (_a = {}, _a[project.slug] = newProject, _a));
        this.trigger(this.itemsBySlug);
    },
    onUpdateSuccess: function (data) {
        // Remove project from updating map
        this.updatingItems.delete(data.slug);
    },
    /**
     * Revert project data when there was an error updating project details
     * @param err Error object
     * @param data Previous project data
     */
    onUpdateError: function (_err, projectSlug) {
        var _a;
        var project = this.updatingItems.get(projectSlug);
        if (!project) {
            return;
        }
        this.updatingItems.delete(projectSlug);
        // Restore old project
        this.itemsBySlug = __assign(__assign({}, this.itemsBySlug), (_a = {}, _a[project.slug] = __assign({}, project), _a));
        this.trigger(this.itemsBySlug);
    },
    getAll: function () {
        return this.itemsBySlug;
    },
    getBySlug: function (slug) {
        return this.itemsBySlug[slug];
    },
};
export default Reflux.createStore(projectsStatsStore);
//# sourceMappingURL=projectsStatsStore.jsx.map