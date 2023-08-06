import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { motion, AnimatePresence } from 'framer-motion';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import { updateOnboardingTask } from 'app/actionCreators/onboardingTasks';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { IconLightning, IconLock, IconCheckmark } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import SidebarPanel from 'app/components/sidebar/sidebarPanel';
import testableTransition from 'app/utils/testableTransition';
import { findUpcomingTasks, findCompleteTasks, findActiveTasks, taskIsDone } from './utils';
import { getMergedTasks } from './taskConfig';
import Task from './task';
import ProgressHeader from './progressHeader';
/**
 * How long (in ms) to delay before beginning to mark tasks complete
 */
var INITIAL_MARK_COMPLETE_TIMEOUT = 600;
/**
 * How long (in ms) to delay between marking each unseen task as complete.
 */
var COMPLETION_SEEN_TIMEOUT = 800;
var doTimeout = function (timeout) {
    return new Promise(function (resolve) { return setTimeout(resolve, timeout); });
};
var Heading = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  margin: 0;\n  font-weight: normal;\n  border-bottom: 1px solid ", ";\n  color: ", ";\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  margin: 0;\n  font-weight: normal;\n  border-bottom: 1px solid ", ";\n  color: ", ";\n  padding-bottom: ", ";\n"])), space(0.75), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.border; }, function (p) { return p.theme.subText; }, space(1));
Heading.defaultProps = {
    positionTransition: true,
    transition: testableTransition(),
};
var completeNowHeading = (<Heading key="now">
    <IconLightning size="xs"/>
    {t('Complete now')}
  </Heading>);
var upcomingTasksHeading = (<Heading key="upcoming">
    <Tooltip containerDisplayMode="block" title={t('Some tasks should be completed before completing these tasks')}>
      <IconLock size="xs"/>
    </Tooltip>
    {t('Upcoming tasks')}
  </Heading>);
var completedTasksHeading = (<Heading key="complete">
    <IconCheckmark size="xs"/>
    {t('Completed tasks')}
  </Heading>);
