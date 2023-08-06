import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import EventWaiter from 'app/utils/eventWaiter';
import space from 'app/styles/space';
import pulsingIndicatorStyles from 'app/styles/pulsingIndicator';
import { IconCheckmark } from 'app/icons';
import testableTransition from 'app/utils/testableTransition';
var FirstEventIndicator = function (props) { return (<EventWaiter {...props}>
    {function (_a) {
    var firstIssue = _a.firstIssue;
    return <Indicator firstIssue={firstIssue} {...props}/>;
}}
  </EventWaiter>); };
var Indicator = function (_a) {
    var firstIssue = _a.firstIssue, props = __rest(_a, ["firstIssue"]);
    return (<AnimatePresence>
    {!firstIssue ? (<Waiting key="waiting"/>) : (<Success key="received" firstIssue={firstIssue} {...props}/>)}
  </AnimatePresence>);
};
var StatusWrapper = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: 0.9em;\n  /* This is a minor hack, but the line height is just *slightly* too low,\n  making the text appear off center, so we adjust it just a bit */\n  line-height: calc(0.9em + 1px);\n  /* Ensure the event waiter status is always the height of a button */\n  height: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: 0.9em;\n  /* This is a minor hack, but the line height is just *slightly* too low,\n  making the text appear off center, so we adjust it just a bit */\n  line-height: calc(0.9em + 1px);\n  /* Ensure the event waiter status is always the height of a button */\n  height: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"])), space(1), space(4));
StatusWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: {
        initial: { opacity: 0, y: -10 },
        animate: {
            opacity: 1,
            y: 0,
            transition: testableTransition({ when: 'beforeChildren', staggerChildren: 0.35 }),
        },
        exit: { opacity: 0, y: 10 },
    },
};
var Waiting = function (props) { return (<StatusWrapper {...props}>
    <WaitingIndicator />
    <AnimatedText>{t('Waiting for verification event')}</AnimatedText>
  </StatusWrapper>); };
var Success = function (_a) {
    var organization = _a.organization, firstIssue = _a.firstIssue, props = __rest(_a, ["organization", "firstIssue"]);
    return (<StatusWrapper {...props}>
    <ReceivedIndicator />
    <AnimatedText>{t('Event was received!')}</AnimatedText>
    {firstIssue && firstIssue !== true && (<EventAction>
        <Button size="small" priority="primary" to={"/organizations/" + organization.slug + "/issues/" + firstIssue.id + "/"}>
          {t('Take me to my event')}
        </Button>
      </EventAction>)}
  </StatusWrapper>);
};
var indicatorAnimation = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
};
var AnimatedText = styled(motion.div)(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
AnimatedText.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition(),
};
var WaitingIndicator = styled(motion.div)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 6px;\n  ", ";\n"], ["\n  margin: 0 6px;\n  ", ";\n"])), pulsingIndicatorStyles);
WaitingIndicator.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition(),
};
var ReceivedIndicator = styled(IconCheckmark)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 5px;\n  margin: 0 2px;\n"], ["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 5px;\n  margin: 0 2px;\n"])), function (p) { return p.theme.green300; });
ReceivedIndicator.defaultProps = {
    size: 'sm',
};
var EventAction = styled(motion.div)(templateObject_5 || (templateObject_5 = __makeTemplateObject([""], [""])));
EventAction.defaultProps = {
    variants: {
        initial: { x: -20, opacity: 0 },
        animate: { x: 0, opacity: 1 },
    },
    transition: testableTransition(),
};
export { Indicator };
export default FirstEventIndicator;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=firstEventIndicator.jsx.map