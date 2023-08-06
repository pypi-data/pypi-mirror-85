import { __makeTemplateObject, __read, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import theme from 'app/utils/theme';
var ScoreBar = function (_a) {
    var score = _a.score, className = _a.className, vertical = _a.vertical, _b = _a.size, size = _b === void 0 ? 40 : _b, _c = _a.thickness, thickness = _c === void 0 ? 4 : _c, _d = _a.radius, radius = _d === void 0 ? 3 : _d, _e = _a.palette, palette = _e === void 0 ? theme.similarity.colors : _e;
    var maxScore = palette.length;
    // Make sure score is between 0 and maxScore
    var scoreInBounds = score >= maxScore ? maxScore : score <= 0 ? 0 : score;
    // Make sure paletteIndex is 0 based
    var paletteIndex = scoreInBounds - 1;
    // Size of bar, depends on orientation, although we could just apply a transformation via css
    var barProps = {
        vertical: vertical,
        thickness: thickness,
        size: size,
        radius: radius,
    };
    return (<div className={className}>
      {__spread(Array(scoreInBounds)).map(function (_j, i) { return (<Bar {...barProps} key={i} color={palette[paletteIndex]}/>); })}
      {__spread(Array(maxScore - scoreInBounds)).map(function (_j, i) { return (<Bar key={"empty-" + i} {...barProps} empty/>); })}
    </div>);
};
ScoreBar.propTypes = {
    vertical: PropTypes.bool,
    score: PropTypes.number.isRequired,
    /** Array of strings */
    palette: PropTypes.arrayOf(PropTypes.string),
    /** Array of classNames whose index maps to score */
    paletteClassNames: PropTypes.arrayOf(PropTypes.string),
    size: PropTypes.number,
    thickness: PropTypes.number,
    radius: PropTypes.number,
};
var StyledScoreBar = styled(ScoreBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n\n  ", ";\n"], ["\n  display: flex;\n\n  ",
    ";\n"])), function (p) {
    return p.vertical
        ? "flex-direction: column-reverse;\n    justify-content: flex-end;"
        : 'min-width: 80px;';
});
var Bar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: ", "px;\n  margin: 2px;\n  ", ";\n  ", ";\n\n  width: ", "px;\n  height: ", "px;\n"], ["\n  border-radius: ", "px;\n  margin: 2px;\n  ", ";\n  ", ";\n\n  width: ", "px;\n  height: ", "px;\n"])), function (p) { return p.radius; }, function (p) { return p.empty && "background-color: " + p.theme.similarity.empty + ";"; }, function (p) { return p.color && "background-color: " + p.color + ";"; }, function (p) { return (!p.vertical ? p.thickness : p.size); }, function (p) { return (!p.vertical ? p.size : p.thickness); });
export default StyledScoreBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=scoreBar.jsx.map