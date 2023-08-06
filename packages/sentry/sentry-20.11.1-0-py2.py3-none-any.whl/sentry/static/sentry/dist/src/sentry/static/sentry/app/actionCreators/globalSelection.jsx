import { __assign, __read, __rest, __spread } from "tslib";
import isInteger from 'lodash/isInteger';
import omit from 'lodash/omit';
import pick from 'lodash/pick';
import * as qs from 'query-string';
import * as Sentry from '@sentry/react';
import { DATE_TIME, LOCAL_STORAGE_KEY, URL_PARAM, } from 'app/constants/globalSelectionHeader';
import { defined } from 'app/utils';
import { getDefaultSelection, getStateFromQuery, } from 'app/components/organizations/globalSelectionHeader/utils';
import { getUtcDateString } from 'app/utils/dates';
import GlobalSelectionActions from 'app/actions/globalSelectionActions';
import localStorage from 'app/utils/localStorage';
// Reset values in global selection store
export function resetGlobalSelection() {
    GlobalSelectionActions.reset();
}
function getProjectIdFromProject(project) {
    return parseInt(project.id, 10);
}
export function initializeUrlState(_a) {
    var _b;
    var organization = _a.organization, queryParams = _a.queryParams, router = _a.router, memberProjects = _a.memberProjects, skipLoadLastUsed = _a.skipLoadLastUsed, shouldForceProject = _a.shouldForceProject, shouldEnforceSingleProject = _a.shouldEnforceSingleProject, defaultSelection = _a.defaultSelection, forceProject = _a.forceProject, _c = _a.showAbsolute, showAbsolute = _c === void 0 ? true : _c;
    var orgSlug = organization.slug;
    var query = pick(queryParams, [URL_PARAM.PROJECT, URL_PARAM.ENVIRONMENT]);
    var hasProjectOrEnvironmentInUrl = Object.keys(query).length > 0;
    var parsed = getStateFromQuery(queryParams, {
        allowAbsoluteDatetime: showAbsolute,
        allowEmptyPeriod: true,
    });
    var _d = getDefaultSelection(), defaultDateTime = _d.datetime, retrievedDefaultSelection = __rest(_d, ["datetime"]);
    var _e = defaultSelection || {}, customizedDefaultDateTime = _e.datetime, customizedDefaultSelection = __rest(_e, ["datetime"]);
    var globalSelection = __assign(__assign(__assign({}, retrievedDefaultSelection), customizedDefaultSelection), { datetime: (_b = {},
            _b[DATE_TIME.START] = parsed.start || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.start) || null,
            _b[DATE_TIME.END] = parsed.end || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.end) || null,
            _b[DATE_TIME.PERIOD] = parsed.period || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.period) || defaultDateTime.period,
            _b[DATE_TIME.UTC] = parsed.utc || (customizedDefaultDateTime === null || customizedDefaultDateTime === void 0 ? void 0 : customizedDefaultDateTime.utc) || null,
            _b) });
    if (globalSelection.datetime.start && globalSelection.datetime.end) {
        globalSelection.datetime.period = null;
    }
    // We only save environment and project, so if those exist in
    // URL, do not touch local storage
    if (hasProjectOrEnvironmentInUrl) {
        globalSelection.projects = parsed.project || [];
        globalSelection.environments = parsed.environment || [];
    }
    else if (!skipLoadLastUsed) {
        try {
            var localStorageKey = LOCAL_STORAGE_KEY + ":" + orgSlug;
            var storedValue = localStorage.getItem(localStorageKey);
            if (storedValue) {
                globalSelection = __assign({ datetime: globalSelection.datetime }, JSON.parse(storedValue));
            }
        }
        catch (err) {
            // use default if invalid
            Sentry.captureException(err);
            console.error(err); // eslint-disable-line no-console
        }
    }
    var projects = globalSelection.projects, environment = globalSelection.environments, datetime = globalSelection.datetime;
    var newProject = null;
    var project = projects;
    /**
     * Skip enforcing a single project if `shouldForceProject` is true,
     * since a component is controlling what that project needs to be.
     * This is true regardless if user has access to multi projects
     */
    if (shouldForceProject && forceProject) {
        newProject = [getProjectIdFromProject(forceProject)];
    }
    else if (shouldEnforceSingleProject && !shouldForceProject) {
        /**
         * If user does not have access to `global-views` (e.g. multi project select) *and* there is no
         * `project` URL parameter, then we update URL params with:
         * 1) the first project from the list of requested projects from URL params,
         * 2) first project user is a member of from org
         *
         * Note this is intentionally skipped if `shouldForceProject == true` since we want to initialize store
         * and wait for the forced project
         */
        if (projects && projects.length > 0) {
            // If there is a list of projects from URL params, select first project from that list
            newProject = typeof projects === 'string' ? [Number(projects)] : [projects[0]];
        }
        else {
            // When we have finished loading the organization into the props,  i.e. the organization slug is consistent with
            // the URL param--Sentry will get the first project from the organization that the user is a member of.
            newProject = __spread(memberProjects).slice(0, 1).map(getProjectIdFromProject);
        }
    }
    if (newProject) {
        globalSelection.projects = newProject;
        project = newProject;
    }
    GlobalSelectionActions.initializeUrlState(globalSelection);
    GlobalSelectionActions.setOrganization(organization);
    // To keep URLs clean, don't push default period if url params are empty
    var parsedWithNoDefaultPeriod = getStateFromQuery(queryParams, {
        allowEmptyPeriod: true,
        allowAbsoluteDatetime: showAbsolute,
    });
    var newDatetime = __assign(__assign({}, datetime), { period: !parsedWithNoDefaultPeriod.start &&
            !parsedWithNoDefaultPeriod.end &&
            !parsedWithNoDefaultPeriod.period
            ? null
            : datetime.period, utc: !parsedWithNoDefaultPeriod.utc ? null : datetime.utc });
    updateParamsWithoutHistory(__assign({ project: project, environment: environment }, newDatetime), router, {
        keepCursor: true,
    });
}
/**
 * Updates store and global project selection URL param if `router` is supplied
 *
 * This accepts `environments` from `options` to also update environments simultaneously
 * as environments are tied to a project, so if you change projects, you may need
 * to clear environments.
 */
