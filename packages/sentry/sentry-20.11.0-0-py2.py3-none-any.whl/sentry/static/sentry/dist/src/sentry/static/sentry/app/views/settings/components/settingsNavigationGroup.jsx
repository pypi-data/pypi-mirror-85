import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import SettingsNavItem from 'app/views/settings/components/settingsNavItem';
import replaceRouterParams from 'app/utils/replaceRouterParams';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var SettingsNavigationGroup = function (props) {
    var organization = props.organization, project = props.project, name = props.name, items = props.items;
    return (<NavSection data-test-id={name}>
      <SettingsHeading>{name}</SettingsHeading>
      {items.map(function (_a) {
        var path = _a.path, title = _a.title, index = _a.index, show = _a.show, badge = _a.badge, id = _a.id, recordAnalytics = _a.recordAnalytics;
        if (typeof show === 'function' && !show(props)) {
            return null;
        }
        if (typeof show !== 'undefined' && !show) {
            return null;
        }
        var badgeResult = typeof badge === 'function' ? badge(props) : null;
        var to = replaceRouterParams(path, __assign(__assign({}, (organization ? { orgId: organization.slug } : {})), (project ? { projectId: project.slug } : {})));
        var handleClick = function () {
            //only call the analytics event if the URL is changing
            if (recordAnalytics && to !== window.location.pathname) {
                trackAnalyticsEvent({
                    organization_id: organization && organization.id,
                    project_id: project && project.id,
                    eventName: 'Sidebar Item Clicked',
                    eventKey: 'sidebar.item_clicked',
                    sidebar_item_id: id,
                    dest: path,
                });
            }
        };
        return (<SettingsNavItem key={title} to={to} label={title} index={index} badge={badgeResult} id={id} onClick={handleClick}/>);
    })}
    </NavSection>);
};
var NavSection = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var SettingsHeading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: 12px;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: 20px;\n"], ["\n  color: ", ";\n  font-size: 12px;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: 20px;\n"])), function (p) { return p.theme.subText; });
export default SettingsNavigationGroup;
var templateObject_1, templateObject_2;
//# sourceMappingURL=settingsNavigationGroup.jsx.map