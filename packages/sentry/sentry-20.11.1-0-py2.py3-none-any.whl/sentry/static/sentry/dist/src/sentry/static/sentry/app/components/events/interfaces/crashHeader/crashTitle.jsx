import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Tooltip from 'app/components/tooltip';
var CrashTitle = function (_a) {
    var title = _a.title, newestFirst = _a.newestFirst, beforeTitle = _a.beforeTitle, _b = _a.hideGuide, hideGuide = _b === void 0 ? false : _b, onChange = _a.onChange;
    var handleToggleOrder = function () {
        if (onChange) {
            onChange({ newestFirst: !newestFirst });
        }
    };
    return (<Wrapper>
      {beforeTitle}
      <StyledH3>
        <GuideAnchor target="exception" disabled={hideGuide} position="bottom">
          {title}
        </GuideAnchor>
        <Tooltip title={t('Toggle stack trace order')}>
          <small>
            (
            <span onClick={handleToggleOrder}>
              {newestFirst ? t('most recent call first') : t('most recent call last')}
            </span>
            )
          </small>
        </Tooltip>
      </StyledH3>
    </Wrapper>);
};
export default CrashTitle;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-wrap: wrap;\n  flex-grow: 1;\n  justify-content: flex-start;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-wrap: wrap;\n  flex-grow: 1;\n  justify-content: flex-start;\n"])));
var StyledH3 = styled('h3')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n  max-width: 100%;\n  white-space: nowrap;\n"], ["\n  margin-bottom: 0;\n  max-width: 100%;\n  white-space: nowrap;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=crashTitle.jsx.map