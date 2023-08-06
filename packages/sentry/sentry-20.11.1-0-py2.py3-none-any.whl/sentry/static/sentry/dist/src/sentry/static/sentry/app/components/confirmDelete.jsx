import { __extends } from "tslib";
import React from 'react';
import Confirm from 'app/components/confirm';
import Alert from 'app/components/alert';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
import { t } from 'app/locale';
var defaultProps = {
    priority: 'primary',
    cancelText: t('Cancel'),
    confirmText: t('Confirm'),
};
var ConfirmDelete = /** @class */ (function (_super) {
    __extends(ConfirmDelete, _super);
    function ConfirmDelete() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            disableConfirmButton: true,
            confirmInput: '',
        };
        _this.handleChange = function (evt) {
            var input = evt.target.value;
            if (input === _this.props.confirmInput) {
                _this.setState({ disableConfirmButton: false, confirmInput: input });
            }
            else {
                _this.setState({ disableConfirmButton: true, confirmInput: input });
            }
        };
        _this.renderConfirmMessage = function () {
            var _a = _this.props, message = _a.message, confirmInput = _a.confirmInput;
            return (<React.Fragment>
        <Alert type="error">{message}</Alert>
        <Field flexibleControlStateSize inline={false} label={t('Please enter %s to confirm the deletion', <code>{confirmInput}</code>)}>
          <Input type="text" placeholder={confirmInput} onChange={_this.handleChange} value={_this.state.confirmInput}/>
        </Field>
      </React.Fragment>);
        };
        return _this;
    }
    ConfirmDelete.prototype.render = function () {
        var disableConfirmButton = this.state.disableConfirmButton;
        return (<Confirm {...this.props} bypass={false} disableConfirmButton={disableConfirmButton} message={this.renderConfirmMessage()}/>);
    };
    ConfirmDelete.defaultProps = defaultProps;
    return ConfirmDelete;
}(React.PureComponent));
export default ConfirmDelete;
//# sourceMappingURL=confirmDelete.jsx.map