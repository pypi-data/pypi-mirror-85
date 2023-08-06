import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
function OnboardingPanel(_a) {
    var className = _a.className, image = _a.image, children = _a.children;
    return (<Panel className={className}>
      <Container>
        <IlloBox>{image}</IlloBox>
        <StyledBox>{children}</StyledBox>
      </Container>
    </Panel>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    flex-direction: row;\n    justify-content: center;\n    flex-wrap: wrap;\n    min-height: 300px;\n    max-width: 1000px;\n    margin: 0 auto;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 350px;\n  }\n"], ["\n  padding: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    flex-direction: row;\n    justify-content: center;\n    flex-wrap: wrap;\n    min-height: 300px;\n    max-width: 1000px;\n    margin: 0 auto;\n  }\n\n  @media (min-width: ", ") {\n    min-height: 350px;\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; });
var StyledBox = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  z-index: 1;\n\n  @media (min-width: ", ") {\n    flex: 2;\n  }\n"], ["\n  z-index: 1;\n\n  @media (min-width: ", ") {\n    flex: 2;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var IlloBox = styled(StyledBox)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  min-height: 100px;\n  max-width: 300px;\n  margin: ", " auto;\n\n  @media (min-width: ", ") {\n    flex: 1;\n    margin: ", ";\n    max-width: auto;\n  }\n"], ["\n  position: relative;\n  min-height: 100px;\n  max-width: 300px;\n  margin: ", " auto;\n\n  @media (min-width: ", ") {\n    flex: 1;\n    margin: ", ";\n    max-width: auto;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, space(3));
export default OnboardingPanel;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=onboardingPanel.jsx.map