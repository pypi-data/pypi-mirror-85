import { __extends } from "tslib";
import React from 'react';
import { defined } from 'app/utils';
import InputField from 'app/components/forms/inputField';
import Tooltip from 'app/components/tooltip';
import { IconQuestion } from 'app/icons';
var BooleanField = /** @class */ (function (_super) {
    __extends(BooleanField, _super);
    function BooleanField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (e) {
            var value = e.target.checked;
            _this.setValue(value);
        };
        return _this;
    }
    BooleanField.prototype.coerceValue = function (initialValue) {
        var value = _super.prototype.coerceValue.call(this, initialValue);
        return value ? true : false;
    };
    BooleanField.prototype.getField = function () {
        return (<input id={this.getId()} type={this.getType()} checked={this.state.value} onChange={this.onChange.bind(this)} disabled={this.props.disabled}/>);
    };
    BooleanField.prototype.render = function () {
        var error = this.state.error;
        var className = this.getClassName();
        if (error) {
            className += ' has-error';
        }
        return (<div className={className}>
        <div className="controls">
          <label className="control-label">
            {this.getField()}
            {this.props.label}
            {this.props.disabled && this.props.disabledReason && (<Tooltip title={this.props.disabledReason}>
                <IconQuestion size="xs"/>
              </Tooltip>)}
          </label>
          {defined(this.props.help) && <p className="help-block">{this.props.help}</p>}
          {error && <p className="error">{error}</p>}
        </div>
      </div>);
    };
    BooleanField.prototype.getClassName = function () {
        return 'control-group checkbox';
    };
    BooleanField.prototype.getType = function () {
        return 'checkbox';
    };
    return BooleanField;
}(InputField));
export default BooleanField;
//# sourceMappingURL=booleanField.jsx.map