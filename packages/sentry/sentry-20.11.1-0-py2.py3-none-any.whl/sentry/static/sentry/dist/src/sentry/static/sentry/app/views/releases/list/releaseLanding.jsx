import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { analytics } from 'app/utils/analytics';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import OnboardingPanel from 'app/components/onboardingPanel';
import withProject from 'app/utils/withProject';
import FeatureTourModal, { TourImage, TourText, } from 'app/components/modals/featureTourModal';
import AsyncView from 'app/views/asyncView';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import emptyStateImg from '../../../../images/spot/releases-empty-state.svg';
import commitImage from '../../../../images/spot/releases-tour-commits.svg';
import statsImage from '../../../../images/spot/releases-tour-stats.svg';
import resolutionImage from '../../../../images/spot/releases-tour-resolution.svg';
import emailImage from '../../../../images/spot/releases-tour-email.svg';
var TOUR_STEPS = [
    {
        title: t('Suspect Commits'),
        image: <TourImage src={commitImage}/>,
        body: (<TourText>
        {t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage.')}
      </TourText>),
    },
    {
        title: t('Release Stats'),
        image: <TourImage src={statsImage}/>,
        body: (<TourText>
        {t('Get an overview of the commits in each release, and which issues were introduced or fixed.')}
      </TourText>),
    },
    {
        title: t('Easily Resolve'),
        image: <TourImage src={resolutionImage}/>,
        body: (<TourText>
        {t('Automatically resolve issues by including the issue number in your commit message.')}
      </TourText>),
    },
    {
        title: t('Deploy Emails'),
        image: <TourImage src={emailImage}/>,
        body: (<TourText>
        {t('Receive email notifications about when your code gets deployed. This can be customized in settings.')}
      </TourText>),
    },
];
var setupDocs = 'https://docs.sentry.io/product/releases/';
var ReleaseLanding = /** @class */ (function (_super) {
    __extends(ReleaseLanding, _super);
    function ReleaseLanding() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // if there are no releases in the last 30 days, we want to show releases promo, otherwise empty message
    ReleaseLanding.prototype.getEndpoints = function () {
        var slug = this.props.organization.slug;
        var query = {
            per_page: 1,
            summaryStatsPeriod: '30d',
        };
        return [['releases', "/organizations/" + slug + "/releases/", { query: query }]];
    };
    ReleaseLanding.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        if (this.state.releases.length === 0) {
            return <Promo organization={organization} project={project}/>;
        }
        return <EmptyStateWarning small>{t('There are no releases.')}</EmptyStateWarning>;
    };
    return ReleaseLanding;
}(AsyncView));
var Promo = /** @class */ (function (_super) {
    __extends(Promo, _super);
    function Promo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAdvance = function (index) {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            analytics('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: project && parseInt(project.id, 10),
                step_id: index,
                step_title: TOUR_STEPS[index].title,
            });
        };
        return _this;
    }
    Promo.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        analytics('releases.landing_card_viewed', {
            org_id: parseInt(organization.id, 10),
            project_id: project && parseInt(project.id, 10),
        });
    };
    Promo.prototype.render = function () {
        return (<OnboardingPanel image={<img src={emptyStateImg}/>}>
        <h3>{t('Demystify Releases')}</h3>
        <p>
          {t('Did you know how many errors your latest release triggered? We do. And more, too.')}
        </p>
        <ButtonList gap={1}>
          <FeatureTourModal steps={TOUR_STEPS} onAdvance={this.handleAdvance}>
            {function (_a) {
            var showModal = _a.showModal;
            return (<Button priority="default" onClick={showModal}>
                {t('Take a Tour')}
              </Button>);
        }}
          </FeatureTourModal>
          <Button priority="primary" href={setupDocs} external>
            {t('Start Setup')}
          </Button>
        </ButtonList>
      </OnboardingPanel>);
    };
    return Promo;
}(React.Component));
var ButtonList = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default withProject(ReleaseLanding);
var templateObject_1;
//# sourceMappingURL=releaseLanding.jsx.map