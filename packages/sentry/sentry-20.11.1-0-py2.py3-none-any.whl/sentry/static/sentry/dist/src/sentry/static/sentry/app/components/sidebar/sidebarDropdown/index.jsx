import { __awaiter, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { logout } from 'app/actionCreators/account';
import { t } from 'app/locale';
import { IconChevron, IconSentry } from 'app/icons';
import Avatar from 'app/components/avatar';
import ConfigStore from 'app/stores/configStore';
import DropdownMenu from 'app/components/dropdownMenu';
import Hook from 'app/components/hook';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import SidebarDropdownMenu from 'app/components/sidebar/sidebarDropdownMenu.styled';
import SidebarMenuItem, { menuItemStyles } from 'app/components/sidebar/sidebarMenuItem';
import SidebarOrgSummary from 'app/components/sidebar/sidebarOrgSummary';
import TextOverflow from 'app/components/textOverflow';
import withApi from 'app/utils/withApi';
import space from 'app/styles/space';
import SwitchOrganization from './switchOrganization';
import Divider from './divider.styled';
var SidebarDropdown = function (_a) {
    var _b, _c, _d;
    var api = _a.api, org = _a.org, orientation = _a.orientation, collapsed = _a.collapsed, config = _a.config, user = _a.user;
    var handleLogout = function () { return __awaiter(void 0, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, logout(api)];
                case 1:
                    _a.sent();
                    window.location.assign('/auth/login/');
                    return [2 /*return*/];
            }
        });
    }); };
    var hasOrganization = !!org;
    var hasUser = !!user;
    // It's possible we do not have an org in context (e.g. RouteNotFound)
    // Otherwise, we should have the full org
    var hasOrgRead = (_b = org === null || org === void 0 ? void 0 : org.access) === null || _b === void 0 ? void 0 : _b.includes('org:read');
    var hasMemberRead = (_c = org === null || org === void 0 ? void 0 : org.access) === null || _c === void 0 ? void 0 : _c.includes('member:read');
    var hasTeamRead = (_d = org === null || org === void 0 ? void 0 : org.access) === null || _d === void 0 ? void 0 : _d.includes('team:read');
    var canCreateOrg = ConfigStore.get('features').has('organizations:create');
    // Avatar to use: Organization --> user --> Sentry
    var avatar = hasOrganization || hasUser ? (<StyledAvatar collapsed={collapsed} organization={org} user={!org ? user : undefined} size={32} round={false}/>) : (<SentryLink to="/">
        <IconSentry size="32px"/>
      </SentryLink>);
    return (<DropdownMenu>
      {function (_a) {
        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
        return (<SidebarDropdownRoot {...getRootProps()}>
          <SidebarDropdownActor type="button" data-test-id="sidebar-dropdown" {...getActorProps({})}>
            {avatar}
            {!collapsed && orientation !== 'top' && (<OrgAndUserWrapper>
                <OrgOrUserName>
                  {hasOrganization ? org.name : user.name}{' '}
                  <StyledIconChevron color="white" size="xs" direction="down"/>
                </OrgOrUserName>
                <UserNameOrEmail>
                  {hasOrganization ? user.name : user.email}
                </UserNameOrEmail>
              </OrgAndUserWrapper>)}
          </SidebarDropdownActor>

          {isOpen && (<OrgAndUserMenu {...getMenuProps({})}>
              {hasOrganization && (<React.Fragment>
                  <SidebarOrgSummary organization={org}/>
                  {hasOrgRead && (<SidebarMenuItem to={"/settings/" + org.slug + "/"}>
                      {t('Organization settings')}
                    </SidebarMenuItem>)}
                  {hasMemberRead && (<SidebarMenuItem to={"/settings/" + org.slug + "/members/"}>
                      {t('Members')}
                    </SidebarMenuItem>)}

                  {hasTeamRead && (<SidebarMenuItem to={"/settings/" + org.slug + "/teams/"}>
                      {t('Teams')}
                    </SidebarMenuItem>)}

                  <Hook name="sidebar:organization-dropdown-menu" organization={org}/>

                  {!config.singleOrganization && (<SidebarMenuItem>
                      <SwitchOrganization canCreateOrganization={canCreateOrg}/>
                    </SidebarMenuItem>)}

                  <Divider />
                </React.Fragment>)}

              {!!user && (<React.Fragment>
                  <UserSummary to="/settings/account/details/">
                    <UserBadgeNoOverflow user={user} avatarSize={32}/>
                  </UserSummary>

                  <div>
                    <SidebarMenuItem to="/settings/account/">
                      {t('User settings')}
                    </SidebarMenuItem>
                    <SidebarMenuItem to="/settings/account/api/">
                      {t('API keys')}
                    </SidebarMenuItem>
                    {user.isSuperuser && (<SidebarMenuItem to="/manage/">{t('Admin')}</SidebarMenuItem>)}
                    <SidebarMenuItem data-test-id="sidebarSignout" onClick={handleLogout}>
                      {t('Sign out')}
                    </SidebarMenuItem>
                  </div>
                </React.Fragment>)}
            </OrgAndUserMenu>)}
        </SidebarDropdownRoot>);
    }}
    </DropdownMenu>);
};
export default withApi(SidebarDropdown);
var SentryLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.white; });
var UserSummary = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n  padding: 10px 15px;\n"], ["\n  ", "\n  padding: 10px 15px;\n"])), menuItemStyles);
var UserBadgeNoOverflow = styled(IdBadge)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var SidebarDropdownRoot = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
// So that long org names and user names do not overflow
var OrgAndUserWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  text-align: left;\n"], ["\n  overflow: hidden;\n  text-align: left;\n"])));
var OrgOrUserName = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: bold;\n  color: ", ";\n  text-shadow: 0 0 6px rgba(255, 255, 255, 0);\n  transition: 0.15s text-shadow linear;\n"], ["\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: bold;\n  color: ", ";\n  text-shadow: 0 0 6px rgba(255, 255, 255, 0);\n  transition: 0.15s text-shadow linear;\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.white; });
var UserNameOrEmail = styled(TextOverflow)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 16px;\n  transition: 0.15s color linear;\n"], ["\n  font-size: ", ";\n  line-height: 16px;\n  transition: 0.15s color linear;\n"])), function (p) { return p.theme.fontSizeMedium; });
var SidebarDropdownActor = styled('button')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  cursor: pointer;\n  border: none;\n  padding: 0;\n  background: none;\n  width: 100%;\n\n  &:hover {\n    ", " {\n      text-shadow: 0 0 6px rgba(255, 255, 255, 0.1);\n    }\n    ", " {\n      color: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  cursor: pointer;\n  border: none;\n  padding: 0;\n  background: none;\n  width: 100%;\n\n  &:hover {\n    ", " {\n      text-shadow: 0 0 6px rgba(255, 255, 255, 0.1);\n    }\n    ", " {\n      color: ", ";\n    }\n  }\n"])), OrgOrUserName, UserNameOrEmail, function (p) { return p.theme.gray200; });
var StyledAvatar = styled(Avatar)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: ", " 0;\n  margin-right: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08);\n  border-radius: 6px; /* Fixes background bleeding on corners */\n"], ["\n  margin: ", " 0;\n  margin-right: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08);\n  border-radius: 6px; /* Fixes background bleeding on corners */\n"])), space(0.25), function (p) { return (p.collapsed ? '0' : space(1.5)); });
var OrgAndUserMenu = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", ";\n  top: 42px;\n  min-width: 180px;\n  z-index: ", ";\n"], ["\n  ", ";\n  top: 42px;\n  min-width: 180px;\n  z-index: ", ";\n"])), SidebarDropdownMenu, function (p) { return p.theme.zIndex.orgAndUserMenu; });
var StyledIconChevron = styled(IconChevron)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=index.jsx.map