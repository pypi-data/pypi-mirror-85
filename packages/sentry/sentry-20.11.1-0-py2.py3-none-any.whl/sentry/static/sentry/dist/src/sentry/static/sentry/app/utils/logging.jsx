import * as Sentry from '@sentry/react';
export function logException(ex, context) {
    Sentry.withScope(function (scope) {
        if (context) {
            scope.setExtra('context', context);
        }
        Sentry.captureException(ex);
    });
    /*eslint no-console:0*/
    window.console && console.error && console.error(ex);
}
//# sourceMappingURL=logging.jsx.map