import { __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import DocumentTitle from 'react-document-title';
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import scrollToElement from 'scroll-to-element';
import styled from '@emotion/styled';
import { IS_ACCEPTANCE_TEST } from 'app/constants';
import { analytics } from 'app/utils/analytics';
import { t } from 'app/locale';
import Hook from 'app/components/hook';
import InlineSvg from 'app/components/inlineSvg';
import PageHeading from 'app/components/pageHeading';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import testableTransition from 'app/utils/testableTransition';
import OnboardingPlatform from './platform';
import OnboardingProjectSetup from './projectSetup';
import OnboardingWelcome from './welcome';
var recordAnalyticStepComplete = function (_a) {
    var organization = _a.organization, project = _a.project, step = _a.step;
    return analytics('onboarding_v2.step_compete', {
        org_id: parseInt(organization.id, 10),
        project: project ? project.slug : null,
        step: step.id,
    });
};
var ONBOARDING_STEPS = [
    {
        id: 'welcome',
        title: t('Welcome to Sentry'),
        Component: OnboardingWelcome,
    },
    {
        id: 'select-platform',
        title: t('Select a platform'),
        Component: OnboardingPlatform,
    },
    {
        id: 'get-started',
        title: t('Install the Sentry SDK'),
        Component: OnboardingProjectSetup,
    },
];
var Onboarding = /** @class */ (function (_super) {
    __extends(Onboarding, _super);
    function Onboarding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleUpdate = function (data) {
            _this.setState(data);
        };
        _this.scrollToActiveStep = function () {
            var step = _this.activeStep;
            scrollToElement("#onboarding_step_" + step.id, {
                align: 'middle',
                offset: 0,
                // Disable animations in CI - must be < 0 to disable
                duration: IS_ACCEPTANCE_TEST ? -1 : 300,
            });
        };
        return _this;
    }
    Onboarding.prototype.componentDidMount = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.componentDidUpdate = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.validateActiveStep = function () {
        if (this.activeStepIndex === -1) {
            var firstStep = this.props.steps[0].id;
            browserHistory.replace("/onboarding/" + this.props.params.orgId + "/" + firstStep + "/");
        }
    };
    Object.defineProperty(Onboarding.prototype, "activeStepIndex", {
        get: function () {
            var _this = this;
            return this.props.steps.findIndex(function (_a) {
                var id = _a.id;
                return _this.props.params.step === id;
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "activeStep", {
        get: function () {
            return this.props.steps[this.activeStepIndex];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "firstProject", {
        get: function () {
            var sortedProjects = this.props.projects.sort(function (a, b) { return new Date(a.dateCreated).getTime() - new Date(b.dateCreated).getTime(); });
            return sortedProjects.length > 0 ? sortedProjects[0] : null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "projectPlatform", {
        get: function () {
            var _a, _b, _c;
            return (_c = (_a = this.state.platform) !== null && _a !== void 0 ? _a : (_b = this.firstProject) === null || _b === void 0 ? void 0 : _b.platform) !== null && _c !== void 0 ? _c : null;
        },
        enumerable: false,
        configurable: true
    });
    Onboarding.prototype.handleNextStep = function (step, data) {
        this.handleUpdate(data);
        if (step !== this.activeStep) {
            return;
        }
        var orgId = this.props.params.orgId;
        var nextStep = this.props.steps[this.activeStepIndex + 1];
        recordAnalyticStepComplete({
            organization: this.props.organization,
            project: this.firstProject,
            step: nextStep,
        });
        browserHistory.push("/onboarding/" + orgId + "/" + nextStep.id + "/");
    };
    Onboarding.prototype.handleReturnToStep = function (step, data) {
        var orgId = this.props.params.orgId;
        this.handleUpdate(data);
        browserHistory.push("/onboarding/" + orgId + "/" + step.id + "/");
    };
    Onboarding.prototype.renderProgressBar = function () {
        var activeStepIndex = this.activeStepIndex;
        return (<ProgressBar>
        {this.props.steps.map(function (step, index) { return (<ProgressStep active={activeStepIndex === index} key={step.id}/>); })}
      </ProgressBar>);
    };
    Onboarding.prototype.renderOnboardingSteps = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var activeStepIndex = this.activeStepIndex;
        var visibleSteps = this.props.steps.slice(0, activeStepIndex + 1);
        return visibleSteps.map(function (step, index) { return (<OnboardingStep key={step.id} data-test-id={"onboarding-step-" + step.id} onAnimationComplete={_this.scrollToActiveStep} active={activeStepIndex === index}>
        <PageHeading withMargins>{step.title}</PageHeading>
        <step.Component scrollTargetId={"onboarding_step_" + step.id} active={activeStepIndex === index} orgId={orgId} project={_this.firstProject} platform={_this.projectPlatform} onReturnToStep={function (data) { return _this.handleReturnToStep(step, data); }} onComplete={function (data) { return _this.handleNextStep(step, data); }} onUpdate={_this.handleUpdate}/>
      </OnboardingStep>); });
    };
    Onboarding.prototype.render = function () {
        if (this.activeStepIndex === -1) {
            return null;
        }
        return (<OnboardingWrapper>
        <DocumentTitle title="Get Started on Sentry"/>
        <Header>
          <Container>
            <LogoSvg src="logo"/>
            {this.renderProgressBar()}
            <AnimatePresence initial={false}>
              <ProgressStatus key={this.activeStep.id}>
                {this.activeStep.title}
              </ProgressStatus>
            </AnimatePresence>
          </Container>
        </Header>
        <Container>
          <AnimatePresence initial={false}>
            {this.renderOnboardingSteps()}
          </AnimatePresence>
        </Container>
        <Hook name="onboarding:extra-chrome"/>
      </OnboardingWrapper>);
    };
    Onboarding.defaultProps = {
        steps: ONBOARDING_STEPS,
    };
    return Onboarding;
}(React.Component));
var OnboardingWrapper = styled('main')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-grow: 1;\n  background: ", ";\n  padding-bottom: 50vh;\n"], ["\n  flex-grow: 1;\n  background: ", ";\n  padding-bottom: 50vh;\n"])), function (p) { return p.theme.backgroundSecondary; });
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0 ", ";\n  max-width: ", ";\n  width: 100%;\n  margin: 0 auto;\n"], ["\n  padding: 0 ", ";\n  max-width: ", ";\n  width: 100%;\n  margin: 0 auto;\n"])), space(3), function (p) { return p.theme.breakpoints[0]; });
var Header = styled('header')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  padding: ", " 0;\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);\n\n  ", " {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    align-items: center;\n  }\n"], ["\n  background: ", ";\n  padding: ", " 0;\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);\n\n  ", " {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    align-items: center;\n  }\n"])), function (p) { return p.theme.background; }, space(4), Container);
var LogoSvg = styled(InlineSvg)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var ProgressBar = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"], ["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"])), space(4), function (p) { return p.theme.inactive; });
var ProgressStep = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"], ["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"])), function (p) { return (p.active ? p.theme.active : p.theme.inactive); }, function (p) { return p.theme.background; });
var ProgressStatus = styled(motion.div)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
ProgressStatus.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: testableTransition(),
};
var OnboardingStep = styled(motion.div)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: 70px 0;\n  margin-left: -20px;\n  padding-left: 18px;\n  counter-increment: step;\n  position: relative;\n\n  &:before {\n    content: counter(step);\n    position: absolute;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    top: -5px;\n    left: -30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: #fff;\n    font-size: 1.5rem;\n  }\n"], ["\n  margin: 70px 0;\n  margin-left: -20px;\n  padding-left: 18px;\n  counter-increment: step;\n  position: relative;\n\n  &:before {\n    content: counter(step);\n    position: absolute;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    top: -5px;\n    left: -30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: #fff;\n    font-size: 1.5rem;\n  }\n"])), function (p) { return (p.active ? p.theme.active : p.theme.gray300); });
OnboardingStep.defaultProps = {
    initial: { opacity: 0, y: 100 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 100 },
    transition: testableTransition(),
};
export default withOrganization(withProjects(Onboarding));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=onboarding.jsx.map