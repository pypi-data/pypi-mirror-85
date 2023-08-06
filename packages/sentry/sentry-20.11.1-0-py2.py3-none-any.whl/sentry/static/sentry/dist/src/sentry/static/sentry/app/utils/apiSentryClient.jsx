import * as Sentry from '@sentry/react';
var hub;
function init(dsn) {
    // This client is used to track all API requests that use `app/api`
    // This is a bit noisy so we don't want it in the main project (yet)
    var client = new Sentry.BrowserClient({
        dsn: dsn,
    });
    hub = new Sentry.Hub(client);
}
var run = function (cb) {
    if (!hub) {
        return;
    }
    hub.run(cb);
};
export { init, run };
//# sourceMappingURL=apiSentryClient.jsx.map