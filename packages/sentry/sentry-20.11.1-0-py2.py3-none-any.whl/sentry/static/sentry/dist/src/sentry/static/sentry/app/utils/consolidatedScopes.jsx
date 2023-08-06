import { __assign, __read, __spread } from "tslib";
import invertBy from 'lodash/invertBy';
import groupBy from 'lodash/groupBy';
import pick from 'lodash/pick';
var PERMISSION_LEVELS = {
    read: 0,
    write: 1,
    admin: 2,
};
var HUMAN_RESOURCE_NAMES = {
    project: 'Project',
    team: 'Team',
    release: 'Release',
    event: 'Event',
    org: 'Organization',
    member: 'Member',
};
var DEFAULT_RESOURCE_PERMISSIONS = {
    Project: 'no-access',
    Team: 'no-access',
    Release: 'no-access',
    Event: 'no-access',
    Organization: 'no-access',
    Member: 'no-access',
};
var PROJECT_RELEASES = 'project:releases';
/**
 * Numerical value of the scope where Admin is higher than Write,
 * which is higher than Read. Used to sort scopes by access.
 */
var permissionLevel = function (scope) {
    var permission = scope.split(':')[1];
    return PERMISSION_LEVELS[permission];
};
var compareScopes = function (a, b) { return permissionLevel(a) - permissionLevel(b); };
/**
 * Return the most permissive scope for each resource.
 *
 * Example:
 *    Given the full list of scopes:
 *      ['project:read', 'project:write', 'team:read', 'team:write', 'team:admin']
 *
 *    this would return:
 *      ['project:write', 'team:admin']
 */
function topScopes(scopeList) {
    return Object.values(groupBy(scopeList, function (scope) { return scope.split(':')[0]; }))
        .map(function (scopes) { return scopes.sort(compareScopes); })
        .map(function (scopes) { return scopes.pop(); });
}
/**
 * Convert into a list of Permissions, grouped by resource.
 *
 * This is used in the new/edit Sentry App form. That page displays permissions
 * in a per-Resource manner, meaning one row for Project, one for Organization, etc.
 *
 * This exposes scopes in a way that works for that UI.
 *
 * Example:
 *    {
 *      'Project': 'read',
 *      'Organization': 'write',
 *      'Team': 'no-access',
 *      ...
 *    }
 */
function toResourcePermissions(scopes) {
    var permissions = __assign({}, DEFAULT_RESOURCE_PERMISSIONS);
    var filteredScopes = __spread(scopes);
    // The scope for releases is `project:releases`, but instead of displaying
    // it as a permission of Project, we want to separate it out into its own
    // row for Releases.
    if (scopes.includes(PROJECT_RELEASES)) {
        permissions.Release = 'admin';
        filteredScopes = scopes.filter(function (scope) { return scope !== PROJECT_RELEASES; }); // remove project:releases
    }
    topScopes(filteredScopes).forEach(function (scope) {
        if (scope) {
            var _a = __read(scope.split(':'), 2), resource = _a[0], permission = _a[1];
            permissions[HUMAN_RESOURCE_NAMES[resource]] = permission;
        }
    });
    return permissions;
}
/**
 * Convert into a list of Permissions, grouped by access and including a
 * list of resources per access level.
 *
 * This is used in the Permissions Modal when installing an App. It displays
 * scopes in a per-Permission way, meaning one row for Read, one for Write,
 * and one for Admin.
 *
 * This exposes scopes in a way that works for that UI.
 *
 * Example:
 *    {
 *      read:  ['Project', 'Organization'],
 *      write: ['Member'],
 *      admin: ['Release']
 *    }
 */
function toPermissions(scopes) {
    var defaultPermissions = { read: [], write: [], admin: [] };
    var resourcePermissions = toResourcePermissions(scopes);
    // Filter out the 'no-access' permissions
    var permissions = pick(invertBy(resourcePermissions), ['read', 'write', 'admin']);
    return __assign(__assign({}, defaultPermissions), permissions);
}
export { toPermissions, toResourcePermissions };
//# sourceMappingURL=consolidatedScopes.jsx.map