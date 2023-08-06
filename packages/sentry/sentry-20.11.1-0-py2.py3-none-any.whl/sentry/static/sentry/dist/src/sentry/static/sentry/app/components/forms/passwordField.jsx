import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import InputField from 'app/components/forms/inputField';
import FormState from 'app/components/forms/state';
// TODO(dcramer): im not entirely sure this is working correctly with
// value propagation in all scenarios
var PasswordField = /** @class */ (function (_super) {
    __extends(PasswordField, _super);
    function PasswordField(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.cancelEdit = function (e) {
            e.preventDefault();
            _this.setState({
                editing: false,
            }, function () {
                _this.setValue('');
            });
        };
        _this.startEdit = function (e) {
            e.preventDefault();
            _this.setState({
                editing: true,
            });
        };
        _this.state = __assign(__assign({}, _this.state), { editing: false });
        return _this;
    }
    PasswordField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // close edit mode after successful save
        // TODO(dcramer): this needs to work with this.context.form
        if (this.props.formState &&
            this.props.formState === FormState.SAVING &&
            nextProps.formState === FormState.READY) {
            this.setState({
                editing: false,
            });
        }
    };
    PasswordField.prototype.getType = function () {
        return 'password';
    };
    PasswordField.prototype.getField = function () {
        if (!this.props.hasSavedValue) {
            return _super.prototype.getField.call(this);
        }
        if (this.state.editing) {
            return (<div className="form-password editing">
          <div>{_super.prototype.getField.call(this)}</div>
          <div>
            <a onClick={this.cancelEdit}>Cancel</a>
          </div>
        </div>);
        }
        else {
            return (<div className="form-password saved">
          <span>
            {this.props.prefix + new Array(21 - this.props.prefix.length).join('*')}
          </span>
          {!this.props.disabled && <a onClick={this.startEdit}>Edit</a>}
        </div>);
        }
    };
    PasswordField.propTypes = __assign(__assign({}, InputField.propTypes), { hasSavedValue: PropTypes.bool, prefix: PropTypes.string.isRequired });
    PasswordField.defaultProps = __assign(__assign({}, InputField.defaultProps), { hasSavedValue: false, prefix: '' });
    return PasswordField;
}(InputField));
export default PasswordField;
//# sourceMappingURL=passwordField.jsx.map