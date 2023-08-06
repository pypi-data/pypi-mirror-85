import { __makeTemplateObject, __read, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import Radio from 'app/components/radio';
import space from 'app/styles/space';
var RadioGroup = function (_a) {
    var value = _a.value, disabled = _a.disabled, choices = _a.choices, label = _a.label, onChange = _a.onChange, orientInline = _a.orientInline, props = __rest(_a, ["value", "disabled", "choices", "label", "onChange", "orientInline"]);
    return (<Container orientInline={orientInline} {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(function (_a, index) {
        var _b = __read(_a, 3), id = _b[0], name = _b[1], description = _b[2];
        return (<RadioLineItem key={index} role="radio" index={index} aria-checked={value === id} disabled={disabled}>
        <Radio aria-label={id} disabled={disabled} checked={value === id} onChange={function (e) { return !disabled && onChange(id, e); }}/>
        <RadioLineText disabled={disabled}>{name}</RadioLineText>
        {description && (<React.Fragment>
            
            <div />
            <Description>{description}</Description>
          </React.Fragment>)}
      </RadioLineItem>);
    })}
  </Container>);
};
RadioGroup.propTypes = {
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    // TODO(ts): This is causing issues with ts
    choices: PropTypes.any.isRequired,
    disabled: PropTypes.bool,
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
};
var shouldForwardProp = function (p) { return !['disabled', 'animate'].includes(p) && isPropValid(p); };
export var RadioLineItem = styled('label', { shouldForwardProp: shouldForwardProp })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  cursor: ", ";\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"], ["\n  display: grid;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  cursor: ", ";\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"])), function (p) { return (p.disabled ? 'default' : 'pointer'); });
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: ", ";\n  grid-auto-rows: max-content;\n  grid-auto-columns: max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: ", ";\n  grid-auto-rows: max-content;\n  grid-auto-columns: max-content;\n"])), function (p) { return space(p.orientInline ? 3 : 1); }, function (p) { return (p.orientInline ? 'column' : 'row'); });
var RadioLineText = styled('div', { shouldForwardProp: shouldForwardProp })(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  opacity: ", ";\n"], ["\n  opacity: ", ";\n"])), function (p) { return (p.disabled ? 0.4 : null); });
var Description = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4em;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4em;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeRelativeSmall; });
export default RadioGroup;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=radioGroup.jsx.map