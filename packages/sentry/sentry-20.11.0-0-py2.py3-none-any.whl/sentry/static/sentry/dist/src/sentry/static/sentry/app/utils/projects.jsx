import { __awaiter, __extends, __generator, __read, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import memoize from 'lodash/memoize';
import partition from 'lodash/partition';
import uniqBy from 'lodash/uniqBy';
import { defined } from 'app/utils';
import ProjectActions from 'app/actions/projectActions';
import ProjectsStore from 'app/stores/projectsStore';
import SentryTypes from 'app/sentryTypes';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
/**
 * This is a utility component that should be used to fetch an organization's projects (summary).
 * It can either fetch explicit projects (e.g. via slug) or a paginated list of projects.
 * These will be passed down to the render prop (`children`).
 *
 * The legacy way of handling this is that `ProjectSummary[]` is expected to be included in an
 * `Organization` as well as being saved to `ProjectsStore`.
 */
var Projects = /** @class */ (function (_super) {
    __extends(Projects, _super);
    function Projects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fetchedProjects: [],
            projectsFromStore: [],
            initiallyLoaded: false,
            fetching: false,
            isIncomplete: null,
            hasMore: null,
            prevSearch: null,
            nextCursor: null,
            fetchError: null,
        };
        /**
         * List of projects that need to be fetched via API
         */
        _this.fetchQueue = new Set();
        /**
         * Memoized function that returns a `Map<project.slug, project>`
         */
        _this.getProjectsMap = memoize(function (projects) { return new Map(projects.map(function (project) { return [project.slug, project]; })); });
        /**
         * When `props.slugs` is included, identifies what projects we already
         * have summaries for and what projects need to be fetched from API
         */
        _this.loadSpecificProjects = function () {
            var _a = _this.props, slugs = _a.slugs, projects = _a.projects;
            var projectsMap = _this.getProjectsMap(projects);
            // Split slugs into projects that are in store and not in store
            // (so we can request projects not in store)
            var _b = __read(partition(slugs, function (slug) { return projectsMap.has(slug); }), 2), inStore = _b[0], notInStore = _b[1];
            // Get the actual summaries of projects that are in store
            var projectsFromStore = inStore.map(function (slug) { return projectsMap.get(slug); }).filter(defined);
            // Add to queue
            notInStore.forEach(function (slug) { return _this.fetchQueue.add(slug); });
            _this.setState({
                // placeholders for projects we need to fetch
                fetchedProjects: notInStore.map(function (slug) { return ({ slug: slug }); }),
                // set initallyLoaded if any projects were fetched from store
                initiallyLoaded: !!inStore.length,
                projectsFromStore: projectsFromStore,
            });
            if (!notInStore.length) {
                return;
            }
            _this.fetchSpecificProjects();
        };
        /**
         * These will fetch projects via API (using project slug) provided by `this.fetchQueue`
         */
        _this.fetchSpecificProjects = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, orgId, passthroughPlaceholderProject, projects, fetchError, results, err_1, projectsMap, projectsOrPlaceholder;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, passthroughPlaceholderProject = _a.passthroughPlaceholderProject;
                        if (!this.fetchQueue.size) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            fetching: true,
                        });
                        projects = [];
                        fetchError = null;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchProjects(api, orgId, {
                                slugs: Array.from(this.fetchQueue),
                            })];
                    case 2:
                        results = (_b.sent()).results;
                        projects = results;
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        console.error(err_1); // eslint-disable-line no-console
                        fetchError = err_1;
                        return [3 /*break*/, 4];
                    case 4:
                        projectsMap = this.getProjectsMap(projects);
                        projectsOrPlaceholder = Array.from(this.fetchQueue)
                            .map(function (slug) {
                            return projectsMap.has(slug)
                                ? projectsMap.get(slug)
                                : !!passthroughPlaceholderProject
                                    ? { slug: slug }
                                    : null;
                        })
                            .filter(defined);
                        this.setState({
                            fetchedProjects: projectsOrPlaceholder,
                            isIncomplete: this.fetchQueue.size !== projects.length,
                            initiallyLoaded: true,
                            fetching: false,
                            fetchError: fetchError,
                        });
                        this.fetchQueue.clear();
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * If `props.slugs` is not provided, request from API a list of paginated project summaries
         * that are in `prop.orgId`.
         *
         * Provide render prop with results as well as `hasMore` to indicate there are more results.
         * Downstream consumers should use this to notify users so that they can e.g. narrow down
         * results using search
         */
        _this.loadAllProjects = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, orgId, limit, allProjects, _b, results, hasMore, nextCursor, err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, limit = _a.limit, allProjects = _a.allProjects;
                        this.setState({
                            fetching: true,
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchProjects(api, orgId, {
                                limit: limit,
                                allProjects: allProjects,
                            })];
                    case 2:
                        _b = _c.sent(), results = _b.results, hasMore = _b.hasMore, nextCursor = _b.nextCursor;
                        this.setState({
                            fetching: false,
                            fetchedProjects: results,
                            initiallyLoaded: true,
                            hasMore: hasMore,
                            nextCursor: nextCursor,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        console.error(err_2); // eslint-disable-line no-console
                        this.setState({
                            fetching: false,
                            fetchedProjects: [],
                            initiallyLoaded: true,
                            fetchError: err_2,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * This is an action provided to consumers for them to update the current projects
         * result set using a simple search query. You can allow the new results to either
         * be appended or replace the existing results.
         *
         * @param {String} search The search term to use
         * @param {Object} options Options object
         * @param {Boolean} options.append Results should be appended to existing list (otherwise, will replace)
         */
        _this.handleSearch = function (search, _a) {
            var append = (_a === void 0 ? {} : _a).append;
            return __awaiter(_this, void 0, void 0, function () {
                var _b, api, orgId, limit, prevSearch, cursor, _c, results_1, hasMore_1, nextCursor_1, err_3;
                return __generator(this, function (_d) {
                    switch (_d.label) {
                        case 0:
                            _b = this.props, api = _b.api, orgId = _b.orgId, limit = _b.limit;
                            prevSearch = this.state.prevSearch;
                            cursor = this.state.nextCursor;
                            this.setState({ fetching: true });
                            _d.label = 1;
                        case 1:
                            _d.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, fetchProjects(api, orgId, {
                                    search: search,
                                    limit: limit,
                                    prevSearch: prevSearch,
                                    cursor: cursor,
                                })];
                        case 2:
                            _c = _d.sent(), results_1 = _c.results, hasMore_1 = _c.hasMore, nextCursor_1 = _c.nextCursor;
                            this.setState(function (state) {
                                var fetchedProjects;
                                if (append) {
                                    // Remove duplicates
                                    fetchedProjects = uniqBy(__spread(state.fetchedProjects, results_1), function (_a) {
                                        var slug = _a.slug;
                                        return slug;
                                    });
                                }
                                else {
                                    fetchedProjects = results_1;
                                }
                                return {
                                    fetchedProjects: fetchedProjects,
                                    hasMore: hasMore_1,
                                    fetching: false,
                                    prevSearch: search,
                                    nextCursor: nextCursor_1,
                                };
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            err_3 = _d.sent();
                            console.error(err_3); // eslint-disable-line no-console
                            this.setState({
                                fetching: false,
                                fetchError: err_3,
                            });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    Projects.prototype.componentDidMount = function () {
        var slugs = this.props.slugs;
        if (slugs && !!slugs.length) {
            this.loadSpecificProjects();
        }
        else {
            this.loadAllProjects();
        }
    };
    Projects.prototype.render = function () {
        var _a = this.props, slugs = _a.slugs, children = _a.children;
        var renderProps = {
            // We want to make sure that at the minimum, we return a list of objects with only `slug`
            // while we load actual project data
            projects: this.state.initiallyLoaded
                ? __spread(this.state.fetchedProjects, this.state.projectsFromStore) : (slugs && slugs.map(function (slug) { return ({ slug: slug }); })) || [],
            // This is set when we fail to find some slugs from both store and API
            isIncomplete: this.state.isIncomplete,
            // This is state for when fetching data from API
            fetching: this.state.fetching,
            // Project results (from API) are paginated and there are more projects
            // that are not in the initial queryset
            hasMore: this.state.hasMore,
            // Calls API and searches for project, accepts a callback function with signature:
            //
            // fn(searchTerm, {append: bool})
            onSearch: this.handleSearch,
            // Reflects whether or not the initial fetch for the requested projects
            // was fulfilled
            initiallyLoaded: this.state.initiallyLoaded,
            // The error that occurred if fetching failed
            fetchError: this.state.fetchError,
        };
        return children(renderProps);
    };
    Projects.propTypes = {
        api: PropTypes.object.isRequired,
        orgId: PropTypes.string.isRequired,
        projects: PropTypes.arrayOf(SentryTypes.Project).isRequired,
        slugs: PropTypes.arrayOf(PropTypes.string),
        limit: PropTypes.number,
        allProjects: PropTypes.bool,
        passthroughPlaceholderProject: PropTypes.bool,
    };
    Projects.defaultProps = {
        passthroughPlaceholderProject: true,
    };
    return Projects;
}(React.Component));
export default withProjects(withApi(Projects));
function fetchProjects(api, orgId, _a) {
    var _b = _a === void 0 ? {} : _a, slugs = _b.slugs, search = _b.search, limit = _b.limit, prevSearch = _b.prevSearch, cursor = _b.cursor, allProjects = _b.allProjects;
    return __awaiter(this, void 0, void 0, function () {
        var query, _c, loading, projects, hasMore, nextCursor, _d, results, xhr, pageLinks, paginationObject;
        return __generator(this, function (_e) {
            switch (_e.label) {
                case 0:
                    query = {};
                    if (slugs && slugs.length) {
                        query.query = slugs.map(function (slug) { return "slug:" + slug; }).join(' ');
                    }
                    if (search) {
                        query.query = "" + (query.query ? query.query + " " : '') + search;
                    }
                    if (((!prevSearch && !search) || prevSearch === search) && cursor) {
                        query.cursor = cursor;
                    }
                    // "0" shouldn't be a valid value, so this check is fine
                    if (limit) {
                        query.per_page = limit;
                    }
                    if (allProjects) {
                        _c = ProjectsStore.getState(), loading = _c.loading, projects = _c.projects;
                        // If the projects store is loaded then return all projects from the store
                        if (!loading) {
                            return [2 /*return*/, {
                                    results: projects,
                                    hasMore: false,
                                }];
                        }
                        // Otherwise mark the query to fetch all projects from the API
                        query.all_projects = 1;
                    }
                    hasMore = false;
                    nextCursor = null;
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/projects/", {
                            includeAllArgs: true,
                            query: query,
                        })];
                case 1:
                    _d = __read.apply(void 0, [_e.sent(), 3]), results = _d[0], xhr = _d[2];
                    pageLinks = xhr && xhr.getResponseHeader('Link');
                    if (pageLinks) {
                        paginationObject = parseLinkHeader(pageLinks);
                        hasMore =
                            paginationObject &&
                                (paginationObject.next.results || paginationObject.previous.results);
                        nextCursor = paginationObject.next.cursor;
                    }
                    // populate the projects store if all projects were fetched
                    if (allProjects) {
                        ProjectActions.loadProjects(results);
                    }
                    return [2 /*return*/, {
                            results: results,
                            hasMore: hasMore,
                            nextCursor: nextCursor,
                        }];
            }
        });
    });
}
//# sourceMappingURL=projects.jsx.map