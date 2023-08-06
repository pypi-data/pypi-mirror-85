var DEFAULT_EMPTY_ROUTING_NAME = 'none';
var DEFAULT_EMPTY_ENV_NAME = '(No Environment)';
export function getUrlRoutingName(env) {
    if (env.name) {
        return encodeURIComponent(env.name);
    }
    if (env.displayName) {
        return encodeURIComponent(env.displayName);
    }
    return DEFAULT_EMPTY_ROUTING_NAME;
}
export function getDisplayName(env) {
    return env.name || env.displayName || DEFAULT_EMPTY_ENV_NAME;
}
//# sourceMappingURL=environment.jsx.map