import { __extends, __makeTemplateObject } from "tslib";
import { ClassNames, css } from '@emotion/core';
import React from 'react';
import styled from '@emotion/styled';
import Input from 'app/views/settings/components/forms/controls/input';
import { analytics } from 'app/utils/analytics';
import { t } from 'app/locale';
import Search from 'app/components/search';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
var CommandPalette = /** @class */ (function (_super) {
    __extends(CommandPalette, _super);
    function CommandPalette() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CommandPalette.prototype.componentDidMount = function () {
        analytics('omnisearch.open', {});
    };
    CommandPalette.prototype.render = function () {
        var Body = this.props.Body;
        return (<Body>
        <ClassNames>
          {function (_a) {
            var injectedCss = _a.css;
            return (<Search isOpen entryPoint="command_palette" minSearch={1} maxResults={10} dropdownStyle={injectedCss(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "], ["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "])), theme.border)} renderInput={function (_a) {
                var getInputProps = _a.getInputProps;
                return (<InputWrapper>
                  <StyledInput autoFocus {...getInputProps({
                    type: 'text',
                    placeholder: t('Search for projects, teams, settings, etc...'),
                })}/>
                </InputWrapper>);
            }}/>);
        }}
        </ClassNames>
      </Body>);
    };
    return CommandPalette;
}(React.Component));
export default CommandPalette;
export var modalCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  .modal-content {\n    padding: 0;\n  }\n"], ["\n  .modal-content {\n    padding: 0;\n  }\n"])));
var InputWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(0.25));
var StyledInput = styled(Input)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 100%;\n  padding: ", ";\n  border-radius: 8px;\n\n  outline: none;\n  border: none;\n  box-shadow: none;\n\n  :focus,\n  :active,\n  :hover {\n    outline: none;\n    border: none;\n    box-shadow: none;\n  }\n"], ["\n  width: 100%;\n  padding: ", ";\n  border-radius: 8px;\n\n  outline: none;\n  border: none;\n  box-shadow: none;\n\n  :focus,\n  :active,\n  :hover {\n    outline: none;\n    border: none;\n    box-shadow: none;\n  }\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=commandPalette.jsx.map