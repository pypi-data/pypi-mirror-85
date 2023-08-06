import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconSettings } from 'app/icons';
import { navigateTo } from 'app/actionCreators/navigation';
import { t } from 'app/locale';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import NavTabs from 'app/components/navTabs';
import * as Layout from 'app/components/layouts/thirds';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
import CreateRuleButton from './createRuleButton';
var AlertHeader = function (_a) {
    var router = _a.router, organization = _a.organization, activeTab = _a.activeTab;
    /**
     * Incidents list is currently at the organization level, but the link needs to
     * go down to a specific project scope.
     */
    var handleNavigateToSettings = function (e) {
        e.preventDefault();
        navigateTo("/settings/" + organization.slug + "/projects/:projectId/alerts/", router);
    };
    return (<Layout.Header>
      <StyledLayoutHeaderContent>
        <StyledLayoutTitle>{t('Alerts')}</StyledLayoutTitle>
        <StyledNavTabs underlined>
          <Feature features={['incidents']} organization={organization}>
            <li className={activeTab === 'stream' ? 'active' : ''}>
              <Link to={"/organizations/" + organization.slug + "/alerts/"}>
                {t('Metric Alerts')}
              </Link>
            </li>
          </Feature>
          <li className={activeTab === 'rules' ? 'active' : ''}>
            <Link to={"/organizations/" + organization.slug + "/alerts/rules/"}>
              {t('Alert Rules')}
            </Link>
          </li>
        </StyledNavTabs>
      </StyledLayoutHeaderContent>
      <Layout.HeaderActions>
        <Actions gap={1}>
          <Button size="small" onClick={handleNavigateToSettings} href="#" icon={<IconSettings size="xs"/>}>
            {t('Settings')}
          </Button>

          <CreateRuleButton organization={organization} router={router} iconProps={{ size: 'xs' }} buttonProps={{ size: 'small' }}/>
        </Actions>
      </Layout.HeaderActions>
    </Layout.Header>);
};
export default AlertHeader;
var StyledLayoutHeaderContent = styled(Layout.HeaderContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledLayoutTitle = styled(Layout.Title)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var StyledNavTabs = styled(NavTabs)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: 15px;\n  margin-bottom: 0;\n  border-bottom: 0 !important;\n  li {\n    margin-right: ", ";\n  }\n  li > a {\n    padding: ", " ", ";\n  }\n"], ["\n  margin-top: 15px;\n  margin-bottom: 0;\n  border-bottom: 0 !important;\n  li {\n    margin-right: ", ";\n  }\n  li > a {\n    padding: ", " ", ";\n  }\n"])), space(0.5), space(1), space(2));
var Actions = styled(ButtonBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 32px;\n"], ["\n  height: 32px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=header.jsx.map