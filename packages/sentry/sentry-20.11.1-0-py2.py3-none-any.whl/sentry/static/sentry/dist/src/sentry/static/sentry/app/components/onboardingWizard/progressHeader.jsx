import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import ProgressRing from 'app/components/progressRing';
import space from 'app/styles/space';
var ProgressHeader = function (_a) {
    var allTasks = _a.allTasks, completedTasks = _a.completedTasks;
    return (<Container>
    <ProgressRing size={88} barWidth={12} text={allTasks.length - completedTasks.length} animateText value={(completedTasks.length / allTasks.length) * 100} progressEndcaps="round" backgroundColor={theme.gray200} textCss={function () { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        font-size: 26px;\n        color: ", ";\n      "], ["\n        font-size: 26px;\n        color: ", ";\n      "])), theme.gray300); }}/>
    <HeadingText>
      <h4>{t('Setup Sentry')}</h4>
      <p>{t('Complete these tasks to take full advantage of Sentry in your project')}</p>
    </HeadingText>
  </Container>);
};
export default ProgressHeader;
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  padding: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  padding: ", ";\n  align-items: center;\n"])), space(2), space(4));
var HeadingText = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  h4 {\n    font-weight: normal;\n    margin-bottom: ", ";\n  }\n\n  p {\n    color: ", ";\n    margin: 0;\n    line-height: 2rem;\n  }\n"], ["\n  h4 {\n    font-weight: normal;\n    margin-bottom: ", ";\n  }\n\n  p {\n    color: ", ";\n    margin: 0;\n    line-height: 2rem;\n  }\n"])), space(1), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=progressHeader.jsx.map