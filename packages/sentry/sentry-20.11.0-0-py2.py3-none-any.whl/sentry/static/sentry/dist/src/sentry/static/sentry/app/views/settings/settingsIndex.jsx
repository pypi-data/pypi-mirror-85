import { __extends, __makeTemplateObject, __rest } from "tslib";
import DocumentTitle from 'react-document-title';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import omit from 'lodash/omit';
import { t } from 'app/locale';
import OrganizationAvatar from 'app/components/avatar/organizationAvatar';
import UserAvatar from 'app/components/avatar/userAvatar';
import ConfigStore from 'app/stores/configStore';
import ExternalLink from 'app/components/links/externalLink';
import { fetchOrganizationDetails } from 'app/actionCreators/organizations';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { IconDocs, IconLock, IconStack, IconSupport } from 'app/icons';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import SentryTypes from 'app/sentryTypes';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
import withLatestContext from 'app/utils/withLatestContext';
var LINKS = {
    DOCUMENTATION: 'https://docs.sentry.io/',
    DOCUMENTATION_PLATFORMS: 'https://docs.sentry.io/clients/',
    DOCUMENATATION_QUICKSTART: 'https://docs.sentry.io/error-reporting/quickstart/',
    DOCUMENTATION_CLI: 'https://docs.sentry.io/cli/',
    DOCUMENTATION_API: 'https://docs.sentry.io/api/',
    API: '/settings/account/api/',
    MANAGE: '/manage/',
    FORUM: 'https://forum.sentry.io/',
    GITHUB_ISSUES: 'https://github.com/getsentry/sentry/issues',
    SERVICE_STATUS: 'https://status.sentry.io/',
};
var HOME_ICON_SIZE = 56;
var flexCenter = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var SettingsIndex = /** @class */ (function (_super) {
    __extends(SettingsIndex, _super);
    function SettingsIndex() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsIndex.prototype.componentDidUpdate = function (prevProps) {
        var organization = this.props.organization;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            fetchOrganizationDetails(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    };
    SettingsIndex.prototype.render = function () {
        var organization = this.props.organization;
        var user = ConfigStore.get('user');
        var isOnPremise = ConfigStore.get('isOnPremise');
        var organizationSettingsUrl = (organization && "/settings/" + organization.slug + "/") || '';
        var supportLinkProps = {
            isOnPremise: isOnPremise,
            href: LINKS.FORUM,
            to: organizationSettingsUrl + "support",
        };
        var supportText = isOnPremise ? t('Community Forums') : t('Contact Support');
        return (<DocumentTitle title={organization ? organization.slug + " Settings" : 'Settings'}>
        <SettingsLayout {...this.props}>
          <GridLayout>
            <GridPanel>
              <HomePanelHeader>
                <HomeLinkIcon to="/settings/account/">
                  <AvatarContainer>
                    <UserAvatar user={user} size={HOME_ICON_SIZE}/>
                  </AvatarContainer>
                  {t('My Account')}
                </HomeLinkIcon>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{t('Quick links')}:</h3>
                <ul>
                  <li>
                    <HomeLink to="/settings/account/security/">
                      {t('Change my password')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to="/settings/account/notifications/">
                      {t('Notification Preferences')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to="/settings/account/">{t('Change my avatar')}</HomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            
            <GridPanel>
              {!organization && <LoadingIndicator overlay hideSpinner/>}
              <HomePanelHeader>
                <HomeLinkIcon to={organizationSettingsUrl}>
                  {organization ? (<AvatarContainer>
                      <OrganizationAvatar organization={organization} size={HOME_ICON_SIZE}/>
                    </AvatarContainer>) : (<HomeIcon color="green300">
                      <IconStack size="lg"/>
                    </HomeIcon>)}
                  <OrganizationName>
                    {organization ? organization.slug : t('No Organization')}
                  </OrganizationName>
                </HomeLinkIcon>
              </HomePanelHeader>
              <HomePanelBody>
                <h3>{t('Quick links')}:</h3>
                <ul>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "projects/"}>
                      {t('Projects')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "teams/"}>
                      {t('Teams')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "members/"}>
                      {t('Members')}
                    </HomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <ExternalHomeLink isCentered href={LINKS.DOCUMENTATION}>
                  <HomeIcon color="orange400">
                    <IconDocs size="lg"/>
                  </HomeIcon>
                </ExternalHomeLink>
                <ExternalHomeLink href={LINKS.DOCUMENTATION}>
                  {t('Documentation')}
                </ExternalHomeLink>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{t('Quick links')}:</h3>
                <ul>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENATATION_QUICKSTART}>
                      {t('Quickstart Guide')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_PLATFORMS}>
                      {t('Platforms & Frameworks')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_CLI}>
                      {t('Sentry CLI')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <SupportLinkComponent isCentered {...supportLinkProps}>
                  <HomeIcon color="purple300">
                    <IconSupport size="lg"/>
                  </HomeIcon>
                  {t('Support')}
                </SupportLinkComponent>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{t('Quick links')}:</h3>
                <ul>
                  <li>
                    <SupportLinkComponent {...supportLinkProps}>
                      {supportText}
                    </SupportLinkComponent>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.GITHUB_ISSUES}>
                      {t('Sentry on GitHub')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.SERVICE_STATUS}>
                      {t('Service Status')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <HomeLinkIcon to={LINKS.API}>
                  <HomeIcon>
                    <IconLock size="lg"/>
                  </HomeIcon>
                  {t('API Keys')}
                </HomeLinkIcon>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{t('Quick links')}:</h3>
                <ul>
                  <li>
                    <HomeLink to={LINKS.API}>{t('Auth Tokens')}</HomeLink>
                  </li>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "developer-settings/"}>
                      {t('Your Integrations')}
                    </HomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_API}>
                      {t('Documentation')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>
          </GridLayout>
        </SettingsLayout>
      </DocumentTitle>);
    };
    SettingsIndex.propTypes = {
        organization: SentryTypes.Organization,
    };
    return SettingsIndex;
}(React.Component));
export { SettingsIndex };
export default withLatestContext(SettingsIndex);
var HomePanelHeader = styled(PanelHeader)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  flex-direction: column;\n  text-align: center;\n  justify-content: center;\n  font-size: 18px;\n  text-transform: unset;\n  padding: 35px 30px;\n"], ["\n  background: ", ";\n  flex-direction: column;\n  text-align: center;\n  justify-content: center;\n  font-size: 18px;\n  text-transform: unset;\n  padding: 35px 30px;\n"])), function (p) { return p.theme.background; });
var HomePanelBody = styled(PanelBody)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 30px;\n\n  h3 {\n    font-size: 14px;\n  }\n\n  ul {\n    margin: 0;\n    li {\n      line-height: 1.6;\n      /* Bullet color */\n      color: ", ";\n    }\n  }\n"], ["\n  padding: 30px;\n\n  h3 {\n    font-size: 14px;\n  }\n\n  ul {\n    margin: 0;\n    li {\n      line-height: 1.6;\n      /* Bullet color */\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.gray200; });
var HomeIcon = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  width: ", "px;\n  height: ", "px;\n  border-radius: ", "px;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 20px;\n"], ["\n  background: ", ";\n  color: ", ";\n  width: ", "px;\n  height: ", "px;\n  border-radius: ", "px;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 20px;\n"])), function (p) { return p.theme[p.color || 'gray300']; }, function (p) { return p.theme.white; }, HOME_ICON_SIZE, HOME_ICON_SIZE, HOME_ICON_SIZE);
var HomeLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; });
var HomeLinkIcon = styled(HomeLink)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow: hidden;\n  width: 100%;\n  ", ";\n"], ["\n  overflow: hidden;\n  width: 100%;\n  ", ";\n"])), flexCenter);
var ExternalHomeLink = styled(function (props) { return (<ExternalLink {...omit(props, 'isCentered')}/>); })(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n\n  ", ";\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n\n  ", ";\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.isCentered && flexCenter; });
var SupportLinkComponent = function (_a) {
    var isCentered = _a.isCentered, isOnPremise = _a.isOnPremise, href = _a.href, to = _a.to, props = __rest(_a, ["isCentered", "isOnPremise", "href", "to"]);
    if (isOnPremise) {
        return <ExternalHomeLink isCentered={isCentered} href={href} {...props}/>;
    }
    return <HomeLink to={to} {...props}/>;
};
SupportLinkComponent.propTypes = {
    isOnPremise: PropTypes.bool,
    href: PropTypes.string,
    to: PropTypes.string,
    isCentered: PropTypes.bool,
    children: PropTypes.node,
};
var AvatarContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var OrganizationName = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  line-height: 1.1em;\n\n  ", ";\n"], ["\n  line-height: 1.1em;\n\n  ", ";\n"])), overflowEllipsis);
var GridLayout = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  grid-gap: 16px;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  grid-gap: 16px;\n"])));
var GridPanel = styled(Panel)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=settingsIndex.jsx.map