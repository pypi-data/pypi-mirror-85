import { __makeTemplateObject } from "tslib";
import createReactClass from 'create-react-class';
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { closeGuide, dismissGuide, nextStep, recordFinish, registerAnchor, unregisterAnchor, } from 'app/actionCreators/guides';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
import GuideStore from 'app/stores/guideStore';
import Hovercard, { Body as HovercardBody } from 'app/components/hovercard';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
/**
 * A GuideAnchor puts an informative hovercard around an element.
 * Guide anchors register with the GuideStore, which uses registrations
 * from one or more anchors on the page to determine which guides can
 * be shown on the page.
 */
var GuideAnchor = createReactClass({
    propTypes: {
        target: PropTypes.string,
        position: PropTypes.string,
        disabled: PropTypes.bool,
        offset: PropTypes.string,
    },
    mixins: [Reflux.listenTo(GuideStore, 'onGuideStateChange')],
    getInitialState: function () {
        return {
            active: false,
            orgId: null,
        };
    },
    componentDidMount: function () {
        var target = this.props.target;
        target && registerAnchor(target);
    },
    componentDidUpdate: function (_prevProps, prevState) {
        if (this.containerElement && !prevState.active && this.state.active) {
            try {
                var top_1 = this.containerElement.getBoundingClientRect().top;
                var scrollTop = window.pageYOffset;
                var centerElement = top_1 + scrollTop - window.innerHeight / 2;
                window.scrollTo({ top: centerElement });
            }
            catch (err) {
                Sentry.captureException(err);
            }
        }
    },
    componentWillUnmount: function () {
        var target = this.props.target;
        target && unregisterAnchor(target);
    },
    onGuideStateChange: function (data) {
        var active = data.currentGuide &&
            data.currentGuide.steps[data.currentStep].target === this.props.target;
        this.setState({
            active: active,
            currentGuide: data.currentGuide,
            step: data.currentStep,
            orgId: data.orgId,
        });
    },
    /**
     * Terminology:
     *
     *  - A guide can be FINISHED by clicking one of the buttons in the last step
     *  - A guide can be DISMISSED by x-ing out of it at any step except the last (where there is no x)
     *  - In both cases we consider it CLOSED
     */
    handleFinish: function (e) {
        e.stopPropagation();
        var _a = this.state, currentGuide = _a.currentGuide, orgId = _a.orgId;
        recordFinish(currentGuide.guide, orgId);
        closeGuide();
    },
    handleNextStep: function (e) {
        e.stopPropagation();
        nextStep();
    },
    handleDismiss: function (e) {
        e.stopPropagation();
        var _a = this.state, currentGuide = _a.currentGuide, step = _a.step, orgId = _a.orgId;
        dismissGuide(currentGuide.guide, step, orgId);
    },
    getHovercardBody: function () {
        var _a = this.state, currentGuide = _a.currentGuide, step = _a.step;
        var totalStepCount = currentGuide.steps.length;
        var currentStepCount = step + 1;
        var currentStep = currentGuide.steps[step];
        var lastStep = currentStepCount === totalStepCount;
        var hasManySteps = totalStepCount > 1;
        return (<GuideContainer>
        <GuideContent>
          <GuideTitle>{currentStep.title}</GuideTitle>
          <GuideDescription>{currentStep.description}</GuideDescription>
        </GuideContent>
        <GuideAction>
          <div>
            {lastStep ? (<StyledButton size="small" href="#" // to clear `#assistant` from the url
         onClick={this.handleFinish}>
                {hasManySteps ? t('Enough Already') : t('Got It')}
              </StyledButton>) : (<React.Fragment>
                <DismissButton priority="primary" size="small" href="#" // to clear `#assistant` from the url
         onClick={this.handleDismiss}>
                  {t('Dismiss')}
                </DismissButton>
                <StyledButton size="small" onClick={this.handleNextStep}>
                  {t('Next')}
                </StyledButton>
              </React.Fragment>)}
          </div>

          {hasManySteps && (<StepCount>
              {tct('[currentStepCount] of [totalStepCount]', {
            currentStepCount: currentStepCount,
            totalStepCount: totalStepCount,
        })}
            </StepCount>)}
        </GuideAction>
      </GuideContainer>);
    },
    render: function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, children = _a.children, position = _a.position, offset = _a.offset;
        var active = this.state.active;
        if (!active || disabled) {
            return children ? children : null;
        }
        return (<StyledHovercard show body={this.getHovercardBody()} tipColor={theme.purple300} position={position} offset={offset}>
        <span ref={function (el) { return (_this.containerElement = el); }}>{children}</span>
      </StyledHovercard>);
    },
});
var GuideContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"])), space(2), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.backgroundSecondary; });
var GuideContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), function (p) { return p.theme.backgroundSecondary; });
var GuideTitle = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n  font-size: ", ";\n"], ["\n  font-weight: bold;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var GuideDescription = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var GuideAction = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"])), space(1));
var StyledButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  border-color: ", ";\n  min-width: 40%;\n"], ["\n  border-color: ", ";\n  min-width: 40%;\n"])), function (p) { return p.theme.border; });
var DismissButton = styled(StyledButton)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n  }\n"], ["\n  margin-right: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n  }\n"])), space(1), function (p) { return p.theme.border; });
var StepCount = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledHovercard = styled(Hovercard)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n  }\n"], ["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n  }\n"])), HovercardBody, theme.purple300, theme.borderRadius);
export default GuideAnchor;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=guideAnchor.jsx.map