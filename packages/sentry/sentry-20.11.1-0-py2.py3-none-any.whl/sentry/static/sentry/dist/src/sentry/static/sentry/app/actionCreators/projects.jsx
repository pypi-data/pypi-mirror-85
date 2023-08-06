import { __assign } from "tslib";
import chunk from 'lodash/chunk';
import debounce from 'lodash/debounce';
import { addLoadingMessage, addErrorMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import ProjectActions from 'app/actions/projectActions';
import ProjectsStatsStore from 'app/stores/projectsStatsStore';
export function update(api, params) {
    ProjectActions.update(params.projectId, params.data);
    var endpoint = "/projects/" + params.orgId + "/" + params.projectId + "/";
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: params.data,
    })
        .then(function (data) {
        ProjectActions.updateSuccess(data);
        return data;
    }, function (err) {
        ProjectActions.updateError(err, params.projectId);
        throw err;
    });
}
export function loadStats(api, params) {
    ProjectActions.loadStats(params.orgId, params.data);
    var endpoint = "/organizations/" + params.orgId + "/stats/";
    api.request(endpoint, {
        query: params.query,
        success: function (data) {
            ProjectActions.loadStatsSuccess(data);
        },
        error: function (data) {
            ProjectActions.loadStatsError(data);
        },
    });
}
// This is going to queue up a list of project ids we need to fetch stats for
// Will be cleared when debounced function fires
var _projectStatsToFetch = new Set();
// Max projects to query at a time, otherwise if we fetch too many in the same request
// it can timeout
var MAX_PROJECTS_TO_FETCH = 10;
var _queryForStats = function (api, projects, orgId, additionalQuery) {
    var idQueryParams = projects.map(function (project) { return "id:" + project; }).join(' ');
    var endpoint = "/organizations/" + orgId + "/projects/";
    var query = __assign({ statsPeriod: '24h', query: idQueryParams }, additionalQuery);
    return api.requestPromise(endpoint, {
        query: query,
    });
};
export var _debouncedLoadStats = debounce(function (api, projectSet, params) {
    var storedProjects = ProjectsStatsStore.getAll();
    var existingProjectStats = Object.values(storedProjects).map(function (_a) {
        var id = _a.id;
        return id;
    });
    var projects = Array.from(projectSet).filter(function (project) { return !existingProjectStats.includes(project); });
    if (!projects.length) {
        _projectStatsToFetch.clear();
        return;
    }
    // Split projects into more manageable chunks to query, otherwise we can
    // potentially face server timeouts
    var queries = chunk(projects, MAX_PROJECTS_TO_FETCH).map(function (chunkedProjects) {
        return _queryForStats(api, chunkedProjects, params.orgId, params.query);
    });
    Promise.all(queries)
        .then(function (results) {
        ProjectActions.loadStatsForProjectSuccess(results.reduce(function (acc, result) { return acc.concat(result); }, []));
    })
        .catch(function () {
        addErrorMessage(t('Unable to fetch all project stats'));
    });
    // Reset projects list
    _projectStatsToFetch.clear();
}, 50);
export function loadStatsForProject(api, project, params) {
    // Queue up a list of projects that we need stats for
    // and call a debounced function to fetch stats for list of projects
    _projectStatsToFetch.add(project);
    _debouncedLoadStats(api, _projectStatsToFetch, params);
}
export function setActiveProject(project) {
    ProjectActions.setActive(project);
}
export function removeProject(api, orgId, project) {
    var endpoint = "/projects/" + orgId + "/" + project.slug + "/";
    ProjectActions.removeProject(project);
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function () {
        ProjectActions.removeProjectSuccess(project);
        addSuccessMessage(tct('[project] was successfully removed', { project: project.slug }));
    }, function (err) {
        ProjectActions.removeProjectError(project);
        addErrorMessage(tct('Error removing [project]', { project: project.slug }));
        throw err;
    });
}
export function transferProject(api, orgId, project, email) {
    var endpoint = "/projects/" + orgId + "/" + project.slug + "/transfer/";
    return api
        .requestPromise(endpoint, {
        method: 'POST',
        data: {
            email: email,
        },
    })
        .then(function () {
        addSuccessMessage(tct('A request was sent to move [project] to a different organization', {
            project: project.slug,
        }));
    }, function (err) {
        addErrorMessage(tct('Error transferring [project]', { project: project.slug }));
        throw err;
    });
}
/**
 * Associate a team with a project
 */
/**
 *  Adds a team to a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param team Team data object
 */
export function addTeamToProject(api, orgSlug, projectSlug, team) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/teams/" + team.slug + "/";
    addLoadingMessage();
    ProjectActions.addTeam(team);
    return api
        .requestPromise(endpoint, {
        method: 'POST',
    })
        .then(function (project) {
        addSuccessMessage(tct('[team] has been added to the [project] project', {
            team: "#" + team.slug,
            project: projectSlug,
        }));
        ProjectActions.addTeamSuccess(team, projectSlug);
        ProjectActions.updateSuccess(project);
    }, function (err) {
        addErrorMessage(tct('Unable to add [team] to the [project] project', {
            team: "#" + team.slug,
            project: projectSlug,
        }));
        ProjectActions.addTeamError();
        throw err;
    });
}
/**
 * Removes a team from a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param teamSlug Team Slug
 */
export function removeTeamFromProject(api, orgSlug, projectSlug, teamSlug) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/teams/" + teamSlug + "/";
    addLoadingMessage();
    ProjectActions.removeTeam(teamSlug);
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function (project) {
        addSuccessMessage(tct('[team] has been removed from the [project] project', {
            team: "#" + teamSlug,
            project: projectSlug,
        }));
        ProjectActions.removeTeamSuccess(teamSlug, projectSlug);
        ProjectActions.updateSuccess(project);
    }, function (err) {
        addErrorMessage(tct('Unable to remove [team] from the [project] project', {
            team: "#" + teamSlug,
            project: projectSlug,
        }));
        ProjectActions.removeTeamError(err);
        throw err;
    });
}
/**
 * Change a project's slug
 *
 * @param prev Previous slug
 * @param next New slug
 */
export function changeProjectSlug(prev, next) {
    ProjectActions.changeSlug(prev, next);
}
/**
 * Send a sample event
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 */
export function sendSampleEvent(api, orgSlug, projectSlug) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/create-sample/";
    return api.requestPromise(endpoint, {
        method: 'POST',
    });
}
/**
 * Creates a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param team The team slug to assign the project to
 * @param name Name of the project
 * @param platform The platform key of the project
 * @param options Additional options such as creating default alert rules
 */
export function createProject(api, orgSlug, team, name, platform, options) {
    if (options === void 0) { options = {}; }
    return api.requestPromise("/teams/" + orgSlug + "/" + team + "/projects/", {
        method: 'POST',
        data: { name: name, platform: platform, default_rules: options.defaultRules },
    });
}
/**
 * Load platform documentation specific to the project. The DSN and various
 * other project specific secrets will be included in the documentation.
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param platform Project platform.
 */
export function loadDocs(api, orgSlug, projectSlug, platform) {
    return api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/docs/" + platform + "/");
}
/**
 * Load the counts of my projects and all projects for the current user
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 */
export function fetchProjectsCount(api, orgSlug) {
    return api.requestPromise("/organizations/" + orgSlug + "/projects-count/");
}
//# sourceMappingURL=projects.jsx.map