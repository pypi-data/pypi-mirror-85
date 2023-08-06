import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import DropdownMenu from 'app/components/dropdownMenu';
import { IconAdd, IconChevron } from 'app/icons';
import withOrganizations from 'app/utils/withOrganizations';
import SidebarOrgSummary from 'app/components/sidebar/sidebarOrgSummary';
import SidebarMenuItem from 'app/components/sidebar/sidebarMenuItem';
import SidebarDropdownMenu from 'app/components/sidebar/sidebarDropdownMenu.styled';
import space from 'app/styles/space';
import Divider from './divider.styled';
/**
 * Switch Organization Menu Label + Sub Menu
 */
var SwitchOrganization = function (_a) {
    var organizations = _a.organizations, canCreateOrganization = _a.canCreateOrganization;
    return (<DropdownMenu isNestedDropdown>
    {function (_a) {
        var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
        return (<React.Fragment>
        <SwitchOrganizationMenuActor data-test-id="sidebar-switch-org" {...getActorProps({})} onClick={function (e) {
            // This overwrites `DropdownMenu.getActorProps.onClick` which normally handles clicks on actor
            // to toggle visibility of menu. Instead, do nothing because it is nested and we only want it
            // to appear when hovered on. Will also stop menu from closing when clicked on (which seems to be common
            // behavior);
            // Stop propagation so that dropdown menu doesn't close here
            e.stopPropagation();
        }}>
          {t('Switch organization')}

          <SubMenuCaret>
            <IconChevron size="xs" direction="right"/>
          </SubMenuCaret>
        </SwitchOrganizationMenuActor>

        {isOpen && (<SwitchOrganizationMenu data-test-id="sidebar-switch-org-menu" {...getMenuProps({})}>
            <OrganizationList>
              {organizations.map(function (organization) {
            var url = "/organizations/" + organization.slug + "/";
            return (<SidebarMenuItem key={organization.slug} to={url}>
                    <SidebarOrgSummary organization={organization}/>
                  </SidebarMenuItem>);
        })}
            </OrganizationList>
            {organizations && !!organizations.length && canCreateOrganization && (<Divider css={{ marginTop: 0 }}/>)}
            {canCreateOrganization && (<SidebarMenuItem data-test-id="sidebar-create-org" to="/organizations/new/" style={{ alignItems: 'center' }}>
                <MenuItemLabelWithIcon>
                  <StyledIconAdd />
                  <span>{t('Create a new organization')}</span>
                </MenuItemLabelWithIcon>
              </SidebarMenuItem>)}
          </SwitchOrganizationMenu>)}
      </React.Fragment>);
    }}
  </DropdownMenu>);
};
var SwitchOrganizationContainer = withOrganizations(SwitchOrganization);
export { SwitchOrganization };
export default SwitchOrganizationContainer;
var StyledIconAdd = styled(IconAdd)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n  color: ", ";\n"], ["\n  margin-right: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme.gray300; });
var MenuItemLabelWithIcon = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  line-height: 1;\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  line-height: 1;\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"])), space(1));
var SubMenuCaret = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
// Menu Item in dropdown to "Switch organization"
var SwitchOrganizationMenuActor = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 -", ";\n  padding: 0 ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 -", ";\n  padding: 0 ", ";\n"])), function (p) { return p.theme.sidebar.menuSpacing; }, function (p) { return p.theme.sidebar.menuSpacing; });
var SwitchOrganizationMenu = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n  top: 0;\n  left: 256px;\n"], ["\n  ", ";\n  top: 0;\n  left: 256px;\n"])), SidebarDropdownMenu);
var OrganizationList = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-height: 350px;\n  overflow-y: auto;\n"], ["\n  max-height: 350px;\n  overflow-y: auto;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=switchOrganization.jsx.map