import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ButtonBar from 'app/components/buttonBar';
import OnboardingPanel from 'app/components/onboardingPanel';
import emptyStateImg from 'app/../images/spot/alerts-empty-state.svg';
function Onboarding(_a) {
    var actions = _a.actions;
    return (<OnboardingPanel image={<AlertsImage src={emptyStateImg}/>}>
      <h3>{t('More signal, less noise')}</h3>
      <p>
        {t('Not every error is worth an email. Set your own rules for alerts you need, with information that helps.')}
      </p>
      <ButtonList gap={1}>{actions}</ButtonList>
    </OnboardingPanel>);
}
var AlertsImage = styled('img')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    user-select: none;\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    width: 220px;\n    margin-top: auto;\n    margin-bottom: auto;\n    transform: translateX(-50%);\n    left: 50%;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-60%);\n    width: 280px;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-75%);\n    width: 320px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    user-select: none;\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    width: 220px;\n    margin-top: auto;\n    margin-bottom: auto;\n    transform: translateX(-50%);\n    left: 50%;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-60%);\n    width: 280px;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-75%);\n    width: 320px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[3]; });
var ButtonList = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default Onboarding;
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map