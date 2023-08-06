import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import ContextPickerModalContainer from 'app/components/contextPickerModal';
var PickProjectToContinue = function (_a) {
    var orgSlug = _a.orgSlug, version = _a.version, router = _a.router, projects = _a.projects;
    var navigating = false;
    var path = "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(version) + "/?project=";
    // if the project in URL is missing, but this release belongs to only one project, redirect there
    if (projects.length === 1) {
        router.replace(path + projects[0].id);
        return null;
    }
    openModal(function (modalProps) { return (<ContextPickerModalContainer {...modalProps} needOrg={false} needProject nextPath={path + ":project"} onFinish={function (pathname) {
        navigating = true;
        router.replace(pathname);
    }} projectSlugs={projects.map(function (p) { return p.slug; })}/>); }, {
        onClose: function () {
            // we want this to be executed only if the user didn't select any project
            // (closed modal either via button, Esc, clicking outside, ...)
            if (!navigating) {
                router.push("/organizations/" + orgSlug + "/releases/");
            }
        },
    });
    return <ContextPickerBackground />;
};
var ContextPickerBackground = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 100vh;\n  width: 100%;\n"], ["\n  height: 100vh;\n  width: 100%;\n"])));
export default PickProjectToContinue;
var templateObject_1;
//# sourceMappingURL=pickProjectToContinue.jsx.map