var OnboardingWizardSidebar = /** @class */ (function (_super) {
    __extends(OnboardingWizardSidebar, _super);
    function OnboardingWizardSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.makeTaskUpdater = function (status) { return function (task) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            updateOnboardingTask(api, organization, { task: task, status: status, completionSeen: true });
        }; };
        _this.renderItem = function (task) { return (<AnimatedTaskItem task={task} key={"" + task.task} onSkip={_this.makeTaskUpdater('skipped')} onMarkComplete={_this.makeTaskUpdater('complete')}/>); };
        return _this;
    }
    OnboardingWizardSidebar.prototype.componentDidMount = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: 
                    // Add a minor delay to marking tasks complete to account for the animation
                    // opening of the sidebar panel
                    return [4 /*yield*/, doTimeout(INITIAL_MARK_COMPLETE_TIMEOUT)];
                    case 1:
                        // Add a minor delay to marking tasks complete to account for the animation
                        // opening of the sidebar panel
                        _a.sent();
                        this.markTasksAsSeen();
                        return [2 /*return*/];
                }
            });
        });
    };
    OnboardingWizardSidebar.prototype.markTasksAsSeen = function () {
        return __awaiter(this, void 0, void 0, function () {
            var unseenTasks, unseenTasks_1, unseenTasks_1_1, task, _a, api, organization, e_1_1;
            var e_1, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        unseenTasks = this.segmentedTasks.all
                            .filter(function (task) { return taskIsDone(task) && !task.completionSeen; })
                            .map(function (task) { return task.task; });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 6, 7, 8]);
                        unseenTasks_1 = __values(unseenTasks), unseenTasks_1_1 = unseenTasks_1.next();
                        _c.label = 2;
                    case 2:
                        if (!!unseenTasks_1_1.done) return [3 /*break*/, 5];
                        task = unseenTasks_1_1.value;
                        return [4 /*yield*/, doTimeout(COMPLETION_SEEN_TIMEOUT)];
                    case 3:
                        _c.sent();
                        _a = this.props, api = _a.api, organization = _a.organization;
                        updateOnboardingTask(api, organization, {
                            task: task,
                            completionSeen: true,
                        });
                        _c.label = 4;
                    case 4:
                        unseenTasks_1_1 = unseenTasks_1.next();
                        return [3 /*break*/, 2];
                    case 5: return [3 /*break*/, 8];
                    case 6:
                        e_1_1 = _c.sent();
                        e_1 = { error: e_1_1 };
                        return [3 /*break*/, 8];
                    case 7:
                        try {
                            if (unseenTasks_1_1 && !unseenTasks_1_1.done && (_b = unseenTasks_1.return)) _b.call(unseenTasks_1);
                        }
                        finally { if (e_1) throw e_1.error; }
                        return [7 /*endfinally*/];
                    case 8: return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(OnboardingWizardSidebar.prototype, "segmentedTasks", {
        get: function () {
            var organization = this.props.organization;
            var all = getMergedTasks(organization).filter(function (task) { return task.display; });
            var active = all.filter(findActiveTasks);
            var upcoming = all.filter(findUpcomingTasks);
            var complete = all.filter(findCompleteTasks);
            return { active: active, upcoming: upcoming, complete: complete, all: all };
        },
        enumerable: false,
        configurable: true
    });
    OnboardingWizardSidebar.prototype.render = function () {
        var _a = this.props, collapsed = _a.collapsed, orientation = _a.orientation, onClose = _a.onClose;
        var _b = this.segmentedTasks, all = _b.all, active = _b.active, upcoming = _b.upcoming, complete = _b.complete;
        var completeList = (<CompleteList key="complete-group">
        <AnimatePresence initial={false}>{complete.map(this.renderItem)}</AnimatePresence>
      </CompleteList>);
        var items = __spread([
            active.length > 0 && completeNowHeading
        ], active.map(this.renderItem), [
            upcoming.length > 0 && upcomingTasksHeading
        ], upcoming.map(this.renderItem), [
            complete.length > 0 && completedTasksHeading,
            completeList,
        ]);
        return (<TaskSidebarPanel collapsed={collapsed} hidePanel={onClose} orientation={orientation}>
        <ProgressHeader allTasks={all} completedTasks={complete}/>
        <TaskList>
          <AnimatePresence initial={false}>{items}</AnimatePresence>
        </TaskList>
      </TaskSidebarPanel>);
    };
    return OnboardingWizardSidebar;
}(React.Component));
var TaskSidebarPanel = styled(SidebarPanel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 450px;\n"], ["\n  width: 450px;\n"])));
var AnimatedTaskItem = motion.custom(Task);
AnimatedTaskItem.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    positionTransition: true,
    variants: {
        initial: {
            opacity: 0,
            y: 40,
        },
        animate: {
            opacity: 1,
            y: 0,
            transition: testableTransition({
                delay: 0.8,
                when: 'beforeChildren',
                staggerChildren: 0.3,
            }),
        },
        exit: {
            y: 20,
            z: -10,
            opacity: 0,
            transition: { duration: 0.2 },
        },
    },
};
var TaskList = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  margin: 0 ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  margin: 0 ", ";\n  margin-bottom: ", ";\n"])), space(2), space(4), space(4));
var CompleteList = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: row;\n\n  > div {\n    transition: border-radius 500ms;\n  }\n\n  > div:not(:first-of-type) {\n    margin-top: -1px;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n\n  > div:not(:last-of-type) {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: row;\n\n  > div {\n    transition: border-radius 500ms;\n  }\n\n  > div:not(:first-of-type) {\n    margin-top: -1px;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n\n  > div:not(:last-of-type) {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"])));
export default withApi(withOrganization(OnboardingWizardSidebar));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sidebar.jsx.map