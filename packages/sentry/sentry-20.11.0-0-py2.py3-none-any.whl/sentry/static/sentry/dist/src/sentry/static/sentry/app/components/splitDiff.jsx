import { __makeTemplateObject, __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { diffChars, diffWords, diffLines } from 'diff';
var diffFnMap = {
    chars: diffChars,
    words: diffWords,
    lines: diffLines,
};
var SplitDiff = function (_a) {
    var className = _a.className, _b = _a.type, type = _b === void 0 ? 'lines' : _b, base = _a.base, target = _a.target;
    var diffFn = diffFnMap[type];
    var baseLines = base.split('\n');
    var targetLines = target.split('\n');
    var _c = __read(baseLines.length > targetLines.length
        ? [baseLines, targetLines]
        : [targetLines, baseLines], 1), largerArray = _c[0];
    var results = largerArray.map(function (_line, index) {
        return diffFn(baseLines[index] || '', targetLines[index] || '', { newlineIsToken: true });
    });
    return (<SplitTable className={className}>
      <SplitBody>
        {results.map(function (line, j) {
        var highlightAdded = line.find(function (result) { return result.added; });
        var highlightRemoved = line.find(function (result) { return result.removed; });
        return (<tr key={j}>
              <Cell isRemoved={highlightRemoved}>
                <Line>
                  {line
            .filter(function (result) { return !result.added; })
            .map(function (result, i) { return (<Word key={i} isRemoved={result.removed}>
                        {result.value}
                      </Word>); })}
                </Line>
              </Cell>

              <Gap />

              <Cell isAdded={highlightAdded}>
                <Line>
                  {line
            .filter(function (result) { return !result.removed; })
            .map(function (result, i) { return (<Word key={i} isAdded={result.added}>
                        {result.value}
                      </Word>); })}
                </Line>
              </Cell>
            </tr>);
    })}
      </SplitBody>
    </SplitTable>);
};
SplitDiff.propTypes = {
    base: PropTypes.string,
    target: PropTypes.string,
    type: PropTypes.oneOf(['lines', 'words', 'chars']),
};
var SplitTable = styled('table')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  table-layout: fixed;\n  border-collapse: collapse;\n  width: 100%;\n"], ["\n  table-layout: fixed;\n  border-collapse: collapse;\n  width: 100%;\n"])));
var SplitBody = styled('tbody')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeSmall; });
var Cell = styled('td')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  vertical-align: top;\n  ", ";\n  ", ";\n"], ["\n  vertical-align: top;\n  ", ";\n  ", ";\n"])), function (p) { return p.isRemoved && "background-color: " + p.theme.diff.removedRow; }, function (p) { return p.isAdded && "background-color: " + p.theme.diff.addedRow; });
var Gap = styled('td')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 20px;\n"], ["\n  width: 20px;\n"])));
var Line = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var Word = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  ", ";\n  ", ";\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  ", ";\n  ", ";\n"])), function (p) { return p.isRemoved && "background-color: " + p.theme.diff.removed; }, function (p) { return p.isAdded && "background-color: " + p.theme.diff.added; });
export default SplitDiff;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=splitDiff.jsx.map