import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import Annotated from 'app/components/events/meta/annotated';
import ExceptionMechanism from 'app/components/events/interfaces/exceptionMechanism';
import { STACK_TYPE } from 'app/types/stacktrace';
import ExceptionStacktraceContent from './exceptionStacktraceContent';
import ExceptionTitle from './exceptionTitle';
var ExceptionContent = function (_a) {
    var newestFirst = _a.newestFirst, event = _a.event, stackView = _a.stackView, platform = _a.platform, values = _a.values, type = _a.type;
    if (!values) {
        return null;
    }
    var children = values.map(function (exc, excIdx) { return (<div key={excIdx} className="exception">
      <ExceptionTitle type={exc.type} exceptionModule={exc === null || exc === void 0 ? void 0 : exc.module}/>
      <Annotated object={exc} objectKey="value" required>
        {function (value) { return <StyledPre className="exc-message">{value}</StyledPre>; }}
      </Annotated>
      {exc.mechanism && <ExceptionMechanism data={exc.mechanism} platform={platform}/>}
      <ExceptionStacktraceContent data={type === STACK_TYPE.ORIGINAL
        ? exc.stacktrace
        : exc.rawStacktrace || exc.stacktrace} stackView={stackView} stacktrace={exc.stacktrace} expandFirstFrame={excIdx === values.length - 1} platform={platform} newestFirst={newestFirst} event={event} chainedException={values.length > 1}/>
    </div>); });
    if (newestFirst) {
        children.reverse();
    }
    return <div>{children}</div>;
};
export default ExceptionContent;
var StyledPre = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: 0;\n"], ["\n  margin-bottom: ", ";\n  margin-top: 0;\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=exceptionContent.jsx.map