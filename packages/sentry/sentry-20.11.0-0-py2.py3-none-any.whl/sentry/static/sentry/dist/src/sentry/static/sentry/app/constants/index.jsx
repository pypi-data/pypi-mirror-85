/* global process */
/**
 * Common constants here
 */
var _a;
import { t } from 'app/locale';
// This is considered the "default" route/view that users should be taken
// to when the application does not have any further context
//
// e.g. loading app root or switching organization
export var DEFAULT_APP_ROUTE = '/organizations/:orgSlug/issues/';
export var API_ACCESS_SCOPES = [
    'project:read',
    'project:write',
    'project:admin',
    'project:releases',
    'team:read',
    'team:write',
    'team:admin',
    'event:read',
    'event:write',
    'event:admin',
    'org:read',
    'org:write',
    'org:admin',
    'org:integrations',
    'member:read',
    'member:write',
    'member:admin',
];
// Default API scopes when adding a new API token or org API token
export var DEFAULT_API_ACCESS_SCOPES = [
    'event:read',
    'event:admin',
    'project:read',
    'project:releases',
    'org:read',
    'team:read',
    'member:read',
];
// These should only be used in the case where we cannot obtain roles through
// the members endpoint (primarily in cases where a user is admining a
// different organization they are not a OrganizationMember of ).
export var MEMBER_ROLES = [
    {
        id: 'member',
        name: 'Member',
        allowed: true,
        desc: 'Members can view and act on events, as well as view most other data within the organization.',
    },
    {
        id: 'admin',
        name: 'Admin',
        allowed: true,
        desc: "Admin privileges on any teams of which they're a member. They can create new teams and projects, as well as remove teams and projects which they already hold membership on (or all teams, if open membership is on).",
    },
    {
        id: 'manager',
        name: 'Manager',
        allowed: true,
        desc: 'Gains admin access on all teams as well as the ability to add and remove members.',
    },
    {
        id: 'owner',
        name: 'Organization Owner',
        allowed: true,
        desc: 'Unrestricted access to the organization, its data, and its settings. Can add, modify, and delete projects and members, as well as make billing and plan changes.',
    },
];
// We expose permissions for Sentry Apps in a more resource-centric way.
// All of the API_ACCESS_SCOPES from above should be represented in a more
// User-friendly way here.
export var SENTRY_APP_PERMISSIONS = [
    {
        resource: 'Project',
        help: 'Projects, Tags, Debug Files, and Feedback',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['project:read'] },
            write: { label: 'Read & Write', scopes: ['project:read', 'project:write'] },
            admin: { label: 'Admin', scopes: ['project:read', 'project:write', 'project:admin'] },
        },
    },
    {
        resource: 'Team',
        help: 'Teams of members',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['team:read'] },
            write: { label: 'Read & Write', scopes: ['team:read', 'team:write'] },
            admin: { label: 'Admin', scopes: ['team:read', 'team:write', 'team:admin'] },
        },
    },
    {
        resource: 'Release',
        help: 'Releases, Commits, and related Files',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            admin: { label: 'Admin', scopes: ['project:releases'] },
        },
    },
    {
        resource: 'Event',
        label: 'Issue & Event',
        help: 'Issues, Events, and workflow statuses',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['event:read'] },
            write: { label: 'Read & Write', scopes: ['event:read', 'event:write'] },
            admin: { label: 'Admin', scopes: ['event:read', 'event:write', 'event:admin'] },
        },
    },
    {
        resource: 'Organization',
        help: 'Manage Organizations, resolve IDs, retrieve Repositories and Commits',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['org:read'] },
            write: { label: 'Read & Write', scopes: ['org:read', 'org:write'] },
            admin: { label: 'Admin', scopes: ['org:read', 'org:write', 'org:admin'] },
        },
    },
    {
        resource: 'Member',
        help: 'Manage Members within Teams',
        choices: {
            'no-access': { label: 'No Access', scopes: [] },
            read: { label: 'Read', scopes: ['member:read'] },
            write: { label: 'Read & Write', scopes: ['member:read', 'member:write'] },
            admin: { label: 'Admin', scopes: ['member:read', 'member:write', 'member:admin'] },
        },
    },
];
export var DEFAULT_TOAST_DURATION = 6000;
export var DEFAULT_DEBOUNCE_DURATION = 300;
export var CSRF_COOKIE_NAME = (_a = window.csrfCookieName) !== null && _a !== void 0 ? _a : 'sc';
export var ALL_ENVIRONMENTS_KEY = '__all_environments__';
// See http://fusejs.io/ for more information
export var DEFAULT_FUSE_OPTIONS = {
    includeScore: true,
    includeMatches: true,
    threshold: 0.4,
    location: 0,
    distance: 75,
    maxPatternLength: 24,
    minMatchCharLength: 2,
};
// Maps a `type: string` -> `url-prefix: string`
export var AVATAR_URL_MAP = {
    team: 'team-avatar',
    organization: 'organization-avatar',
    project: 'project-avatar',
    user: 'avatar',
};
export var MENU_CLOSE_DELAY = 200;
export var MAX_PICKABLE_DAYS = 90;
export var DEFAULT_STATS_PERIOD = '14d';
export var DEFAULT_QUERY = 'is:unresolved';
export var DEFAULT_USE_UTC = true;
export var DEFAULT_RELATIVE_PERIODS = {
    '1h': t('Last hour'),
    '24h': t('Last 24 hours'),
    '7d': t('Last 7 days'),
    '14d': t('Last 14 days'),
    '30d': t('Last 30 days'),
    '90d': t('Last 90 days'),
};
// Special Search characters
export var NEGATION_OPERATOR = '!';
export var SEARCH_WILDCARD = '*';
// SmartSearchBar settings
export var MAX_AUTOCOMPLETE_RECENT_SEARCHES = 3;
export var MAX_AUTOCOMPLETE_RELEASES = 5;
export var DEFAULT_PER_PAGE = 50;
export var TEAMS_PER_PAGE = 25;
// Webpack configures DEPLOY_PREVIEW_CONFIG for deploy preview builds.
export var DEPLOY_PREVIEW_CONFIG = process.env.DEPLOY_PREVIEW_CONFIG;
// Webpack configures EXPERIMENTAL_SPA.
export var EXPERIMENTAL_SPA = process.env.EXPERIMENTAL_SPA;
// so we don't use filtered values in certain display contexts
// TODO(kmclb): once relay is doing the scrubbing, the masking value will be dynamic,
// so this will have to change
export var FILTER_MASK = '[Filtered]';
// Errors that may occur during the fetching of organization details
export var ORGANIZATION_FETCH_ERROR_TYPES = {
    ORG_NOT_FOUND: 'ORG_NOT_FOUND',
};
export var CONFIG_DOCS_URL = 'https://docs.sentry.io/server/config/';
export var DISCOVER2_DOCS_URL = 'https://docs.sentry.io/product/discover-queries/';
export var IS_ACCEPTANCE_TEST = !!process.env.IS_ACCEPTANCE_TEST;
export var NODE_ENV = process.env.NODE_ENV;
export var DISABLE_RR_WEB = !!process.env.DISABLE_RR_WEB;
export var SPA_DSN = process.env.SPA_DSN;
export var DEFAULT_ERROR_JSON = {
    detail: t('Unknown error. Please try again.'),
};
//# sourceMappingURL=index.jsx.map