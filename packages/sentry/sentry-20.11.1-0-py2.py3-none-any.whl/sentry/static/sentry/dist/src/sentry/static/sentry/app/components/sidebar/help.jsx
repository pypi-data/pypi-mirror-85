import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openHelpSearchModal } from 'app/actionCreators/modal';
import { t } from 'app/locale';
import DropdownMenu from 'app/components/dropdownMenu';
import SidebarItem from 'app/components/sidebar/sidebarItem';
import Hook from 'app/components/hook';
import { IconQuestion } from 'app/icons';
import SidebarMenuItem from './sidebarMenuItem';
import SidebarDropdownMenu from './sidebarDropdownMenu.styled';
var SidebarHelp = function (_a) {
    var orientation = _a.orientation, collapsed = _a.collapsed, hidePanel = _a.hidePanel, organization = _a.organization;
    return (<DropdownMenu>
    {function (_a) {
        var isOpen = _a.isOpen, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
        return (<HelpRoot>
        <HelpActor {...getActorProps({ onClick: hidePanel })}>
          <SidebarItem orientation={orientation} collapsed={collapsed} hasPanel={false} icon={<IconQuestion size="md"/>} label={t('Help')} id="help"/>
        </HelpActor>

        {isOpen && (<HelpMenu {...getMenuProps({})}>
            <Hook name="sidebar:help-menu" organization={organization}/>
            <SidebarMenuItem onClick={function () { return openHelpSearchModal({ organization: organization }); }}>
              {t('Search Docs and FAQs')}
            </SidebarMenuItem>
            <SidebarMenuItem href="https://forum.sentry.io/">
              {t('Community Discussions')}
            </SidebarMenuItem>
            <SidebarMenuItem href="https://status.sentry.io/">
              {t('Service Status')}
            </SidebarMenuItem>
          </HelpMenu>)}
      </HelpRoot>);
    }}
  </DropdownMenu>);
};
export default SidebarHelp;
var HelpRoot = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
// This exists to provide a styled actor for the dropdown. Making the actor a regular,
// non-styled react component causes some issues with toggling correctly because of
// how refs are handled.
var HelpActor = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var HelpMenu = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  bottom: 100%;\n"], ["\n  ", ";\n  bottom: 100%;\n"])), SidebarDropdownMenu);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=help.jsx.map