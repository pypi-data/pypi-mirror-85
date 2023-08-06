import { __makeTemplateObject } from "tslib";
import throttle from 'lodash/throttle';
import React from 'react';
import ReactDOM from 'react-dom';
import zxcvbn from 'zxcvbn';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { tct } from 'app/locale';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
/**
 * NOTE: Do not import this component synchronously. The zxcvbn library is
 * relatively large. This component should be loaded async as a split chunk.
 */
/**
 * The maximum score that zxcvbn reports
 */
var MAX_SCORE = 5;
var PasswordStrength = function (_a) {
    var value = _a.value, _b = _a.labels, labels = _b === void 0 ? ['Very Weak', 'Very Weak', 'Weak', 'Strong', 'Very Strong'] : _b, _c = _a.colors, colors = _c === void 0 ? [theme.red300, theme.red300, theme.yellow300, theme.green300, theme.green300] : _c;
    if (value === '') {
        return null;
    }
    var result = zxcvbn(value);
    if (!result) {
        return null;
    }
    var score = result.score;
    var percent = Math.round(((score + 1) / MAX_SCORE) * 100);
    var styles = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    background: ", ";\n    width: ", "%;\n    height: 100%;\n  "], ["\n    background: ", ";\n    width: ", "%;\n    height: 100%;\n  "])), colors[score], percent);
    return (<React.Fragment>
      <StrengthProgress role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}>
        <div css={styles}/>
      </StrengthProgress>
      <StrengthLabel>
        {tct('Strength: [textScore]', {
        textScore: <ScoreText>{labels[score]}</ScoreText>,
    })}
      </StrengthLabel>
    </React.Fragment>);
};
var StrengthProgress = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  height: 8px;\n  border-radius: 2px;\n  overflow: hidden;\n"], ["\n  background: ", ";\n  height: 8px;\n  border-radius: 2px;\n  overflow: hidden;\n"])), theme.gray200);
var StrengthLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 0.8em;\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  margin-top: ", ";\n  color: ", ";\n"])), space(0.25), theme.gray400);
var ScoreText = styled('strong')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.black; });
export default PasswordStrength;
/**
 * This is a shim that allows the password strength component to be used
 * outside of our main react application. Mostly useful since all of our
 * registration pages aren't in the react app.
 */
export var attachTo = function (_a) {
    var input = _a.input, element = _a.element;
    return element &&
        input &&
        input.addEventListener('input', throttle(function (e) {
            ReactDOM.render(<PasswordStrength value={e.target.value}/>, element);
        }));
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=passwordStrength.jsx.map