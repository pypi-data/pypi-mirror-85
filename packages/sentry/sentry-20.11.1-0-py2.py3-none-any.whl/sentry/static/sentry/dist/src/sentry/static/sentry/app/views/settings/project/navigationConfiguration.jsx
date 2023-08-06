import { __read, __spread } from "tslib";
import { t } from 'app/locale';
var pathPrefix = '/settings/:orgId/projects/:projectId';
export default function getConfiguration(_a) {
    var project = _a.project, organization = _a.organization;
    var plugins = ((project && project.plugins) || []).filter(function (plugin) { return plugin.enabled; });
    return [
        {
            name: t('Project'),
            items: [
                {
                    path: pathPrefix + "/",
                    index: true,
                    title: t('General Settings'),
                    description: t('Configure general settings for a project'),
                },
                {
                    path: pathPrefix + "/teams/",
                    title: t('Project Teams'),
                    description: t('Manage team access for a project'),
                },
                {
                    path: pathPrefix + "/alerts/",
                    title: t('Alerts'),
                    description: t('Manage alert rules for a project'),
                },
                {
                    path: pathPrefix + "/tags/",
                    title: t('Tags'),
                    description: t("View and manage a  project's tags"),
                },
                {
                    path: pathPrefix + "/environments/",
                    title: t('Environments'),
                    description: t('Manage environments in a project'),
                },
                {
                    path: pathPrefix + "/ownership/",
                    title: t('Issue Owners'),
                    description: t('Manage issue ownership rules for a project'),
                },
                {
                    path: pathPrefix + "/data-forwarding/",
                    title: t('Data Forwarding'),
                },
            ],
        },
        {
            name: t('Processing'),
            items: [
                {
                    path: pathPrefix + "/filters/",
                    title: t('Inbound Filters'),
                    description: t("Configure a project's inbound filters (e.g. browsers, messages)"),
                },
                {
                    path: pathPrefix + "/security-and-privacy/",
                    title: t('Security & Privacy'),
                    description: t('Configuration related to dealing with sensitive data and other security settings. (Data Scrubbing, Data Privacy, Data Scrubbing) for a project'),
                },
                {
                    path: pathPrefix + "/issue-grouping/",
                    title: t('Issue Grouping'),
                },
                {
                    path: pathPrefix + "/processing-issues/",
                    title: t('Processing Issues'),
                    // eslint-disable-next-line no-shadow
                    badge: function (_a) {
                        var project = _a.project;
                        if (!project) {
                            return null;
                        }
                        if (project.processingIssues <= 0) {
                            return null;
                        }
                        return project.processingIssues > 99 ? '99+' : project.processingIssues;
                    },
                },
                {
                    path: pathPrefix + "/debug-symbols/",
                    title: t('Debug Files'),
                },
                {
                    path: pathPrefix + "/source-maps/",
                    title: t('Source Maps'),
                },
                {
                    path: pathPrefix + "/proguard/",
                    title: t('ProGuard'),
                    show: function () { var _a; return !!((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('android-mappings')); },
                },
            ],
        },
        {
            name: t('SDK Setup'),
            items: [
                {
                    path: pathPrefix + "/install/",
                    title: t('Instrumentation'),
                },
                {
                    path: pathPrefix + "/keys/",
                    title: t('Client Keys (DSN)'),
                    description: t("View and manage the project's client keys (DSN)"),
                },
                {
                    path: pathPrefix + "/release-tracking/",
                    title: t('Releases'),
                },
                {
                    path: pathPrefix + "/security-headers/",
                    title: t('Security Headers'),
                },
                {
                    path: pathPrefix + "/user-feedback/",
                    title: t('User Feedback'),
                    description: t('Configure user feedback reporting feature'),
                },
            ],
        },
        {
            name: t('Legacy Integrations'),
            items: __spread([
                {
                    path: pathPrefix + "/plugins/",
                    title: t('Legacy Integrations'),
                    description: t('View, enable, and disable all integrations for a project'),
                    id: 'legacy_integrations',
                    recordAnalytics: true,
                }
            ], plugins.map(function (plugin) { return ({
                path: pathPrefix + "/plugins/" + plugin.id + "/",
                title: plugin.name,
                show: function (opts) { var _a; return (_a = opts === null || opts === void 0 ? void 0 : opts.access) === null || _a === void 0 ? void 0 : _a.has('project:write'); },
                id: 'plugin_details',
                recordAnalytics: true,
            }); })),
        },
    ];
}
//# sourceMappingURL=navigationConfiguration.jsx.map