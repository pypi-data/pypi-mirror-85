import * as Sentry from '@sentry/react';
import localStorage from 'app/utils/localStorage';
var ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY = 'advanced-data-scrubbing';
// TODO(Priscila): add the method below in app/utils
function fetchFromStorage() {
    var storage = localStorage.getItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY);
    if (!storage) {
        return undefined;
    }
    try {
        return JSON.parse(storage);
    }
    catch (err) {
        Sentry.withScope(function (scope) {
            scope.setExtra('storage', storage);
            Sentry.captureException(err);
        });
        return undefined;
    }
}
function saveToStorage(obj) {
    try {
        localStorage.setItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY, JSON.stringify(obj));
    }
    catch (err) {
        Sentry.captureException(err);
        Sentry.withScope(function (scope) {
            scope.setExtra('storage', obj);
            Sentry.captureException(err);
        });
    }
}
export { fetchFromStorage, saveToStorage };
//# sourceMappingURL=localStorage.jsx.map