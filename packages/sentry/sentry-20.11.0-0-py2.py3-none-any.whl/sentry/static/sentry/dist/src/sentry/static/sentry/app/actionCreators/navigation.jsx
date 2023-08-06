import React from 'react';
import { openModal } from 'app/actionCreators/modal';
import ContextPickerModal from 'app/components/contextPickerModal';
import NavigationActions from 'app/actions/navigationActions';
// TODO(ts): figure out better typing for react-router here
export function navigateTo(to, router) {
    var _a, _b;
    // Check for placeholder params
    var needOrg = to.indexOf(':orgId') > -1;
    var needProject = to.indexOf(':projectId') > -1;
    var comingFromProjectId = (_b = (_a = router === null || router === void 0 ? void 0 : router.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.project;
    if (needOrg || needProject) {
        openModal(function (modalProps) { return (<ContextPickerModal {...modalProps} nextPath={to} needOrg={needOrg} needProject={needProject} comingFromProjectId={Array.isArray(comingFromProjectId) ? '' : comingFromProjectId || ''} onFinish={function (path) {
            modalProps.closeModal();
            setTimeout(function () { return router.push(path); }, 0);
        }}/>); }, {});
    }
    else {
        router.push(to);
    }
}
export function setLastRoute(route) {
    NavigationActions.setLastRoute(route);
}
//# sourceMappingURL=navigation.jsx.map