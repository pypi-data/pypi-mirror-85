import { __assign, __extends, __read, __spread } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import FormField from 'app/components/forms/formField';
import Tooltip from 'app/components/tooltip';
import { IconQuestion } from 'app/icons';
import { defined } from 'app/utils';
var MultipleCheckboxField = /** @class */ (function (_super) {
    __extends(MultipleCheckboxField, _super);
    function MultipleCheckboxField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (e, _value) {
            var value = _value; // Casting here to allow _value to be optional, which it has to be since it's overloaded.
            var allValues = _this.state.values;
            if (e.target.checked) {
                if (allValues) {
                    allValues = __spread(allValues, [value]);
                }
                else {
                    allValues = [value];
                }
            }
            else {
                allValues = allValues.filter(function (v) { return v !== value; });
            }
            _this.setValues(allValues);
        };
        return _this;
    }
    MultipleCheckboxField.prototype.setValues = function (values) {
        var _this = this;
        var form = (this.context || {}).form;
        this.setState({
            values: values,
        }, function () {
            var finalValue = _this.coerceValue(_this.state.values);
            _this.props.onChange && _this.props.onChange(finalValue);
            form && form.onFieldChange(_this.props.name, finalValue);
        });
    };
    MultipleCheckboxField.prototype.render = function () {
        var _this = this;
        var _a = this.props, required = _a.required, className = _a.className, disabled = _a.disabled, disabledReason = _a.disabledReason, label = _a.label, help = _a.help, choices = _a.choices, hideLabelDivider = _a.hideLabelDivider, style = _a.style;
        var error = this.state.error;
        var cx = classNames(className, 'control-group', {
            'has-error': error,
        });
        // Hacky, but this isn't really a form label vs the checkbox labels, but
        // we want to treat it as one (i.e. for "required" indicator)
        var labelCx = classNames({
            required: required,
        });
        var shouldShowDisabledReason = disabled && disabledReason;
        return (<div style={style} className={cx}>
        <div className={labelCx}>
          <div className="controls">
            <label className="control-label" style={{
            display: 'block',
            marginBottom: !hideLabelDivider ? 10 : undefined,
            borderBottom: !hideLabelDivider ? '1px solid #f1eff3' : undefined,
        }}>
              {label}
              {shouldShowDisabledReason && (<Tooltip title={disabledReason}>
                  <span className="disabled-indicator">
                    <IconQuestion size="xs"/>
                  </span>
                </Tooltip>)}
            </label>
            {help && <p className="help-block">{help}</p>}
            {error && <p className="error">{error}</p>}
          </div>
        </div>

        <div className="control-list">
          {choices.map(function (_a) {
            var _b = __read(_a, 2), value = _b[0], choiceLabel = _b[1];
            return (<label className="checkbox" key={value}>
              <input type="checkbox" value={value} onChange={function (e) { return _this.onChange(e, value); }} disabled={disabled} checked={defined(_this.state.values) && _this.state.values.indexOf(value) !== -1}/>
              {choiceLabel}
            </label>);
        })}
        </div>
      </div>);
    };
    MultipleCheckboxField.propTypes = __assign(__assign({}, FormField.propTypes), { hideLabelDivider: PropTypes.bool, choices: PropTypes.array.isRequired });
    return MultipleCheckboxField;
}(FormField));
export default MultipleCheckboxField;
//# sourceMappingURL=multipleCheckboxField.jsx.map