import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
// eslint import checks can't find types in the flow code.
// eslint-disable-next-line import/named
import { components } from 'react-select';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
var SelectField = /** @class */ (function (_super) {
    __extends(SelectField, _super);
    function SelectField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.selectRef = React.createRef();
        return _this;
    }
    SelectField.prototype.componentDidMount = function () {
        var _a, _b;
        if (!this.selectRef.current) {
            return;
        }
        if ((_b = (_a = this.selectRef.current) === null || _a === void 0 ? void 0 : _a.select) === null || _b === void 0 ? void 0 : _b.inputRef) {
            this.selectRef.current.select.inputRef.autocomplete = 'off';
        }
    };
    SelectField.prototype.render = function () {
        return (<SelectControl {...this.props} isSearchable={false} styles={{
            control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '41px', height: '41px' })); },
        }} ref={this.selectRef} components={{
            Option: function (_a) {
                var _b = _a.data, label = _b.label, description = _b.description, data = __rest(_b, ["label", "description"]), isSelected = _a.isSelected, props = __rest(_a, ["data", "isSelected"]);
                return (<components.Option isSelected={isSelected} data={data} {...props}>
              <Wrapper isSelected={isSelected}>
                <div data-test-id="label">{label}</div>
                {description && <Description>{"(" + description + ")"}</Description>}
              </Wrapper>
            </components.Option>);
            },
        }} openOnFocus/>);
    };
    return SelectField;
}(React.Component));
export default SelectField;
var Description = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  grid-gap: ", ";\n  ", "\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  grid-gap: ", ";\n  ",
    "\n"])), space(1), function (p) {
    return p.isSelected &&
        "\n      " + Description + " {\n        :not(:hover) {\n          color: " + p.theme.white + ";\n        }\n      }\n    ";
});
var templateObject_1, templateObject_2;
//# sourceMappingURL=selectField.jsx.map