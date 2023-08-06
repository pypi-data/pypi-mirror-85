import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { motion, AnimatePresence } from 'framer-motion';
import theme from 'app/utils/theme';
import testableTransition from 'app/utils/testableTransition';
var Text = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  width: 100%;\n  color: ", ";\n  font-size: ", ";\n  padding-top: 1px;\n  transition: color 100ms;\n  ", "\n"], ["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  width: 100%;\n  color: ", ";\n  font-size: ", ";\n  padding-top: 1px;\n  transition: color 100ms;\n  ", "\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.textCss && p.textCss(p); });
var AnimatedText = motion.custom(Text);
AnimatedText.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: testableTransition(),
};
var ProgressRing = function (_a) {
    var value = _a.value, _b = _a.minValue, minValue = _b === void 0 ? 0 : _b, _c = _a.maxValue, maxValue = _c === void 0 ? 100 : _c, _d = _a.size, size = _d === void 0 ? 20 : _d, _e = _a.barWidth, barWidth = _e === void 0 ? 3 : _e, text = _a.text, textCss = _a.textCss, _f = _a.animateText, animateText = _f === void 0 ? false : _f, _g = _a.progressColor, progressColor = _g === void 0 ? theme.green300 : _g, _h = _a.backgroundColor, backgroundColor = _h === void 0 ? theme.gray200 : _h, progressEndcaps = _a.progressEndcaps, p = __rest(_a, ["value", "minValue", "maxValue", "size", "barWidth", "text", "textCss", "animateText", "progressColor", "backgroundColor", "progressEndcaps"]);
    var radius = size / 2 - barWidth / 2;
    var circumference = 2 * Math.PI * radius;
    var boundedValue = Math.min(Math.max(value, minValue), maxValue);
    var progress = (boundedValue - minValue) / (maxValue - minValue);
    var percent = progress * 100;
    var progressOffset = (1 - progress) * circumference;
    var TextComponent = animateText ? AnimatedText : Text;
    var textNode = (<TextComponent key={text === null || text === void 0 ? void 0 : text.toString()} {...{ textCss: textCss, percent: percent }}>
      {text}
    </TextComponent>);
    textNode = animateText ? (<AnimatePresence initial={false}>{textNode}</AnimatePresence>) : (textNode);
    var ringColor = typeof progressColor === 'function' ? progressColor({ percent: percent, theme: theme }) : progressColor;
    return (<RingSvg height={radius * 2 + barWidth} width={radius * 2 + barWidth} {...p}>
      <RingBackground r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={backgroundColor}/>
      <RingBar strokeDashoffset={progressOffset} strokeLinecap={progressEndcaps} circumference={circumference} r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={ringColor}/>
      <foreignObject height="100%" width="100%">
        {text !== undefined && textNode}
      </foreignObject>
    </RingSvg>);
};
var RingSvg = styled('svg')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var RingBackground = styled('circle')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  transition: stroke 100ms;\n"], ["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  transition: stroke 100ms;\n"])), function (p) { return p.color; }, function (p) { return p.barWidth; });
var RingBar = styled('circle')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  stroke-dasharray: ", " ", ";\n  transform: rotate(-90deg);\n  transform-origin: 50% 50%;\n  transition: stroke-dashoffset 200ms, stroke 100ms;\n"], ["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  stroke-dasharray: ", " ", ";\n  transform: rotate(-90deg);\n  transform-origin: 50% 50%;\n  transition: stroke-dashoffset 200ms, stroke 100ms;\n"])), function (p) { return p.color; }, function (p) { return p.barWidth; }, function (p) { return p.circumference; }, function (p) { return p.circumference; });
export default ProgressRing;
// We export components to allow for css selectors
export { RingBar, RingBackground, Text as RingText };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=progressRing.jsx.map