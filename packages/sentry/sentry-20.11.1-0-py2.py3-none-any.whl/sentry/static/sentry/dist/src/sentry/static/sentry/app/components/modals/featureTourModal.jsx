import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import { IconClose } from 'app/icons';
import { callIfFunction } from 'app/utils/callIfFunction';
import space from 'app/styles/space';
var defaultProps = {
    doneText: t('Done'),
};
/**
 * Provide a showModal action to the child function that lets
 * a tour be triggered.
 *
 * Once active this component will track when the tour was started and keep
 * a last known step state. Ideally the state would live entirely in this component.
 * However, once the modal has been opened state changes in this component don't
 * trigger re-renders in the modal contents. This requires a bit of duplicate state
 * to be managed around the current step.
 */
var FeatureTourModal = /** @class */ (function (_super) {
    __extends(FeatureTourModal, _super);
    function FeatureTourModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            openedAt: 0,
            current: 0,
        };
        // Record the step change and call the callback this component was given.
        _this.handleAdvance = function (current, duration) {
            _this.setState({ current: current });
            callIfFunction(_this.props.onAdvance, current, duration);
        };
        _this.handleShow = function () {
            _this.setState({ openedAt: Date.now() }, function () {
                var modalProps = {
                    steps: _this.props.steps,
                    onAdvance: _this.handleAdvance,
                    openedAt: _this.state.openedAt,
                    doneText: _this.props.doneText,
                    doneUrl: _this.props.doneUrl,
                };
                openModal(function (deps) { return <ModalContents {...deps} {...modalProps}/>; }, {
                    onClose: _this.handleClose,
                });
            });
        };
        _this.handleClose = function () {
            // The bootstrap modal and modal store both call this callback.
            // We use the state flag to deduplicate actions to upstream components.
            if (_this.state.openedAt === 0) {
                return;
            }
            var onCloseModal = _this.props.onCloseModal;
            var duration = Date.now() - _this.state.openedAt;
            callIfFunction(onCloseModal, _this.state.current, duration);
            // Reset the state now that the modal is closed, used to deduplicate close actions.
            _this.setState({ openedAt: 0, current: 0 });
        };
        return _this;
    }
    FeatureTourModal.prototype.render = function () {
        var children = this.props.children;
        return <React.Fragment>{children({ showModal: this.handleShow })}</React.Fragment>;
    };
    FeatureTourModal.defaultProps = defaultProps;
    return FeatureTourModal;
}(React.Component));
export default FeatureTourModal;
var ModalContents = /** @class */ (function (_super) {
    __extends(ModalContents, _super);
    function ModalContents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            current: 0,
            openedAt: Date.now(),
        };
        _this.handleAdvance = function () {
            var _a = _this.props, onAdvance = _a.onAdvance, openedAt = _a.openedAt;
            _this.setState(function (prevState) { return ({ current: prevState.current + 1 }); }, function () {
                var duration = Date.now() - openedAt;
                callIfFunction(onAdvance, _this.state.current, duration);
            });
        };
        return _this;
    }
    ModalContents.prototype.render = function () {
        var _a = this.props, Body = _a.Body, steps = _a.steps, doneText = _a.doneText, doneUrl = _a.doneUrl, closeModal = _a.closeModal;
        var current = this.state.current;
        var step = steps[current] !== undefined ? steps[current] : steps[steps.length - 1];
        var hasNext = steps[current + 1] !== undefined;
        return (<Body>
        <CloseButton borderless size="zero" onClick={closeModal} icon={<IconClose />}/>
        <TourContent>
          {step.image}
          <TourHeader>{step.title}</TourHeader>
          {step.body}
          <TourButtonBar gap={1}>
            {step.actions && step.actions}
            {hasNext && (<Button data-test-id="next-step" priority="primary" onClick={this.handleAdvance}>
                {t('Next')}
              </Button>)}
            {!hasNext && (<Button external href={doneUrl} data-test-id="complete-tour" onClick={closeModal} priority="primary">
                {doneText}
              </Button>)}
          </TourButtonBar>
          <StepCounter>{t('%s of %s', current + 1, steps.length)}</StepCounter>
        </TourContent>
      </Body>);
    };
    ModalContents.defaultProps = defaultProps;
    return ModalContents;
}(React.Component));
var CloseButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: -", ";\n  right: -", ";\n"], ["\n  position: absolute;\n  top: -", ";\n  right: -", ";\n"])), space(2), space(1));
var TourContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin: ", " ", " ", " ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin: ", " ", " ", " ", ";\n"])), space(3), space(4), space(1), space(4));
var TourHeader = styled('h4')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var TourButtonBar = styled(ButtonBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StepCounter = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n"], ["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
// Styled components that can be used to build tour content.
export var TourText = styled('p')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: center;\n  margin-bottom: ", ";\n"], ["\n  text-align: center;\n  margin-bottom: ", ";\n"])), space(4));
export var TourImage = styled('img')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  height: 200px;\n  margin-bottom: ", ";\n\n  /** override styles in less files */\n  max-width: 380px !important;\n  box-shadow: none !important;\n  border: 0 !important;\n  border-radius: 0 !important;\n"], ["\n  height: 200px;\n  margin-bottom: ", ";\n\n  /** override styles in less files */\n  max-width: 380px !important;\n  box-shadow: none !important;\n  border: 0 !important;\n  border-radius: 0 !important;\n"])), space(4));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=featureTourModal.jsx.map