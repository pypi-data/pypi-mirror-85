import { __assign } from "tslib";
import * as Sentry from '@sentry/react';
import HookStore from 'app/stores/hookStore';
/**
 * Analytics and metric tracking functionality.
 *
 * These are primarily driven through hooks provided through the hookstore. For
 * sentry.io these are currently mapped to our in-house analytics backend
 * 'Reload' and the Amplitude service.
 *
 * NOTE: sentry.io contributors, you will need to nesure that the eventKey
 *       passed exists as an event key in the Reload events.py configuration:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/events.py
 *
 * NOTE: sentry.io contributors, if you are using `gauge` or `increment` the
 *       name must be added to the Reload metrics module:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/metrics/__init__.py
 */
/**
 * This should be primarily used for product events. In that case where you
 * want to track some one-off Adhoc events, use the `trackAdhocEvent` function.
 *
 * Generally this is the function you will want to use for event tracking.
 *
 * Refer for the backend implementation provided through HookStore for more
 * details.
 */
export var trackAnalyticsEvent = function (options) {
    return HookStore.get('analytics:track-event').forEach(function (cb) { return cb(options); });
};
/**
 * This should be used for adhoc analytics tracking.
 *
 * This is used for high volume events, and events with unbounded parameters,
 * such as tracking search queries.
 *
 * Refer for the backend implementation provided through HookStore for a more
 * thorough explanation of when to use this.
 */
export var trackAdhocEvent = function (options) {
    return HookStore.get('analytics:track-adhoc-event').forEach(function (cb) { return cb(options); });
};
/**
 * This should be used to log when a `organization.experiments` experiment
 * variant is checked in the application.
 *
 * Refer for the backend implementation provided through HookStore for more
 * details.
 */
export var logExperiment = function (options) {
    return HookStore.get('analytics:log-experiment').forEach(function (cb) { return cb(options); });
};
/**
 * Helper function for `trackAnalyticsEvent` to generically track usage of deprecated features
 *
 * @param feature A name to identify the feature you are tracking
 * @param orgId The organization id
 * @param url [optional] The URL
 */
export var trackDeprecated = function (feature, orgId, url) {
    if (url === void 0) { url = ''; }
    return trackAdhocEvent({
        eventKey: 'deprecated.feature',
        feature: feature,
        url: url,
        org_id: orgId && Number(orgId),
    });
};
/**
 * Legacy analytics tracking.
 *
 * @deprecated Prefer `trackAnalyticsEvent` and `trackAdhocEvent`.
 */
export var analytics = function (name, data) {
    return HookStore.get('analytics:event').forEach(function (cb) { return cb(name, data); });
};
/**
 * Used to pass data between metric.mark() and metric.measure()
 */
var metricDataStore = new Map();
/**
 * Record metrics.
 */
export var metric = function (name, value, tags) {
    return HookStore.get('metrics:event').forEach(function (cb) { return cb(name, value, tags); });
};
// JSDOM implements window.performance but not window.performance.mark
var CAN_MARK = window.performance &&
    typeof window.performance.mark === 'function' &&
    typeof window.performance.measure === 'function' &&
    typeof window.performance.getEntriesByName === 'function' &&
    typeof window.performance.clearMeasures === 'function';
metric.mark = function metricMark(_a) {
    var name = _a.name, _b = _a.data, data = _b === void 0 ? {} : _b;
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name) {
        throw new Error('Invalid argument provided to `metric.mark`');
    }
    window.performance.mark(name);
    metricDataStore.set(name, data);
};
/**
 * Performs a measurement between `start` and `end` (or now if `end` is not
 * specified) Calls `metric` with `name` and the measured time difference.
 */
metric.measure = function metricMeasure(_a) {
    var _b = _a === void 0 ? {} : _a, name = _b.name, start = _b.start, end = _b.end, _c = _b.data, data = _c === void 0 ? {} : _c, noCleanup = _b.noCleanup;
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name || !start) {
        throw new Error('Invalid arguments provided to `metric.measure`');
    }
    var endMarkName = end;
    // Can't destructure from performance
    var performance = window.performance;
    // NOTE: Edge REQUIRES an end mark if it is given a start mark
    // If we don't have an end mark, create one now.
    if (!end) {
        endMarkName = start + "-end";
        performance.mark(endMarkName);
    }
    // Check if starting mark exists
    if (!performance.getEntriesByName(start, 'mark').length) {
        return;
    }
    performance.measure(name, start, endMarkName);
    var startData = metricDataStore.get(start) || {};
    // Retrieve measurement entries
    performance
        .getEntriesByName(name, 'measure')
        .forEach(function (measurement) {
        return metric(measurement.name, measurement.duration, __assign(__assign({}, startData), data));
    });
    // By default, clean up measurements
    if (!noCleanup) {
        performance.clearMeasures(name);
        performance.clearMarks(start);
        performance.clearMarks(endMarkName);
        metricDataStore.delete(start);
    }
};
/**
 * Used to pass data between startTransaction and endTransaction
 */
var transactionDataStore = new Map();
var getCurrentTransaction = function () {
    var _a;
    return (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
};
metric.startTransaction = function (_a) {
    var _b;
    var name = _a.name, traceId = _a.traceId, op = _a.op;
    if (!traceId) {
        traceId = (_b = getCurrentTransaction()) === null || _b === void 0 ? void 0 : _b.traceId;
    }
    var transaction = Sentry.startTransaction({ name: name, op: op, traceId: traceId });
    transactionDataStore[name] = transaction;
};
metric.endTransaction = function (_a) {
    var name = _a.name;
    var transaction = transactionDataStore[name];
    if (transaction) {
        transaction.finish();
    }
};
//# sourceMappingURL=analytics.jsx.map