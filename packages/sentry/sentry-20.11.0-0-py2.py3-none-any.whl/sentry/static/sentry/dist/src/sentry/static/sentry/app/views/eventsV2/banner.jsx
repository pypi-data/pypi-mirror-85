import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Banner from 'app/components/banner';
import Button from 'app/components/button';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import FeatureTourModal, { TourText, TourImage, } from 'app/components/modals/featureTourModal';
import space from 'app/styles/space';
import BackgroundSpace from './backgroundSpace';
import tourExplore from '../../../images/spot/discover-tour-explore.svg';
import tourFilter from '../../../images/spot/discover-tour-filter.svg';
import tourGroup from '../../../images/spot/discover-tour-group.svg';
import tourAlert from '../../../images/spot/discover-tour-alert.svg';
var docsUrl = 'https://docs.sentry.io/product/discover-queries/';
var docsLink = (<Button external href={docsUrl}>
    {t('View Docs')}
  </Button>);
var TOUR_STEPS = [
    {
        title: t('Explore Data over Time'),
        image: <TourImage src={tourExplore}/>,
        body: (<TourText>
        {t('Analyze and visualize all of your data over time to find answers to your most complex problems.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Filter on Event Attributes.'),
        image: <TourImage src={tourFilter}/>,
        body: (<TourText>
        {t('Drill down on data by any custom tag or field to reduce noise and hone in on specific areas.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Group Data by Tags'),
        image: <TourImage src={tourGroup}/>,
        body: (<TourText>
        {t('Go beyond Issues and create custom groupings to investigate events from a different lens.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Save, Share and Alert'),
        image: <TourImage src={tourAlert}/>,
        body: (<TourText>
        {t('Send insights to your team and set alerts to monitor any future spikes.')}
      </TourText>),
    },
];
function DiscoverBanner(_a) {
    var organization = _a.organization, resultsUrl = _a.resultsUrl, isSmallBanner = _a.isSmallBanner, onHideBanner = _a.onHideBanner;
    function onAdvance(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'discover_v2.tour.advance',
            eventName: 'Discoverv2: Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function onCloseModal(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'discover_v2.tour.close',
            eventName: 'Discoverv2: Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    return (<StyledBanner title={t('Discover Trends')} subtitle={t('Customize and save queries by search conditions, event fields, and tags')} backgroundComponent={<BackgroundSpace />} onCloseClick={onHideBanner}>
      <StarterButton size={isSmallBanner ? 'xsmall' : undefined} to={resultsUrl} onClick={function () {
        trackAnalyticsEvent({
            eventKey: 'discover_v2.build_new_query',
            eventName: 'Discoverv2: Build a new Discover Query',
            organization_id: parseInt(organization.id, 10),
        });
    }}>
        {t('Build a new query')}
      </StarterButton>
      <FeatureTourModal steps={TOUR_STEPS} doneText={t('View all Events')} doneUrl={resultsUrl} onAdvance={onAdvance} onCloseModal={onCloseModal}>
        {function (_a) {
        var showModal = _a.showModal;
        return (<StarterButton size={isSmallBanner ? 'xsmall' : undefined} onClick={function () {
            trackAnalyticsEvent({
                eventKey: 'discover_v2.tour.start',
                eventName: 'Discoverv2: Tour Start',
                organization_id: parseInt(organization.id, 10),
            });
            showModal();
        }}>
            {t('Get a Tour')}
          </StarterButton>);
    }}
      </FeatureTourModal>
    </StyledBanner>);
}
export default DiscoverBanner;
var StyledBanner = styled(Banner)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-height: 220px;\n\n  @media (min-width: ", ") {\n    max-height: 260px;\n  }\n"], ["\n  max-height: 220px;\n\n  @media (min-width: ", ") {\n    max-height: 260px;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var StarterButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=banner.jsx.map