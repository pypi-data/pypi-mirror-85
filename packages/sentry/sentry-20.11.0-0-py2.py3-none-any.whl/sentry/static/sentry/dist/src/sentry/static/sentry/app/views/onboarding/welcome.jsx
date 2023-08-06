import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { analytics } from 'app/utils/analytics';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import withConfig from 'app/utils/withConfig';
import withOrganization from 'app/utils/withOrganization';
var recordAnalyticsOnboardingSkipped = function (_a) {
    var organization = _a.organization;
    return analytics('onboarding_v2.skipped', { org_id: organization.id });
};
var OnboardingWelcome = function (_a) {
    var organization = _a.organization, onComplete = _a.onComplete, config = _a.config, active = _a.active;
    var user = config.user;
    var skipOnboarding = function () { return recordAnalyticsOnboardingSkipped({ organization: organization }); };
    return (<React.Fragment>
      <p>
        {tct("We're happy you're here, [name]!", {
        name: <strong>{user.name.split(' ')[0]}</strong>,
    })}
      </p>
      <p>
        {t("With Sentry, you can find and fix bugs before your customers even\n             notice a problem. When things go to hell, we'll help you fight the\n             fires. In the next two steps you will\u2026")}
      </p>
      <ul>
        <li>{t('Choose your platform.')}</li>
        <li>
          {t("Integrate Sentry into your application, invite your team, or take\n               a tour of Sentry.")}
        </li>
      </ul>
      <ActionGroup>
        <Button data-test-id="welcome-next" disabled={!active} priority="primary" onClick={function () { return onComplete({}); }}>
          {t("I'm Ready!")}
        </Button>
        <SecondaryAction>
          {tct('Not your first Sentry rodeo? [exitLink:Skip this onboarding].', {
        exitLink: <Button priority="link" onClick={skipOnboarding} href="/"/>,
    })}
        </SecondaryAction>
      </ActionGroup>
    </React.Fragment>);
};
var ActionGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var SecondaryAction = styled('small')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export default withOrganization(withConfig(OnboardingWelcome));
var templateObject_1, templateObject_2;
//# sourceMappingURL=welcome.jsx.map