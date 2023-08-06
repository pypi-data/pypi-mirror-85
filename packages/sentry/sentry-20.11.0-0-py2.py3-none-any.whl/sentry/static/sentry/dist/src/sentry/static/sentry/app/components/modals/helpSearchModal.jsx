import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { ClassNames, css } from '@emotion/core';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import HelpSearch from 'app/components/helpSearch';
import Hook from 'app/components/hook';
import space from 'app/styles/space';
var HelpSearchModal = function (_a) {
    var Body = _a.Body, closeModal = _a.closeModal, organization = _a.organization, _b = _a.placeholder, placeholder = _b === void 0 ? t('Search for documentation, FAQs, blog posts...') : _b, props = __rest(_a, ["Body", "closeModal", "organization", "placeholder"]);
    return (<Body>
    <ClassNames>
      {function (_a) {
        var injectedCss = _a.css;
        return (<HelpSearch {...props} entryPoint="sidebar_help" dropdownStyle={injectedCss(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "], ["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "])), theme.border)} renderInput={function (_a) {
            var getInputProps = _a.getInputProps;
            return (<InputWrapper>
              <Input autoFocus {...getInputProps({ type: 'text', placeholder: placeholder })}/>
            </InputWrapper>);
        }} resultFooter={<Hook name="help-modal:footer" {...{ organization: organization, closeModal: closeModal }}/>}/>);
    }}
    </ClassNames>
  </Body>);
};
var InputWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(0.25));
var Input = styled('input')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n  padding: ", ";\n  border: none;\n  border-radius: 8px;\n  outline: none;\n\n  &:focus {\n    outline: none;\n  }\n"], ["\n  width: 100%;\n  padding: ", ";\n  border: none;\n  border-radius: 8px;\n  outline: none;\n\n  &:focus {\n    outline: none;\n  }\n"])), space(1));
export var modalCss = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  .modal-content {\n    padding: 0;\n  }\n"], ["\n  .modal-content {\n    padding: 0;\n  }\n"])));
export default HelpSearchModal;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=helpSearchModal.jsx.map