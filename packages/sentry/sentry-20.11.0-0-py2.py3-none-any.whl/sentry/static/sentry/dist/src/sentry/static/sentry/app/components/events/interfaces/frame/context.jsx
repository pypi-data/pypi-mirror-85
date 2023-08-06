import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import ClippedBox from 'app/components/clippedBox';
import ContextLine from 'app/components/events/interfaces/contextLine';
import FrameRegisters from 'app/components/events/interfaces/frameRegisters/frameRegisters';
import FrameVariables from 'app/components/events/interfaces/frameVariables';
import ErrorBoundary from 'app/components/errorBoundary';
import { IconFlag } from 'app/icons';
import { Assembly } from 'app/components/events/interfaces/assembly';
import { parseAssembly } from 'app/components/events/interfaces/utils';
import { OpenInContextLine } from 'app/components/events/interfaces/openInContextLine';
import StacktraceLink from 'app/components/events/interfaces/stacktraceLink';
import withOrganization from 'app/utils/withOrganization';
import space from 'app/styles/space';
var Context = function (_a) {
    var _b = _a.hasContextVars, hasContextVars = _b === void 0 ? false : _b, _c = _a.hasContextSource, hasContextSource = _c === void 0 ? false : _c, _d = _a.hasContextRegisters, hasContextRegisters = _d === void 0 ? false : _d, _e = _a.isExpanded, isExpanded = _e === void 0 ? false : _e, _f = _a.hasAssembly, hasAssembly = _f === void 0 ? false : _f, _g = _a.expandable, expandable = _g === void 0 ? false : _g, _h = _a.emptySourceNotation, emptySourceNotation = _h === void 0 ? false : _h, registers = _a.registers, components = _a.components, frame = _a.frame, event = _a.event, organization = _a.organization;
    if (!hasContextSource && !hasContextVars && !hasContextRegisters && !hasAssembly) {
        return emptySourceNotation ? (<div className="empty-context">
        <StyledIconFlag size="xs"/>
        <p>{t('No additional details are available for this frame.')}</p>
      </div>) : null;
    }
    var getContextLines = function () {
        if (isExpanded) {
            return frame.context;
        }
        return frame.context.filter(function (l) { return l[0] === frame.lineNo; });
    };
    var contextLines = getContextLines();
    var startLineNo = hasContextSource ? frame.context[0][0] : undefined;
    return (<ol start={startLineNo} className={"context " + (isExpanded ? 'expanded' : '')}>
      {defined(frame.errors) && (<li className={expandable ? 'expandable error' : 'error'} key="errors">
          {frame.errors.join(', ')}
        </li>)}

      {frame.context &&
        contextLines.map(function (line, index) {
            var isActive = frame.lineNo === line[0];
            var hasComponents = isActive && components.length > 0;
            return (<StyledContextLine key={index} line={line} isActive={isActive}>
              {hasComponents && (<ErrorBoundary mini>
                  <OpenInContextLine key={index} lineNo={line[0]} filename={frame.filename || ''} components={components}/>
                </ErrorBoundary>)}
              {(organization === null || organization === void 0 ? void 0 : organization.features.includes('integrations-stacktrace-link')) &&
                isActive &&
                isExpanded && (<ErrorBoundary mini>
                    <StacktraceLink key={index} lineNo={line[0]} frame={frame} event={event}/>
                  </ErrorBoundary>)}
            </StyledContextLine>);
        })}

      {(hasContextRegisters || hasContextVars) && (<StyledClippedBox clipHeight={100}>
          {hasContextRegisters && <FrameRegisters data={registers} key="registers"/>}
          {hasContextVars && <FrameVariables data={frame.vars || {}} key="vars"/>}
        </StyledClippedBox>)}

      {hasAssembly && (<Assembly {...parseAssembly(frame.package)} filePath={frame.absPath}/>)}
    </ol>);
};
export default withOrganization(Context);
var StyledClippedBox = styled(ClippedBox)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"], ["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"])), space(3));
var StyledIconFlag = styled(IconFlag)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledContextLine = styled(ContextLine)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"], ["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=context.jsx.map