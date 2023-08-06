import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { analytics } from 'app/utils/analytics';
import ExternalLink from 'app/components/links/externalLink';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
var ResourceCard = function (_a) {
    var title = _a.title, link = _a.link, imgUrl = _a.imgUrl;
    return (<ResourceCardWrapper onClick={function () { return analytics('orgdash.resource_clicked', { link: link, title: title }); }}>
    <StyledLink href={link}>
      <StyledImg src={imgUrl} alt={title}/>
      <StyledTitle>{title}</StyledTitle>
    </StyledLink>
  </ResourceCardWrapper>);
};
export default ResourceCard;
var ResourceCardWrapper = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  padding: ", ";\n  margin-bottom: 0;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  padding: ", ";\n  margin-bottom: 0;\n"])), space(3));
var StyledLink = styled(ExternalLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var StyledImg = styled('img')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: block;\n  margin: 0 auto ", " auto;\n  height: 160px;\n"], ["\n  display: block;\n  margin: 0 auto ", " auto;\n  height: 160px;\n"])), space(3));
var StyledTitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  font-weight: bold;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  font-weight: bold;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=resourceCard.jsx.map