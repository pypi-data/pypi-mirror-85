import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import ExternalLink from 'app/components/links/externalLink';
import { IconSentry } from 'app/icons';
import Hook from 'app/components/hook';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
function Footer(_a) {
    var className = _a.className;
    var config = ConfigStore.getConfig();
    return (<footer className={className}>
      <div>
        {config.isOnPremise && (<React.Fragment>
            {'Sentry '}
            {getDynamicText({
        fixed: 'Acceptance Test',
        value: config.version.current,
    })}
            <Build>
              {getDynamicText({
        fixed: 'test',
        value: config.version.build.substring(0, 7),
    })}
            </Build>
          </React.Fragment>)}
      </div>
      <LogoLink />
      <Links>
        <FooterLink href="/api/">{t('API')}</FooterLink>
        <FooterLink href="/docs/">{t('Docs')}</FooterLink>
        <FooterLink href="https://github.com/getsentry/sentry">
          {t('Contribute')}
        </FooterLink>
        {config.isOnPremise && (<FooterLink href="/out/">{t('Migrate to SaaS')}</FooterLink>)}
      </Links>
      <Hook name="footer"/>
    </footer>);
}
var Links = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"])), space(2));
var FooterLink = styled(ExternalLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"], ["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.blue300; });
var LogoLink = styled(function (props) { return (<a href="/" tabIndex={-1} {...props}>
    <IconSentry size="xl"/>
  </a>); })(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"], ["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"])), function (p) { return p.theme.subText; });
var Build = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, function (p) { return p.theme.subText; }, space(1));
var StyledFooter = styled(Footer)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.border; }, space(4), function (p) { return p.theme.breakpoints[0]; });
export default StyledFooter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=footer.jsx.map