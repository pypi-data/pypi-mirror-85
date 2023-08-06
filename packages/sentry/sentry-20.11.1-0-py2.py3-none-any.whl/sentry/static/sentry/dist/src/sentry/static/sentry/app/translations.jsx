import { __read } from "tslib";
import * as Sentry from '@sentry/react';
// zh-cn => zh_CN
function convertToDjangoLocaleFormat(language) {
    var _a = __read(language.split('-'), 2), left = _a[0], right = _a[1];
    return left + (right ? '_' + right.toUpperCase() : '');
}
export function getTranslations(language) {
    language = convertToDjangoLocaleFormat(language);
    try {
        return require("sentry-locale/" + language + "/LC_MESSAGES/django.po");
    }
    catch (e) {
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['sentry-locale-not-found']);
            scope.setExtra('locale', language);
            Sentry.captureException(e);
        });
        // Default locale if not found
        return require('sentry-locale/en/LC_MESSAGES/django.po');
    }
}
//# sourceMappingURL=translations.jsx.map