import { __assign, __read, __spread } from "tslib";
import capitalize from 'lodash/capitalize';
import React from 'react';
import * as qs from 'query-string';
import HookStore from 'app/stores/hookStore';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { uniqueId } from 'app/utils/guid';
import { IconBitbucket, IconGeneric, IconGithub, IconGitlab, IconJira, IconVsts, } from 'app/icons';
var INTEGRATIONS_ANALYTICS_SESSION_KEY = 'INTEGRATION_ANALYTICS_SESSION';
var FEATURES_TO_INCLUDE_IN_ANALYTICS = ['slack-migration'];
export var startAnalyticsSession = function () {
    var sessionId = uniqueId();
    window.sessionStorage.setItem(INTEGRATIONS_ANALYTICS_SESSION_KEY, sessionId);
    return sessionId;
};
export var clearAnalyticsSession = function () {
    window.sessionStorage.removeItem(INTEGRATIONS_ANALYTICS_SESSION_KEY);
};
export var getAnalyticsSessionId = function () {
    return window.sessionStorage.getItem(INTEGRATIONS_ANALYTICS_SESSION_KEY);
};
var hasAnalyticsDebug = function () {
    return window.localStorage.getItem('DEBUG_INTEGRATION_ANALYTICS') === '1';
};
/**
 * Tracks an event for ecosystem analytics
 * Must be tied to an organization
 * Uses the current session ID or generates a new one if startSession == true
 */
export var trackIntegrationEvent = function (analyticsParams, org, //we should pass in org whenever we can but not every place guarantees this
options) {
    var startSession = (options || {}).startSession;
    var sessionId = startSession ? startAnalyticsSession() : getAnalyticsSessionId();
    //we should always have a session id but if we don't, we should generate one
    if (hasAnalyticsDebug() && !sessionId) {
        // eslint-disable-next-line no-console
        console.warn("analytics_session_id absent from event " + analyticsParams.eventName);
        sessionId = startAnalyticsSession();
    }
    var features = {};
    if (org) {
        features = Object.fromEntries(FEATURES_TO_INCLUDE_IN_ANALYTICS.map(function (f) { return [
            "feature-" + f,
            org.features.includes(f),
        ]; }));
    }
    var custom_referrer;
    try {
        //pull the referrer from the query parameter of the page
        var referrer = (qs.parse(window.location.search) || {}).referrer;
        if (typeof referrer === 'string') {
            // Amplitude has its own referrer which inteferes with our custom referrer
            custom_referrer = referrer;
        }
    }
    catch (_a) {
        // ignore if this fails to parse
        // this can happen if we have an invalid query string
        // e.g. unencoded "%"
    }
    var params = __assign(__assign({ analytics_session_id: sessionId, organization_id: org === null || org === void 0 ? void 0 : org.id, role: org === null || org === void 0 ? void 0 : org.role, custom_referrer: custom_referrer }, features), analyticsParams);
    //add the integration_status to the type of params so TS doesn't complain about what we do below
    var fullParams = params;
    //Reload expects integration_status even though it's not relevant for non-sentry apps
    //Passing in a dummy value of published in those cases
    if (analyticsParams.integration && analyticsParams.integration_type !== 'sentry_app') {
        fullParams.integration_status = 'published';
    }
    //TODO(steve): remove once we pass in org always
    if (hasAnalyticsDebug() && !org) {
        // eslint-disable-next-line no-console
        console.warn("Organization absent from event " + analyticsParams.eventName);
    }
    //could put this into a debug method or for the main trackAnalyticsEvent event
    if (hasAnalyticsDebug()) {
        // eslint-disable-next-line no-console
        console.log('trackIntegrationEvent', fullParams);
    }
    return trackAnalyticsEvent(fullParams);
};
/**
 * In sentry.io the features list supports rendering plan details. If the hook
 * is not registered for rendering the features list like this simply show the
 * features as a normal list.
 */
var generateFeaturesList = function (p) { return (<ul>
    {p.features.map(function (f, i) { return (<li key={i}>{f.description}</li>); })}
  </ul>); };
var generateIntegrationFeatures = function (p) {
    return p.children({
        disabled: false,
        disabledReason: null,
        ungatedFeatures: p.features,
        gatedFeatureGroups: [],
    });
};
var defaultFeatureGateComponents = {
    IntegrationFeatures: generateIntegrationFeatures,
    IntegrationDirectoryFeatures: generateIntegrationFeatures,
    FeatureList: generateFeaturesList,
    IntegrationDirectoryFeatureList: generateFeaturesList,
};
export var getIntegrationFeatureGate = function () {
    var defaultHook = function () { return defaultFeatureGateComponents; };
    var featureHook = HookStore.get('integrations:feature-gates')[0] || defaultHook;
    return featureHook();
};
export var getSentryAppInstallStatus = function (install) {
    if (install) {
        return capitalize(install.status);
    }
    return 'Not Installed';
};
export var getCategories = function (features) {
    var transform = features.map(function (_a) {
        var featureGate = _a.featureGate;
        var feature = featureGate
            .replace(/integrations/g, '')
            .replace(/-/g, ' ')
            .trim();
        switch (feature) {
            case 'actionable notification':
                return 'notification action';
            case 'issue basic':
            case 'issue link':
            case 'issue sync':
                return 'project management';
            case 'commits':
                return 'source code management';
            case 'chat unfurl':
                return 'chat';
            default:
                return feature;
        }
    });
    return __spread(new Set(transform));
};
export var getCategoriesForIntegration = function (integration) {
    if (isSentryApp(integration)) {
        return ['internal', 'unpublished'].includes(integration.status)
            ? [integration.status]
            : getCategories(integration.featureData);
    }
    if (isPlugin(integration)) {
        return getCategories(integration.featureDescriptions);
    }
    if (isDocumentIntegration(integration)) {
        return getCategories(integration.features);
    }
    return getCategories(integration.metadata.features);
};
export function isSentryApp(integration) {
    return !!integration.uuid;
}
export function isPlugin(integration) {
    return integration.hasOwnProperty('shortName');
}
export function isDocumentIntegration(integration) {
    return integration.hasOwnProperty('docUrl');
}
export function isSlackWorkspaceApp(integration) {
    return integration.configData.installationType === 'workspace_app';
}
//returns the text in the alert asking the user to re-authenticate a first-party integration
export function getReauthAlertText(provider) {
    var _a, _b;
    return (_b = (_a = provider.metadata.aspects) === null || _a === void 0 ? void 0 : _a.reauthentication_alert) === null || _b === void 0 ? void 0 : _b.alertText;
}
export var convertIntegrationTypeToSnakeCase = function (type) {
    switch (type) {
        case 'firstParty':
            return 'first_party';
        case 'sentryApp':
            return 'sentry_app';
        case 'documentIntegration':
            return 'document';
        default:
            return type;
    }
};
export var safeGetQsParam = function (param) {
    try {
        var query = qs.parse(window.location.search) || {};
        return query[param];
    }
    catch (_a) {
        return undefined;
    }
};
export var getIntegrationIcon = function (integrationType) {
    switch (integrationType) {
        case 'bitbucket':
            return <IconBitbucket size="md"/>;
        case 'gitlab':
            return <IconGitlab size="md"/>;
        case 'github':
        case 'github_enterprise':
            return <IconGithub size="md"/>;
        case 'jira':
        case 'jira_server':
            return <IconJira size="md"/>;
        case 'vsts':
            return <IconVsts size="md"/>;
        default:
            return <IconGeneric size="md"/>;
    }
};
//# sourceMappingURL=integrationUtil.jsx.map