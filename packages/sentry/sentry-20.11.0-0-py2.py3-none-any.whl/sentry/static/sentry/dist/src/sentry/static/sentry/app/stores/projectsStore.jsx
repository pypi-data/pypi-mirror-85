import { __assign, __read, __spread } from "tslib";
import Reflux from 'reflux';
import ProjectActions from 'app/actions/projectActions';
import TeamActions from 'app/actions/teamActions';
var storeConfig = {
    itemsById: {},
    loading: true,
    init: function () {
        this.reset();
        this.listenTo(ProjectActions.addTeamSuccess, this.onAddTeam);
        this.listenTo(ProjectActions.changeSlug, this.onChangeSlug);
        this.listenTo(ProjectActions.createSuccess, this.onCreateSuccess);
        this.listenTo(ProjectActions.loadProjects, this.loadInitialData);
        this.listenTo(ProjectActions.loadStatsSuccess, this.onStatsLoadSuccess);
        this.listenTo(ProjectActions.removeTeamSuccess, this.onRemoveTeam);
        this.listenTo(ProjectActions.reset, this.reset);
        this.listenTo(ProjectActions.updateSuccess, this.onUpdateSuccess);
        this.listenTo(TeamActions.removeTeamSuccess, this.onDeleteTeam);
    },
    reset: function () {
        this.itemsById = {};
        this.loading = true;
    },
    loadInitialData: function (items) {
        this.itemsById = items.reduce(function (map, project) {
            map[project.id] = project;
            return map;
        }, {});
        this.loading = false;
        this.trigger(new Set(Object.keys(this.itemsById)));
    },
    onChangeSlug: function (prevSlug, newSlug) {
        var _a;
        var prevProject = this.getBySlug(prevSlug);
        // This shouldn't happen
        if (!prevProject) {
            return;
        }
        var newProject = __assign(__assign({}, prevProject), { slug: newSlug });
        this.itemsById = __assign(__assign({}, this.itemsById), (_a = {}, _a[newProject.id] = newProject, _a));
        // Ideally we'd always trigger this.itemsById, but following existing patterns
        // so we don't break things
        this.trigger(new Set([prevProject.id]));
    },
    onCreateSuccess: function (project) {
        var _a;
        this.itemsById = __assign(__assign({}, this.itemsById), (_a = {}, _a[project.id] = project, _a));
        this.trigger(new Set([project.id]));
    },
    onUpdateSuccess: function (data) {
        var _a;
        var project = this.getById(data.id);
        if (!project) {
            return;
        }
        var newProject = Object.assign({}, project, data);
        this.itemsById = __assign(__assign({}, this.itemsById), (_a = {}, _a[project.id] = newProject, _a));
        this.trigger(new Set([data.id]));
    },
    onStatsLoadSuccess: function (data) {
        var _this = this;
        var touchedIds = [];
        Object.entries(data || {}).forEach(function (_a) {
            var _b = __read(_a, 2), projectId = _b[0], stats = _b[1];
            if (projectId in _this.itemsById) {
                _this.itemsById[projectId].stats = stats;
                touchedIds.push(projectId);
            }
        });
        this.trigger(new Set(touchedIds));
    },
    /**
     * Listener for when a team is completely removed
     *
     * @param teamSlug Team Slug
     */
    onDeleteTeam: function (teamSlug) {
        var _this = this;
        // Look for team in all projects
        var projectIds = this.getWithTeam(teamSlug).map(function (projectWithTeam) {
            _this.removeTeamFromProject(teamSlug, projectWithTeam);
            return projectWithTeam.id;
        });
        this.trigger(new Set([projectIds]));
    },
    onRemoveTeam: function (teamSlug, projectSlug) {
        var project = this.getBySlug(projectSlug);
        if (!project) {
            return;
        }
        this.removeTeamFromProject(teamSlug, project);
        this.trigger(new Set([project.id]));
    },
    onAddTeam: function (team, projectSlug) {
        var _a;
        var project = this.getBySlug(projectSlug);
        // Don't do anything if we can't find a project
        if (!project) {
            return;
        }
        this.itemsById = __assign(__assign({}, this.itemsById), (_a = {}, _a[project.id] = __assign(__assign({}, project), { teams: __spread(project.teams, [team]) }), _a));
        this.trigger(new Set([project.id]));
    },
    // Internal method, does not trigger
    removeTeamFromProject: function (teamSlug, project) {
        var _a;
        var newTeams = project.teams.filter(function (_a) {
            var slug = _a.slug;
            return slug !== teamSlug;
        });
        this.itemsById = __assign(__assign({}, this.itemsById), (_a = {}, _a[project.id] = __assign(__assign({}, project), { teams: newTeams }), _a));
    },
    /**
     * Returns a list of projects that has the specified team
     *
     * @param {String} teamSlug Slug of team to find in projects
     */
    getWithTeam: function (teamSlug) {
        return this.getAll().filter(function (_a) {
            var teams = _a.teams;
            return teams.find(function (_a) {
                var slug = _a.slug;
                return slug === teamSlug;
            });
        });
    },
    getAll: function () {
        return Object.values(this.itemsById).sort(function (a, b) {
            if (a.slug > b.slug) {
                return 1;
            }
            if (a.slug < b.slug) {
                return -1;
            }
            return 0;
        });
    },
    getById: function (id) {
        return this.getAll().find(function (project) { return project.id === id; });
    },
    getBySlug: function (slug) {
        return this.getAll().find(function (project) { return project.slug === slug; });
    },
    getBySlugs: function (slugs) {
        return this.getAll().filter(function (project) { return slugs.includes(project.slug); });
    },
    getState: function (slugs) {
        return {
            projects: slugs ? this.getBySlugs(slugs) : this.getAll(),
            loading: this.loading,
        };
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=projectsStore.jsx.map