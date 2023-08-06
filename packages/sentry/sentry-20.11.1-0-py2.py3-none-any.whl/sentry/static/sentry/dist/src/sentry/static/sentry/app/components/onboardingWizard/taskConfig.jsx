import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import { sourceMaps } from 'app/data/platformCategories';
import { OnboardingTaskKey, } from 'app/types';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
import EventWaiter from 'app/utils/eventWaiter';
import { taskIsDone } from 'app/components/onboardingWizard/utils';
import pulsingIndicatorStyles from 'app/styles/pulsingIndicator';
import space from 'app/styles/space';
function hasPlatformWithSourceMaps(organization) {
    var projects = organization === null || organization === void 0 ? void 0 : organization.projects;
    if (!projects) {
        return false;
    }
    return projects.some(function (_a) {
        var platform = _a.platform;
        return platform && sourceMaps.includes(platform);
    });
}
export function getOnboardingTasks(organization) {
    return [
        {
            task: OnboardingTaskKey.FIRST_PROJECT,
            title: t('Create a project'),
            description: t('Create your first Sentry project'),
            detailedDescription: t('Follow our quick and easy steps to set up a project and start sending errors.'),
            skippable: false,
            requisites: [],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: OnboardingTaskKey.FIRST_EVENT,
            title: t('Send your first event'),
            description: t('Install the appropriate Sentry SDK for your application'),
            detailedDescription: t('Choose your platform and send an event.'),
            skippable: false,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/install/",
            display: true,
            SupplementComponent: withProjects(withApi(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<EventWaiter api={api} organization={organization} project={projects[0]} eventType="error" onIssueReceived={function () { return !taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </EventWaiter>) : null;
            })),
        },
        {
            task: OnboardingTaskKey.INVITE_MEMBER,
            title: t('Invite team members'),
            description: t('Bring your team aboard'),
            detailedDescription: t("Let Sentry help your team triage and assign issues. Improve your workflow\n        by unlocking mentions, assignment, and suggested issue owners."),
            skippable: true,
            requisites: [],
            actionType: 'action',
            action: function () { return openInviteMembersModal({ source: 'onboarding_widget' }); },
            display: true,
        },
        {
            task: OnboardingTaskKey.SECOND_PLATFORM,
            title: t('Add a second platform'),
            description: t('Add Sentry to a second platform'),
            detailedDescription: t('Capture errors from both your front and back ends.'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: OnboardingTaskKey.FIRST_TRANSACTION,
            title: t('Monitor Performance'),
            description: t('See slow faster'),
            detailedDescription: t("Set up Performance Monitoring to see everything from macro-level metrics to micro-level spans.\n        Cross-reference transactions with related issues, customize queries, and monitor mission-critical endpoints using metric alerts."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/performance/getting-started/',
            display: true,
            SupplementComponent: withProjects(withApi(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<EventWaiter api={api} organization={organization} project={projects[0]} eventType="transaction" onIssueReceived={function () { return !taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </EventWaiter>) : null;
            })),
        },
        {
            task: OnboardingTaskKey.USER_CONTEXT,
            title: t('Add user context'),
            description: t('Know who is being affected by crashes'),
            detailedDescription: t("Unlock features that let you drill down into the number of users affected by an issue\n        and get a broader sense about the quality of your application."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/enriching-error-data/context/#capturing-the-user',
            display: true,
        },
        {
            task: OnboardingTaskKey.RELEASE_TRACKING,
            title: t('Set up release tracking'),
            description: t('See which releases cause errors'),
            detailedDescription: t("Set up releases and associate commits to gain additional context when determining the\n        cause of an issue and unlock the ability to resolve issues via commit message."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/release-tracking/",
            display: true,
        },
        {
            task: OnboardingTaskKey.SOURCEMAPS,
            title: t('Upload source maps'),
            description: t('Deminify JavaScript stack traces'),
            detailedDescription: t("View source code context obtained from stack traces in its\n        original untransformed form, which is particularly useful for debugging minified code."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/platforms/javascript/sourcemaps/',
            display: hasPlatformWithSourceMaps(organization),
        },
        {
            task: OnboardingTaskKey.USER_REPORTS,
            title: 'User crash reports',
            description: t('Collect user feedback when your application crashes'),
            skippable: true,
            requisites: [
                OnboardingTaskKey.FIRST_PROJECT,
                OnboardingTaskKey.FIRST_EVENT,
                OnboardingTaskKey.USER_CONTEXT,
            ],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/user-reports/",
            display: false,
        },
        {
            task: OnboardingTaskKey.ISSUE_TRACKER,
            title: t('Set up issue tracking'),
            description: t('Link to Sentry issues within your issue tracker'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/plugins/",
            display: false,
        },
        {
            task: OnboardingTaskKey.ALERT_RULE,
            title: t('Configure alerting rules'),
            description: t('Configure alerting rules to control error emails'),
            detailedDescription: t('Receive Sentry alerts in Slack, PagerDuty, and more.'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/alerts/",
            display: true,
        },
    ];
}
export function getMergedTasks(organization) {
    var taskDescriptors = getOnboardingTasks(organization);
    var serverTasks = organization.onboardingTasks;
    // Map server task state (i.e. completed status) with tasks objects
    var allTasks = taskDescriptors.map(function (desc) {
        return (__assign(__assign(__assign({}, desc), serverTasks.find(function (serverTask) { return serverTask.task === desc.task; })), { requisiteTasks: [] }));
    });
    // Map incomplete requisiteTasks as full task objects
    return allTasks.map(function (task) { return (__assign(__assign({}, task), { requisiteTasks: task.requisites
            .map(function (key) { return allTasks.find(function (task2) { return task2.task === key; }); })
            .filter(function (reqTask) { return reqTask.status !== 'complete'; }) })); });
}
var PulsingIndicator = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), pulsingIndicatorStyles);
var EventWaitingIndicator = styled(function (p) { return (<div {...p}>
    {t('Waiting for first event')}
    <PulsingIndicator />
  </div>); })(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  line-height: 1rem;\n"], ["\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  line-height: 1rem;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.textColor; }, space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=taskConfig.jsx.map