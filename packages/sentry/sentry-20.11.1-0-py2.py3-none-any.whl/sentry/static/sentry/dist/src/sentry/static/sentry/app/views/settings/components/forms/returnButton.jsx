import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconReturn } from 'app/icons/iconReturn';
import Tooltip from 'app/components/tooltip';
var SubmitButton = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: transparent;\n  box-shadow: none;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: 0.2s all;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 1.4em;\n  width: 1.4em;\n"], ["\n  background: transparent;\n  box-shadow: none;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: 0.2s all;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 1.4em;\n  width: 1.4em;\n"])), function (p) { return p.theme.borderRadius; });
var ClickTargetStyled = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 100%;\n  width: 25%;\n  max-width: 2.5em;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n\n  &:hover ", " {\n    background: ", ";\n    box-shadow: ", ";\n    border: 1px solid ", ";\n  }\n"], ["\n  height: 100%;\n  width: 25%;\n  max-width: 2.5em;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n\n  &:hover ", " {\n    background: ", ";\n    box-shadow: ", ";\n    border: 1px solid ", ";\n  }\n"])), SubmitButton, function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; });
var ReturnButton = function (props) { return (<ClickTargetStyled {...props}>
    <Tooltip title={t('Save')}>
      <SubmitButton>
        <IconReturn />
      </SubmitButton>
    </Tooltip>
  </ClickTargetStyled>); };
export default ReturnButton;
var templateObject_1, templateObject_2;
//# sourceMappingURL=returnButton.jsx.map