import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import EventMessage from 'app/components/events/eventMessage';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import UnhandledTag, { TagAndMessageWrapper, } from '../organizationGroupDetails/unhandledTag';
var SharedGroupHeader = function (_a) {
    var group = _a.group;
    return (<Wrapper>
    <Details>
      <Title>{group.title}</Title>
      <TagAndMessageWrapper>
        {group.isUnhandled && <UnhandledTag />}
        <EventMessage message={group.culprit}/>
      </TagAndMessageWrapper>
    </Details>
  </Wrapper>);
};
export default SharedGroupHeader;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", " ", " ", ";\n  border-bottom: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  position: relative;\n  margin: 0 0 ", ";\n"], ["\n  padding: ", " ", " ", " ", ";\n  border-bottom: ", ";\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  position: relative;\n  margin: 0 0 ", ";\n"])), space(3), space(4), space(3), space(4), function (p) { return "1px solid " + p.theme.border; }, space(3));
var Details = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-width: 960px;\n  margin: 0 auto;\n"], ["\n  max-width: 960px;\n  margin: 0 auto;\n"])));
// TODO(style): the color #161319 is not yet in the color object of the theme
var Title = styled('h3')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: #161319;\n  margin: 0 0 ", ";\n  overflow-wrap: break-word;\n  line-height: 1.2;\n  font-size: ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n    line-height: 1.1;\n    ", ";\n  }\n"], ["\n  color: #161319;\n  margin: 0 0 ", ";\n  overflow-wrap: break-word;\n  line-height: 1.2;\n  font-size: ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n    line-height: 1.1;\n    ", ";\n  }\n"])), space(1), function (p) { return p.theme.fontSizeExtraLarge; }, function (props) { return props.theme.breakpoints[0]; }, function (p) { return p.theme.headerFontSize; }, overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sharedGroupHeader.jsx.map