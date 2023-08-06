import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as ReactRouter from 'react-router';
import { motion } from 'framer-motion';
import moment from 'moment';
import { tct, t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
import space from 'app/styles/space';
import { navigateTo } from 'app/actionCreators/navigation';
import Card from 'app/components/card';
import Tooltip from 'app/components/tooltip';
import Button from 'app/components/button';
import { IconLock, IconCheckmark, IconClose, IconEvent } from 'app/icons';
import Avatar from 'app/components/avatar';
import LetterAvatar from 'app/components/letterAvatar';
import testableTransition from 'app/utils/testableTransition';
import { taskIsDone } from './utils';
import SkipConfirm from './skipConfirm';
var recordAnalytics = function (task, organization, action) {
    return trackAnalyticsEvent({
        eventKey: 'onboarding.wizard_clicked',
        eventName: 'Onboarding Wizard Clicked',
        organization_id: organization.id,
        todo_id: task.task,
        todo_title: task.title,
        action: action,
    });
};
function Task(_a) {
    var router = _a.router, task = _a.task, onSkip = _a.onSkip, onMarkComplete = _a.onMarkComplete, forwardedRef = _a.forwardedRef, organization = _a.organization;
    var handleSkip = function () {
        recordAnalytics(task, organization, 'skipped');
        onSkip(task.task);
    };
    var handleClick = function (e) {
        recordAnalytics(task, organization, 'clickthrough');
        e.stopPropagation();
        if (task.actionType === 'external') {
            window.open(task.location, '_blank');
        }
        if (task.actionType === 'action') {
            task.action();
        }
        if (task.actionType === 'app') {
            navigateTo(task.location + "?onboardingTask", router);
        }
    };
    if (taskIsDone(task) && task.completionSeen) {
        var completedOn = moment(task.dateCompleted);
        return (<ItemComplete ref={forwardedRef} onClick={handleClick}>
        <StatusIndicator>
          {task.status === 'complete' && <CompleteIndicator />}
          {task.status === 'skipped' && <SkippedIndicator />}
        </StatusIndicator>
        {task.title}
        <CompletedDate title={completedOn.toString()}>
          {completedOn.fromNow()}
        </CompletedDate>
        {task.user ? (<TaskUserAvatar hasTooltip user={task.user}/>) : (<Tooltip containerDisplayMode="inherit" title={t('No user was associated with completing this task')}>
            <TaskBlankAvatar round/>
          </Tooltip>)}
      </ItemComplete>);
    }
    var IncompleteMarker = task.requisiteTasks.length > 0 && (<Tooltip containerDisplayMode="block" title={tct('[requisite] before completing this task', {
        requisite: task.requisiteTasks[0].title,
    })}>
      <IconLock size="xs" color="red300"/>
    </Tooltip>);
    var SupplementComponent = task.SupplementComponent;
    var supplement = SupplementComponent && (<SupplementComponent task={task} onCompleteTask={function () { return onMarkComplete(task.task); }}/>);
    var skipAction = task.skippable && (<SkipConfirm onSkip={handleSkip}>
      {function (_a) {
        var skip = _a.skip;
        return (<SkipButton priority="link" onClick={skip}>
          {t('Skip task')}
        </SkipButton>);
    }}
    </SkipConfirm>);
    return (<Item interactive ref={forwardedRef} onClick={handleClick} data-test-id={task.task}>
      <Title>
        {IncompleteMarker}
        {task.title}
      </Title>
      <Description>{task.description + ". " + task.detailedDescription}</Description>
      {task.requisiteTasks.length === 0 && (<ActionBar>
          {task.status === 'pending' ? (<InProgressIndicator user={task.user}/>) : (<CTA>{t('Setup now')}</CTA>)}
          {skipAction}
          {supplement}
        </ActionBar>)}
    </Item>);
}
var Item = styled(Card)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  position: relative;\n"], ["\n  padding: ", ";\n  position: relative;\n"])), space(3));
var Title = styled('h5')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin: 0;\n"], ["\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin: 0;\n"])), space(0.75));
var Description = styled('p')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-top: ", ";\n  font-size: ", ";\n  line-height: 1.75rem;\n  color: ", ";\n  margin: 0;\n"], ["\n  padding-top: ", ";\n  font-size: ", ";\n  line-height: 1.75rem;\n  color: ", ";\n  margin: 0;\n"])), space(1), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; });
var ActionBar = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 40px;\n  border-top: 1px solid ", ";\n  margin: ", " -", " -", ";\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 0 ", ";\n"], ["\n  height: 40px;\n  border-top: 1px solid ", ";\n  margin: ", " -", " -", ";\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 0 ", ";\n"])), function (p) { return p.theme.border; }, space(3), space(3), space(3), space(2));
var InProgressIndicator = styled(function (_a) {
    var user = _a.user, props = __rest(_a, ["user"]);
    return (<div {...props}>
    <Tooltip disabled={!user} containerDisplayMode="flex" title={tct('This task has been started by [user]', {
        user: user === null || user === void 0 ? void 0 : user.name,
    })}>
      <IconEvent />
    </Tooltip>
    {t('Task in progress...')}
  </div>);
})(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.orange300; }, space(1));
var CTA = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: bold;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: bold;\n"])), function (p) { return p.theme.blue300; }, function (p) { return p.theme.fontSizeMedium; });
var SkipButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var ItemComplete = styled(Card)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  cursor: pointer;\n  color: ", ";\n  padding: ", " ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr max-content 20px;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  cursor: pointer;\n  color: ", ";\n  padding: ", " ", ";\n  display: grid;\n  grid-template-columns: max-content 1fr max-content 20px;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.subText; }, space(1), space(1.5), space(1));
var transition = testableTransition();
var StatusIndicator = styled(motion.div)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
StatusIndicator.defaultProps = {
    variants: {
        initial: { opacity: 0, x: 10 },
        animate: { opacity: 1, x: 0 },
    },
    transition: transition,
};
var CompleteIndicator = styled(IconCheckmark)(templateObject_10 || (templateObject_10 = __makeTemplateObject([""], [""])));
CompleteIndicator.defaultProps = {
    isCircled: true,
    color: 'green300',
};
var SkippedIndicator = styled(IconClose)(templateObject_11 || (templateObject_11 = __makeTemplateObject([""], [""])));
SkippedIndicator.defaultProps = {
    isCircled: true,
    color: 'orange300',
};
var completedItemAnimation = {
    initial: { opacity: 0, x: -10 },
    animate: { opacity: 1, x: 0 },
};
var CompletedDate = styled(motion.div)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; });
CompletedDate.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskUserAvatar = motion.custom(Avatar);
TaskUserAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskBlankAvatar = styled(motion.custom(LetterAvatar))(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  position: unset;\n"], ["\n  position: unset;\n"])));
TaskBlankAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var WrappedTask = withOrganization(ReactRouter.withRouter(Task));
export default React.forwardRef(function (props, ref) { return <WrappedTask forwardedRef={ref} {...props}/>; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=task.jsx.map