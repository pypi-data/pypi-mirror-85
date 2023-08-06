import { Client } from 'app/api';
import ConfigStore from 'app/stores/configStore';
import GuideActions from 'app/actions/guideActions';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var api = new Client();
export function fetchGuides() {
    api.request('/assistant/?v2', {
        method: 'GET',
        success: function (data) {
            GuideActions.fetchSucceeded(data);
        },
    });
}
export function registerAnchor(target) {
    GuideActions.registerAnchor(target);
}
export function unregisterAnchor(target) {
    GuideActions.unregisterAnchor(target);
}
export function nextStep() {
    GuideActions.nextStep();
}
export function closeGuide() {
    GuideActions.closeGuide();
}
export function dismissGuide(guide, step, orgId) {
    recordDismiss(guide, step, orgId);
    closeGuide();
}
export function recordFinish(guide, orgId) {
    api.request('/assistant/', {
        method: 'PUT',
        data: {
            guide: guide,
            status: 'viewed',
        },
    });
    var user = ConfigStore.get('user');
    if (!user) {
        return;
    }
    var data = {
        eventKey: 'assistant.guide_finished',
        eventName: 'Assistant Guide Finished',
        guide: guide,
        organization_id: orgId,
        user_id: parseInt(user.id, 10),
    };
    trackAnalyticsEvent(data);
}
export function recordDismiss(guide, step, orgId) {
    api.request('/assistant/', {
        method: 'PUT',
        data: {
            guide: guide,
            status: 'dismissed',
        },
    });
    var user = ConfigStore.get('user');
    if (!user) {
        return;
    }
    var data = {
        eventKey: 'assistant.guide_dismissed',
        eventName: 'Assistant Guide Dismissed',
        guide: guide,
        step: step,
        organization_id: orgId,
        user_id: parseInt(user.id, 10),
    };
    trackAnalyticsEvent(data);
}
//# sourceMappingURL=guides.jsx.map