import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import OnboardingPanel from 'app/components/onboardingPanel';
import FeatureTourModal, { TourText, TourImage, } from 'app/components/modals/featureTourModal';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import emptyStateImg from '../../../images/spot/performance-empty-state.svg';
import tourMetrics from '../../../images/spot/performance-tour-metrics.svg';
import tourCorrelate from '../../../images/spot/performance-tour-correlate.svg';
import tourTrace from '../../../images/spot/performance-tour-trace.svg';
import tourAlert from '../../../images/spot/performance-tour-alert.svg';
var performanceSetupUrl = 'https://docs.sentry.io/performance-monitoring/getting-started/';
var docsLink = (<Button external href={performanceSetupUrl}>
    {t('Setup')}
  </Button>);
var TOUR_STEPS = [
    {
        title: t('Track Application Metrics'),
        image: <TourImage src={tourMetrics}/>,
        body: (<TourText>
        {t('Monitor your slowest pageloads and APIs to see which users are having the worst time.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Correlate Errors and Performance'),
        image: <TourImage src={tourCorrelate}/>,
        body: (<TourText>
        {t('See what errors occurred within a transaction and the impact of those errors.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Watch and Alert'),
        image: <TourImage src={tourAlert}/>,
        body: (<TourText>
        {t('Highlight mission-critical pages and APIs and set latency alerts to notify you before things go wrong.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Trace Across Systems'),
        image: <TourImage src={tourTrace}/>,
        body: (<TourText>
        {t("Follow a trace from a user's session and drill down to identify any bottlenecks that occur.")}
      </TourText>),
    },
];
function Onboarding(_a) {
    var organization = _a.organization;
    function handleAdvance(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'performance_views.tour.advance',
            eventName: 'Performance Views: Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'performance_views.tour.close',
            eventName: 'Performance Views: Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    return (<OnboardingPanel image={<PerfImage src={emptyStateImg}/>}>
      <h3>{t('Pinpoint problems')}</h3>
      <p>
        {t('Something seem slow? Track down transactions to connect the dots between 10-second page loads and poor-performing API calls or slow database queries.')}
      </p>
      <ButtonList gap={1}>
        <FeatureTourModal steps={TOUR_STEPS} onAdvance={handleAdvance} onCloseModal={handleClose} doneUrl={performanceSetupUrl} doneText={t('Start Setup')}>
          {function (_a) {
        var showModal = _a.showModal;
        return (<Button priority="default" onClick={function () {
            trackAnalyticsEvent({
                eventKey: 'performance_views.tour.start',
                eventName: 'Performance Views: Tour Start',
                organization_id: parseInt(organization.id, 10),
            });
            showModal();
        }}>
              {t('Take a Tour')}
            </Button>);
    }}
        </FeatureTourModal>
        <Button priority="primary" target="_blank" href="https://docs.sentry.io/performance-monitoring/getting-started/">
          {t('Start Setup')}
        </Button>
      </ButtonList>
    </OnboardingPanel>);
}
var PerfImage = styled('img')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ButtonList = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default Onboarding;
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map