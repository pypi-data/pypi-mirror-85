import { __read, __spread } from "tslib";
var TYPES = {
    STRING: 'string',
    NUMBER: 'number',
    BOOLEAN: 'boolean',
    DATETIME: 'datetime',
};
export var PROMOTED_TAGS = [
    'level',
    'logger',
    'server.name',
    'transaction',
    'environment',
    'site',
    'url',
    'app.device',
    'device',
    'device.family',
    'runtime',
    'runtime.name',
    'browser',
    'browser.name',
    'os',
    'os.name',
    'os.rooted',
];
// All tags are assumed to be strings, except the following
export var SPECIAL_TAGS = {
    os_rooted: TYPES.DATETIME,
};
// Hide the following tags if they are returned from Snuba since these are
// already mapped to user and release attributes
export var HIDDEN_TAGS = ['sentry:user', 'sentry:release'];
export var COLUMNS = [
    { name: 'id', type: TYPES.STRING },
    { name: 'event.type', type: TYPES.STRING },
    { name: 'issue.id', type: TYPES.NUMBER },
    { name: 'project.id', type: TYPES.STRING },
    { name: 'project.name', type: TYPES.STRING },
    { name: 'platform', type: TYPES.STRING },
    { name: 'message', type: TYPES.STRING },
    { name: 'title', type: TYPES.STRING },
    { name: 'location', type: TYPES.STRING },
    { name: 'timestamp', type: TYPES.DATETIME },
    { name: 'release', type: TYPES.STRING },
    { name: 'user.id', type: TYPES.STRING },
    { name: 'user.username', type: TYPES.STRING },
    { name: 'user.email', type: TYPES.STRING },
    { name: 'user.ip', type: TYPES.STRING },
    { name: 'sdk.name', type: TYPES.STRING },
    { name: 'sdk.version', type: TYPES.STRING },
    // {name: 'tags_key', type: TYPES.STRING},
    // {name: 'tags_value', type: TYPES.STRING},
    { name: 'contexts.key', type: TYPES.STRING },
    { name: 'contexts.value', type: TYPES.STRING },
    { name: 'http.method', type: TYPES.STRING },
    { name: 'http.referer', type: TYPES.STRING },
    { name: 'http.url', type: TYPES.STRING },
    { name: 'os.build', type: TYPES.STRING },
    { name: 'os.kernel_version', type: TYPES.STRING },
    { name: 'device.name', type: TYPES.STRING },
    { name: 'device.brand', type: TYPES.STRING },
    { name: 'device.locale', type: TYPES.STRING },
    { name: 'device.uuid', type: TYPES.STRING },
    { name: 'device.model_id', type: TYPES.STRING },
    { name: 'device.arch', type: TYPES.STRING },
    { name: 'device.battery_level', type: TYPES.NUMBER },
    { name: 'device.orientation', type: TYPES.STRING },
    { name: 'device.simulator', type: TYPES.BOOLEAN },
    { name: 'device.online', type: TYPES.BOOLEAN },
    { name: 'device.charging', type: TYPES.BOOLEAN },
    { name: 'geo.country_code', type: TYPES.STRING },
    { name: 'geo.region', type: TYPES.STRING },
    { name: 'geo.city', type: TYPES.STRING },
    { name: 'error.type', type: TYPES.STRING },
    { name: 'error.value', type: TYPES.STRING },
    { name: 'error.mechanism', type: TYPES.STRING },
    { name: 'error.handled', type: TYPES.BOOLEAN },
    { name: 'stack.abs_path', type: TYPES.STRING },
    { name: 'stack.filename', type: TYPES.STRING },
    { name: 'stack.package', type: TYPES.STRING },
    { name: 'stack.module', type: TYPES.STRING },
    { name: 'stack.function', type: TYPES.STRING },
    { name: 'stack.in_app', type: TYPES.BOOLEAN },
    { name: 'stack.colno', type: TYPES.NUMBER },
    { name: 'stack.lineno', type: TYPES.NUMBER },
    { name: 'stack.stack_level', type: TYPES.NUMBER },
];
export var NON_SNUBA_FIELDS = ['project.name', 'issue'];
export var NON_CONDITIONS_FIELDS = __spread(NON_SNUBA_FIELDS, ['project.id']);
export var OPERATOR = {
    GREATER_THAN: '>',
    LESS_THAN: '<',
    GREATER_THAN_OR_EQUAL: '>=',
    LESS_THAN_OR_EQUAL: '<=',
    EQUAL: '=',
    NOT_EQUAL: '!=',
    IS_NULL: 'IS NULL',
    IS_NOT_NULL: 'IS NOT NULL',
    LIKE: 'LIKE',
    NOT_LIKE: 'NOT LIKE',
};
export var CONDITION_OPERATORS = Object.values(OPERATOR);
export var NEGATION_OPERATORS = [
    OPERATOR.IS_NOT_NULL,
    OPERATOR.NOT_EQUAL,
    OPERATOR.NOT_LIKE,
];
export var NULL_OPERATORS = [OPERATOR.IS_NOT_NULL, OPERATOR.IS_NULL];
export var WILDCARD_OPERATORS = [OPERATOR.LIKE, OPERATOR.NOT_LIKE];
export var ARRAY_FIELD_PREFIXES = ['error', 'stack'];
export var NUMBER_OF_SERIES_BY_DAY = 10;
//# sourceMappingURL=data.jsx.map