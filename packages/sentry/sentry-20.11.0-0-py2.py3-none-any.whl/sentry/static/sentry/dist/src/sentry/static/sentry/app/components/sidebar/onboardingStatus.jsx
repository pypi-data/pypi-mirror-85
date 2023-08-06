import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getMergedTasks } from 'app/components/onboardingWizard/taskConfig';
import { tct, t } from 'app/locale';
import OnboardingSidebar from 'app/components/onboardingWizard/sidebar';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import ProgressRing, { RingBackground, RingBar, RingText, } from 'app/components/progressRing';
var isDone = function (task) {
    return task.status === 'complete' || task.status === 'skipped';
};
var progressTextCss = function () { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n"])), theme.fontSizeMedium); };
var OnboardingStatus = /** @class */ (function (_super) {
    __extends(OnboardingStatus, _super);
    function OnboardingStatus() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleShowPanel = function () {
            var _a = _this.props, org = _a.org, onShowPanel = _a.onShowPanel;
            trackAnalyticsEvent({
                eventKey: 'onboarding.wizard_opened',
                eventName: 'Onboarding Wizard Opened',
                organization_id: org.id,
            });
            onShowPanel();
        };
        return _this;
    }
    OnboardingStatus.prototype.render = function () {
        var _a = this.props, collapsed = _a.collapsed, org = _a.org, currentPanel = _a.currentPanel, orientation = _a.orientation, hidePanel = _a.hidePanel, showPanel = _a.showPanel;
        if (!(org.features && org.features.includes('onboarding'))) {
            return null;
        }
        var tasks = getMergedTasks(org);
        var allDisplayedTasks = tasks.filter(function (task) { return task.display; });
        var doneTasks = allDisplayedTasks.filter(isDone);
        var numberRemaining = allDisplayedTasks.length - doneTasks.length;
        var pendingCompletionSeen = doneTasks.some(function (task) {
            return allDisplayedTasks.some(function (displayedTask) { return displayedTask.task === task.task; }) &&
                task.status === 'complete' &&
                !task.completionSeen;
        });
        var isActive = showPanel && currentPanel === 'todos';
        if (doneTasks.length >= allDisplayedTasks.length && !isActive) {
            return null;
        }
        return (<React.Fragment>
        <Container onClick={this.handleShowPanel} isActive={isActive}>
          <ProgressRing animateText textCss={progressTextCss} text={allDisplayedTasks.length - doneTasks.length} value={(doneTasks.length / allDisplayedTasks.length) * 100} backgroundColor="rgba(255, 255, 255, 0.15)" progressEndcaps="round" size={38} barWidth={6}/>
          {!collapsed && (<div>
              <Heading>{t('Setup Sentry')}</Heading>
              <Remaining>
                {tct('[numberRemaining] Remaining tasks', { numberRemaining: numberRemaining })}
                {pendingCompletionSeen && <PendingSeenIndicator />}
              </Remaining>
            </div>)}
        </Container>
        {isActive && (<OnboardingSidebar orientation={orientation} collapsed={collapsed} onClose={hidePanel}/>)}
      </React.Fragment>);
    };
    return OnboardingStatus;
}(React.Component));
var Heading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray200; }, space(0.25));
var Remaining = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space(0.75));
var PendingSeenIndicator = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  border-radius: 50%;\n  height: 7px;\n  width: 7px;\n"], ["\n  background: ", ";\n  border-radius: 50%;\n  height: 7px;\n  width: 7px;\n"])), function (p) { return p.theme.red300; });
var hoverCss = function (p) { return css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  background: rgba(255, 255, 255, 0.05);\n\n  ", " {\n    stroke: rgba(255, 255, 255, 0.3);\n  }\n  ", " {\n    stroke: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n"], ["\n  background: rgba(255, 255, 255, 0.05);\n\n  ", " {\n    stroke: rgba(255, 255, 255, 0.3);\n  }\n  ", " {\n    stroke: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n"])), RingBackground, RingBar, p.theme.green200, RingText, p.theme.white, Heading, p.theme.white, Remaining, p.theme.gray200); };
var Container = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: 9px 19px 9px 16px;\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  transition: background 100ms;\n\n  ", ";\n\n  &:hover {\n    ", ";\n  }\n"], ["\n  padding: 9px 19px 9px 16px;\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  transition: background 100ms;\n\n  ", ";\n\n  &:hover {\n    ", ";\n  }\n"])), space(1.5), function (p) { return p.isActive && hoverCss(p); }, hoverCss);
export default OnboardingStatus;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=onboardingStatus.jsx.map