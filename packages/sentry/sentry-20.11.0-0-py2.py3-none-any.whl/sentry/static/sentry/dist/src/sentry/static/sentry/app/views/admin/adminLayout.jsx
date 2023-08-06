import { __makeTemplateObject } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import styled from '@emotion/styled';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
import space from 'app/styles/space';
var AdminLayout = function (_a) {
    var children = _a.children;
    return (<DocumentTitle title="Sentry Admin">
    <Page>
      <NavWrapper>
        <SettingsNavigation stickyTop="0" navigationObjects={[
        {
            name: 'System Status',
            items: [
                { path: '/manage/', index: true, title: 'Overview' },
                { path: '/manage/buffer/', title: 'Buffer' },
                { path: '/manage/queue/', title: 'Queue' },
                { path: '/manage/quotas/', title: 'Quotas' },
                { path: '/manage/status/environment/', title: 'Environment' },
                { path: '/manage/status/packages/', title: 'Packages' },
                { path: '/manage/status/mail/', title: 'Mail' },
                { path: '/manage/status/warnings/', title: 'Warnings' },
                { path: '/manage/settings/', title: 'Settings' },
            ],
        },
        {
            name: 'Manage',
            items: [
                { path: '/manage/organizations/', title: 'Organizations' },
                { path: '/manage/projects/', title: 'Projects' },
                { path: '/manage/users/', title: 'Users' },
            ],
        },
    ]}/>
      </NavWrapper>
      <Content>{children}</Content>
    </Page>
  </DocumentTitle>);
};
var NavWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-shrink: 0;\n  flex-grow: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n"], ["\n  flex-shrink: 0;\n  flex-grow: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n"])), function (p) { return p.theme.settings.sidebarWidth; }, function (p) { return p.theme.white; }, function (p) { return p.theme.border; });
var Page = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"], ["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"])));
var Content = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  padding: ", ";\n"], ["\n  flex-grow: 1;\n  padding: ", ";\n"])), space(4));
export default AdminLayout;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=adminLayout.jsx.map