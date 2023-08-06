import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import { IconInfo } from 'app/icons';
import space from 'app/styles/space';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
var NotFound = function () { return (<NotFoundAlert type="error" icon={<IconInfo size="lg"/>}>
    <Heading>{t('Page Not Found')}</Heading>
    <p>{t('The page you are looking for was not found.')}</p>
    <p>{t('You may wish to try the following:')}</p>
    <ul>
      <li>
        {t("If you entered the address manually, double check the path. Did you\n           forget a trailing slash?")}
      </li>
      <li>
        {t("If you followed a link here, try hitting back and reloading the\n           page. It's possible the resource was moved out from under you.")}
      </li>
      <li>
        {tct('If all else fails, [link:contact us] with more details', {
    link: (<ExternalLink href="https://github.com/getsentry/sentry/issues/new/choose"/>),
})}
      </li>
    </ul>
    <p>
      {tct('Not sure what to do? [link:Return to the dashboard]', {
    link: <Link to="/"/>,
})}
    </p>
  </NotFoundAlert>); };
var NotFoundAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(3));
var Heading = styled('h1')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " 0;\n"], ["\n  font-size: ", ";\n  margin: ", " 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
export default NotFound;
var templateObject_1, templateObject_2;
//# sourceMappingURL=notFound.jsx.map