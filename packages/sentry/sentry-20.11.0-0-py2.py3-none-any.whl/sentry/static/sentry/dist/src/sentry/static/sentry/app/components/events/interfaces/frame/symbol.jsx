import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import { defined } from 'app/utils';
import { t } from 'app/locale';
import { IconFilter } from 'app/icons';
import FunctionName from './functionName';
import { getFrameHint } from './utils';
var Symbol = function (_a) {
    var frame = _a.frame, onFunctionNameToggle = _a.onFunctionNameToggle, showCompleteFunctionName = _a.showCompleteFunctionName;
    var hasFunctionNameHiddenDetails = defined(frame.rawFunction) &&
        defined(frame.function) &&
        frame.function !== frame.rawFunction;
    var getFunctionNameTooltipTitle = function () {
        if (!hasFunctionNameHiddenDetails) {
            return undefined;
        }
        if (!showCompleteFunctionName) {
            return t('Expand function details');
        }
        return t('Hide function details');
    };
    var _b = __read(getFrameHint(frame), 2), hint = _b[0], hintIcon = _b[1];
    var enablePathTooltip = defined(frame.absPath) && frame.absPath !== frame.filename;
    var functionNameTooltipTitle = getFunctionNameTooltipTitle();
    return (<Wrapper>
      <FunctionNameToggleTooltip title={functionNameTooltipTitle} containerDisplayMode="inline-flex">
        <FunctionNameToggleIcon hasFunctionNameHiddenDetails={hasFunctionNameHiddenDetails} onClick={hasFunctionNameHiddenDetails ? onFunctionNameToggle : undefined} size="xs" color="purple300"/>
      </FunctionNameToggleTooltip>
      <Data>
        <StyledFunctionName frame={frame} showCompleteFunctionName={showCompleteFunctionName} hasHiddenDetails={hasFunctionNameHiddenDetails}/>
        {hint && (<HintStatus>
            <Tooltip title={hint}>{hintIcon}</Tooltip>
          </HintStatus>)}
        {frame.filename && (<FileNameTooltip title={frame.absPath} disabled={!enablePathTooltip}>
            <Filename>
              {'('}
              {frame.filename}
              {frame.lineNo && ":" + frame.lineNo}
              {')'}
            </Filename>
          </FileNameTooltip>)}
      </Data>
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: left;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  order: 3;\n  flex: 1;\n\n  display: flex;\n\n  code {\n    background: transparent;\n    color: ", ";\n    padding-right: ", ";\n  }\n\n  @media (min-width: ", ") {\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"], ["\n  text-align: left;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  order: 3;\n  flex: 1;\n\n  display: flex;\n\n  code {\n    background: transparent;\n    color: ", ";\n    padding-right: ", ";\n  }\n\n  @media (min-width: ", ") {\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"])), function (p) { return p.theme.textColor; }, space(0.5), function (props) { return props.theme.breakpoints[0]; });
var StyledFunctionName = styled(FunctionName)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.75));
var Data = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  max-width: 100%;\n"], ["\n  max-width: 100%;\n"])));
var HintStatus = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  top: ", ";\n  margin: 0 ", " 0 -", ";\n"], ["\n  position: relative;\n  top: ", ";\n  margin: 0 ", " 0 -", ";\n"])), space(0.25), space(0.75), space(0.25));
var FileNameTooltip = styled(Tooltip)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var Filename = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.purple300; });
var FunctionNameToggleIcon = styled(IconFilter, {
    shouldForwardProp: function (prop) { return prop !== 'hasFunctionNameHiddenDetails'; },
})(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n  ", ";\n"], ["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n  ", ";\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return !p.hasFunctionNameHiddenDetails && 'opacity: 0; cursor: inherit;'; });
var FunctionNameToggleTooltip = styled(Tooltip)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  height: 16px;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  height: 16px;\n  align-items: center;\n  margin-right: ", ";\n"])), space(0.75));
export default Symbol;
export { FunctionNameToggleIcon };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=symbol.jsx.map