export function updateProjects(projects, router, options) {
    if (!isProjectsValid(projects)) {
        Sentry.withScope(function (scope) {
            scope.setExtra('projects', projects);
            Sentry.captureException(new Error('Invalid projects selected'));
        });
        return;
    }
    GlobalSelectionActions.updateProjects(projects, options === null || options === void 0 ? void 0 : options.environments);
    updateParams({ project: projects, environment: options === null || options === void 0 ? void 0 : options.environments }, router, options);
}
function isProjectsValid(projects) {
    return Array.isArray(projects) && projects.every(function (project) { return isInteger(project); });
}
/**
 * Updates store and global datetime selection URL param if `router` is supplied
 *
 * @param {Object} datetime Object with start, end, range keys
 * @param {Object} [router] Router object
 * @param {Object} [options] Options object
 * @param {String[]} [options.resetParams] List of parameters to remove when changing URL params
 */
export function updateDateTime(datetime, router, options) {
    GlobalSelectionActions.updateDateTime(datetime);
    // We only save projects/environments to local storage, do not
    // save anything when date changes.
    updateParams(datetime, router, __assign(__assign({}, options), { save: false }));
}
/**
 * Updates store and updates global environment selection URL param if `router` is supplied
 *
 * @param {String[]} environments List of environments
 * @param {Object} [router] Router object
 * @param {Object} [options] Options object
 * @param {String[]} [options.resetParams] List of parameters to remove when changing URL params
 */
export function updateEnvironments(environment, router, options) {
    GlobalSelectionActions.updateEnvironments(environment);
    updateParams({ environment: environment }, router, options);
}
/**
 * Updates router/URL with new query params
 *
 * @param obj New query params
 * @param [router] React router object
 * @param [options] Options object
 */
export function updateParams(obj, router, options) {
    // Allow another component to handle routing
    if (!router) {
        return;
    }
    var newQuery = getNewQueryParams(obj, router.location.query, options);
    // Only push new location if query params has changed because this will cause a heavy re-render
    if (qs.stringify(newQuery) === qs.stringify(router.location.query)) {
        return;
    }
    if (options === null || options === void 0 ? void 0 : options.save) {
        GlobalSelectionActions.save(newQuery);
    }
    router.push({
        pathname: router.location.pathname,
        query: newQuery,
    });
}
/**
 * Like updateParams but just replaces the current URL and does not create a
 * new browser history entry
 *
 * @param obj New query params
 * @param [router] React router object
 * @param [options] Options object
 */
export function updateParamsWithoutHistory(obj, router, options) {
    // Allow another component to handle routing
    if (!router) {
        return;
    }
    var newQuery = getNewQueryParams(obj, router.location.query, options);
    // Only push new location if query params have changed because this will cause a heavy re-render
    if (qs.stringify(newQuery) === qs.stringify(router.location.query)) {
        return;
    }
    router.replace({
        pathname: router.location.pathname,
        query: newQuery,
    });
}
/**
 * Creates a new query parameter object given new params and old params
 * Preserves the old query params, except for `cursor` (can be overriden with keepCursor option)
 *
 * @param obj New query params
 * @param oldQueryParams Old query params
 * @param [options] Options object
 */
function getNewQueryParams(obj, oldQueryParams, _a) {
    var _b = _a === void 0 ? {} : _a, resetParams = _b.resetParams, keepCursor = _b.keepCursor;
    var cursor = oldQueryParams.cursor, statsPeriod = oldQueryParams.statsPeriod, oldQuery = __rest(oldQueryParams, ["cursor", "statsPeriod"]);
    var oldQueryWithoutResetParams = !!(resetParams === null || resetParams === void 0 ? void 0 : resetParams.length)
        ? omit(oldQuery, resetParams)
        : oldQuery;
    var newQuery = getParams(__assign(__assign(__assign({}, oldQueryWithoutResetParams), { 
        // Some views update using `period`, and some `statsPeriod`, we should make this uniform
        period: !obj.start && !obj.end ? obj.period || statsPeriod : null }), obj));
    if (newQuery.start) {
        newQuery.start = getUtcDateString(newQuery.start);
    }
    if (newQuery.end) {
        newQuery.end = getUtcDateString(newQuery.end);
    }
    if (keepCursor) {
        newQuery.cursor = cursor;
    }
    return newQuery;
}
function getParams(params) {
    var start = params.start, end = params.end, period = params.period, statsPeriod = params.statsPeriod, otherParams = __rest(params, ["start", "end", "period", "statsPeriod"]);
    // `statsPeriod` takes precedence for now
    var coercedPeriod = statsPeriod || period;
    // Filter null values
    return Object.fromEntries(Object.entries(__assign({ statsPeriod: coercedPeriod, start: coercedPeriod ? null : start, end: coercedPeriod ? null : end }, otherParams)).filter(function (_a) {
        var _b = __read(_a, 2), value = _b[1];
        return defined(value);
    }));
}
//# sourceMappingURL=globalSelection.jsx.map