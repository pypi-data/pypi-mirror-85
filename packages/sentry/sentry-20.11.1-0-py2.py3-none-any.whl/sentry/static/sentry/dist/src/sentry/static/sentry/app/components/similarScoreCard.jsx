import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
var scoreComponents = {
    'exception:message:character-shingles': t('Exception Message'),
    'exception:stacktrace:pairs': t('Stack Trace Frames'),
    'message:message:character-shingles': t('Log Message'),
};
var SimilarScoreCard = function (_a) {
    var _b = _a.scoreList, scoreList = _b === void 0 ? [] : _b;
    if (scoreList.length === 0) {
        return null;
    }
    return (<React.Fragment>
      {scoreList.map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], score = _b[1];
        return (<Wrapper key={key}>
          <div>{scoreComponents[key]}</div>

          <Score score={score === null ? score : Math.round(score * 5)}/>
        </Wrapper>);
    })}
    </React.Fragment>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n"])), space(0.25));
var Score = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 16px;\n  width: 48px;\n  border-radius: 2px;\n  background-color: ", ";\n"], ["\n  height: 16px;\n  width: 48px;\n  border-radius: 2px;\n  background-color: ",
    ";\n"])), function (p) {
    return p.score === null ? p.theme.similarity.empty : p.theme.similarity.colors[p.score];
});
export default SimilarScoreCard;
var templateObject_1, templateObject_2;
//# sourceMappingURL=similarScoreCard.jsx.map