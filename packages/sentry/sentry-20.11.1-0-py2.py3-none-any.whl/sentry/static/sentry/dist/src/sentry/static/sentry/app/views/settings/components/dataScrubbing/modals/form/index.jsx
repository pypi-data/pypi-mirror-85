import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import sortBy from 'lodash/sortBy';
import space from 'app/styles/space';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
import Button from 'app/components/button';
import { IconChevron } from 'app/icons';
import EventIdField from './eventIdField';
import SelectField from './selectField';
import SourceField from './sourceField';
import { getRuleLabel, getMethodLabel } from '../../utils';
import { MethodType, RuleType, } from '../../types';
var Form = /** @class */ (function (_super) {
    __extends(Form, _super);
    function Form() {
        var _a;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.state = { displayEventId: !!((_a = _this.props.eventId) === null || _a === void 0 ? void 0 : _a.value) };
        _this.handleChange = function (field) { return function (event) {
            _this.props.onChange(field, event.target.value);
        }; };
        _this.handleToggleEventId = function () {
            _this.setState(function (prevState) { return ({ displayEventId: !prevState.displayEventId }); });
        };
        return _this;
    }
    Form.prototype.render = function () {
        var _a = this.props, values = _a.values, onChange = _a.onChange, errors = _a.errors, onValidate = _a.onValidate, sourceSuggestions = _a.sourceSuggestions, onUpdateEventId = _a.onUpdateEventId, eventId = _a.eventId;
        var method = values.method, type = values.type, source = values.source;
        var displayEventId = this.state.displayEventId;
        return (<React.Fragment>
        <FieldGroup hasTwoColumns={values.method === MethodType.REPLACE}>
          <Field data-test-id="method-field" label={t('Method')} help={t('What to do')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <SelectField placeholder={t('Select method')} name="method" options={sortBy(Object.values(MethodType)).map(function (value) { return (__assign(__assign({}, getMethodLabel(value)), { value: value })); })} value={method} onChange={function (_a) {
            var value = _a.value;
            return onChange('method', value);
        }}/>
          </Field>
          {values.method === MethodType.REPLACE && (<Field data-test-id="placeholder-field" label={t('Custom Placeholder (Optional)')} help={t('It will replace the default placeholder [Filtered]')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
              <Input type="text" name="placeholder" placeholder={"[" + t('Filtered') + "]"} onChange={this.handleChange('placeholder')} value={values.placeholder}/>
            </Field>)}
        </FieldGroup>
        <FieldGroup hasTwoColumns={values.type === RuleType.PATTERN}>
          <Field data-test-id="type-field" label={t('Data Type')} help={t('What to look for. Use an existing pattern or define your own using regular expressions.')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <SelectField placeholder={t('Select type')} name="type" options={sortBy(Object.values(RuleType)).map(function (value) { return ({
            label: getRuleLabel(value),
            value: value,
        }); })} value={type} onChange={function (_a) {
            var value = _a.value;
            return onChange('type', value);
        }}/>
          </Field>
          {values.type === RuleType.PATTERN && (<Field data-test-id="regex-field" label={t('Regex matches')} help={t('Custom regular expression (see documentation)')} inline={false} error={errors === null || errors === void 0 ? void 0 : errors.pattern} flexibleControlStateSize stacked required showHelpInTooltip>
              <RegularExpression type="text" name="pattern" placeholder={t('[a-zA-Z0-9]+')} onChange={this.handleChange('pattern')} value={values.pattern} onBlur={onValidate('pattern')}/>
            </Field>)}
        </FieldGroup>
        <ToggleWrapper>
          {displayEventId ? (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {t('Hide event ID field')}
              <IconChevron direction="up" size="xs"/>
            </Toggle>) : (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {t('Use event ID for auto-completion')}
              <IconChevron direction="down" size="xs"/>
            </Toggle>)}
        </ToggleWrapper>
        <SourceGroup isExpanded={displayEventId}>
          {displayEventId && (<EventIdField onUpdateEventId={onUpdateEventId} eventId={eventId}/>)}
          <SourceField onChange={function (value) { return onChange('source', value); }} value={source} error={errors === null || errors === void 0 ? void 0 : errors.source} onBlur={onValidate('source')} isRegExMatchesSelected={type === RuleType.PATTERN} suggestions={sourceSuggestions}/>
        </SourceGroup>
      </React.Fragment>);
    };
    return Form;
}(React.Component));
export default Form;
var FieldGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    grid-gap: ", ";\n    ", "\n    margin-bottom: ", ";\n  }\n"], ["\n  display: grid;\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    grid-gap: ", ";\n    ", "\n    margin-bottom: ", ";\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, space(2), function (p) { return p.hasTwoColumns && "grid-template-columns: 1fr 1fr;"; }, function (p) { return (p.hasTwoColumns ? 0 : space(2)); });
var SourceGroup = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 65px;\n  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  transition-property: height;\n  ", "\n"], ["\n  height: 65px;\n  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  transition-property: height;\n  ",
    "\n"])), function (p) {
    return p.isExpanded &&
        "\n    border-radius: " + p.theme.borderRadius + ";\n    border: 1px solid " + p.theme.border + ";\n    box-shadow: " + p.theme.dropShadowLight + ";\n    margin: " + space(2) + " 0 " + space(3) + " 0;\n    padding: " + space(2) + ";\n    height: 180px;\n  ";
});
var RegularExpression = styled(Input)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var ToggleWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var Toggle = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n  > *:first-child {\n    display: grid;\n    grid-gap: ", ";\n    grid-template-columns: repeat(2, max-content);\n    align-items: center;\n  }\n"], ["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n  > *:first-child {\n    display: grid;\n    grid-gap: ", ";\n    grid-template-columns: repeat(2, max-content);\n    align-items: center;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; }, space(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map