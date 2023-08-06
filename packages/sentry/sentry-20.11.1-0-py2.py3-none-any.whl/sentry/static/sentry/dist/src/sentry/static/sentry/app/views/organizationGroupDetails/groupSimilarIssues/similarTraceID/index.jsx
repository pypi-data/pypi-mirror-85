import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import Body from './body';
import Header from './header';
var SimilarTraceID = function (_a) {
    var _b, _c;
    var event = _a.event, props = __rest(_a, ["event"]);
    var traceID = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    return (<Wrapper>
      <Header traceID={traceID}/>
      <Body traceID={traceID} event={event} {...props}/>
    </Wrapper>);
};
SimilarTraceID.propTypes = {
    event: SentryTypes.Event,
};
export default SimilarTraceID;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(2));
var templateObject_1;
//# sourceMappingURL=index.jsx.map