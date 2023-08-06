import { __decorate, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import keydown from 'react-keydown';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconSearch } from 'app/icons';
import Search from 'app/components/search';
var MIN_SEARCH_LENGTH = 1;
var MAX_RESULTS = 10;
var SettingsSearch = /** @class */ (function (_super) {
    __extends(SettingsSearch, _super);
    function SettingsSearch() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.searchInput = React.createRef();
        return _this;
    }
    SettingsSearch.prototype.handleFocusSearch = function (e) {
        if (!this.searchInput.current) {
            return;
        }
        if (e.target === this.searchInput.current) {
            return;
        }
        e.preventDefault();
        this.searchInput.current.focus();
    };
    SettingsSearch.prototype.render = function () {
        var _this = this;
        return (<Search {...this.props} entryPoint="settings_search" minSearch={MIN_SEARCH_LENGTH} maxResults={MAX_RESULTS} renderInput={function (_a) {
            var getInputProps = _a.getInputProps;
            return (<SearchInputWrapper>
            <SearchInputIcon size="14px"/>
            <SearchInput {...getInputProps({
                type: 'text',
                placeholder: t('Search'),
            })} ref={_this.searchInput}/>
          </SearchInputWrapper>);
        }}/>);
    };
    __decorate([
        keydown('/')
    ], SettingsSearch.prototype, "handleFocusSearch", null);
    return SettingsSearch;
}(React.Component));
// This is so we can use this as a selector for emotion
var StyledSettingsSearch = styled(SettingsSearch)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
export default StyledSettingsSearch;
export { SettingsSearch };
var SearchInputWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var SearchInputIcon = styled(IconSearch)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  position: absolute;\n  left: 10px;\n  top: 8px;\n"], ["\n  color: ", ";\n  position: absolute;\n  left: 10px;\n  top: 8px;\n"])), function (p) { return p.theme.gray300; });
var SearchInput = styled('input')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  transition: border-color 0.15s ease;\n  font-size: 14px;\n  width: 260px;\n  line-height: 1;\n  padding: 5px 8px 4px 28px;\n  border: 1px solid ", ";\n  border-radius: 30px;\n  height: 28px;\n\n  box-shadow: inset ", ";\n\n  &:focus {\n    outline: none;\n    border: 1px solid ", ";\n  }\n\n  &::placeholder {\n    color: ", ";\n  }\n"], ["\n  transition: border-color 0.15s ease;\n  font-size: 14px;\n  width: 260px;\n  line-height: 1;\n  padding: 5px 8px 4px 28px;\n  border: 1px solid ", ";\n  border-radius: 30px;\n  height: 28px;\n\n  box-shadow: inset ", ";\n\n  &:focus {\n    outline: none;\n    border: 1px solid ", ";\n  }\n\n  &::placeholder {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; }, function (p) { return p.theme.formPlaceholder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map