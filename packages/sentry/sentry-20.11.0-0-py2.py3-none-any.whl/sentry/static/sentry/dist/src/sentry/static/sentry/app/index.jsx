import { __awaiter, __generator } from "tslib";
// These imports (core-js and regenerator-runtime) are replacements for deprecated `@babel/polyfill`
import 'core-js/stable';
import 'regenerator-runtime/runtime';
var BOOTSTRAP_URL = '/api/client-config/';
var bootApplication = function (data) {
    var distPrefix = data.distPrefix, csrfCookieName = data.csrfCookieName, sentryConfig = data.sentryConfig, userIdentity = data.userIdentity;
    // TODO(epurkhiser): Would be great if we could remove some of these from
    // existing on the window object and instead pass into a bootstrap function.
    // We can't currently do this due to some of these globals needing to be
    // available for modules imported by the bootstrap.
    window.csrfCookieName = csrfCookieName;
    window.__sentryGlobalStaticPrefix = distPrefix;
    window.__SENTRY__OPTIONS = sentryConfig;
    window.__SENTRY__USER = userIdentity;
    window.__initialData = data;
    // Once data hydration is done we can initialize the app
    require('./bootstrap');
};
function bootWithHydration() {
    return __awaiter(this, void 0, void 0, function () {
        var response, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(BOOTSTRAP_URL)];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    // XXX(epurkhiser): Currently we only boot with hydration in experimental SPA
                    // mode, where assets are *currently not versioned*. We hardcode this here
                    // for now as a quick workaround for the index.html being aware of versioned
                    // asset paths.
                    data.distPrefix = '/_assets/';
                    bootApplication(data);
                    // TODO(epurkhiser): This should live somewhere else
                    $(window.SentryRenderApp);
                    return [2 /*return*/];
            }
        });
    });
}
var bootstrapData = window.__initialData;
// If __initialData is not already set on the window, we are likely running in
// pure SPA mode, meaning django is not serving our frontend application and we
// need to make an API request to hydrate the bootstrap data to boot the app.
if (bootstrapData === undefined) {
    bootWithHydration();
}
else {
    bootApplication(bootstrapData);
}
//# sourceMappingURL=index.jsx.map