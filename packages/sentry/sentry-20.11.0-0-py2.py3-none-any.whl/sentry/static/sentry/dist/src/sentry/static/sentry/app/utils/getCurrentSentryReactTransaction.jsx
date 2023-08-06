import * as Sentry from '@sentry/react';
/**
 * Gets the current transaction, if one exists.
 */
export default function getCurrentSentryReactTransaction() {
    var _a, _b;
    return (_b = (_a = Sentry === null || Sentry === void 0 ? void 0 : Sentry.getCurrentHub()) === null || _a === void 0 ? void 0 : _a.getScope()) === null || _b === void 0 ? void 0 : _b.getTransaction();
}
//# sourceMappingURL=getCurrentSentryReactTransaction.jsx.map