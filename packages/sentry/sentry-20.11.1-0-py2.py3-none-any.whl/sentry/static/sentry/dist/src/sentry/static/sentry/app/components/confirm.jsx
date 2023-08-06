import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import Modal from 'react-bootstrap/lib/Modal';
import Button from 'app/components/button';
import { t } from 'app/locale';
var defaultProps = {
    /**
     * Button priority
     */
    priority: 'primary',
    /**
     * Disables the confirm button
     */
    disableConfirmButton: false,
    /**
     * Text to show in the cancel button
     */
    cancelText: t('Cancel'),
    /**
     * Text to show in the confirmation button
     */
    confirmText: t('Confirm'),
    // Stop event propagation when opening the confirm modal
    stopPropagation: false,
};
var Confirm = /** @class */ (function (_super) {
    __extends(Confirm, _super);
    function Confirm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isModalOpen: false,
            disableConfirmButton: _this.props.disableConfirmButton,
        };
        _this.confirming = false;
        _this.openModal = function () {
            var _a = _this.props, onConfirming = _a.onConfirming, disableConfirmButton = _a.disableConfirmButton;
            if (typeof onConfirming === 'function') {
                onConfirming();
            }
            _this.setState({
                isModalOpen: true,
                disableConfirmButton: disableConfirmButton || false,
            });
            // always reset `confirming` when modal visibility changes
            _this.confirming = false;
        };
        _this.closeModal = function () {
            var _a = _this.props, onCancel = _a.onCancel, disableConfirmButton = _a.disableConfirmButton;
            if (typeof onCancel === 'function') {
                onCancel();
            }
            _this.setState({
                isModalOpen: false,
                disableConfirmButton: disableConfirmButton || false,
            });
            // always reset `confirming` when modal visibility changes
            _this.confirming = false;
        };
        _this.handleConfirm = function () {
            // `confirming` is used to make sure `onConfirm` is only called once
            if (!_this.confirming) {
                _this.props.onConfirm();
            }
            // Close modal
            _this.setState({
                isModalOpen: false,
                disableConfirmButton: true,
            });
            _this.confirming = true;
        };
        _this.handleToggle = function (e) {
            var _a = _this.props, disabled = _a.disabled, bypass = _a.bypass, stopPropagation = _a.stopPropagation, onConfirm = _a.onConfirm;
            if (disabled) {
                return;
            }
            if (e && stopPropagation) {
                e.stopPropagation();
            }
            if (bypass) {
                onConfirm();
                return;
            }
            // Current state is closed, means it will toggle open
            if (!_this.state.isModalOpen) {
                _this.openModal();
            }
            else {
                _this.closeModal();
            }
        };
        return _this;
    }
    Confirm.getDerivedStateFromProps = function (props, state) {
        // Reset the state to handle prop changes from ConfirmDelete
        if (props.disableConfirmButton !== state.disableConfirmButton) {
            return {
                disableConfirmButton: props.disableConfirmButton,
            };
        }
        return null;
    };
    Confirm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, message = _a.message, renderMessage = _a.renderMessage, priority = _a.priority, confirmText = _a.confirmText, cancelText = _a.cancelText, children = _a.children, header = _a.header;
        var confirmMessage;
        if (typeof renderMessage === 'function') {
            confirmMessage = renderMessage({
                confirm: this.handleConfirm,
                close: this.handleToggle,
            });
        }
        else {
            confirmMessage = React.isValidElement(message) ? (message) : (<p>
          <strong>{message}</strong>
        </p>);
        }
        return (<React.Fragment>
        {typeof children === 'function'
            ? children({
                close: this.closeModal,
                open: this.openModal,
            })
            : React.isValidElement(children) &&
                React.cloneElement(children, {
                    disabled: disabled,
                    onClick: this.handleToggle,
                })}
        <Modal show={this.state.isModalOpen} animation={false} onHide={this.handleToggle}>
          {header && <div className="modal-header">{header}</div>}
          <div className="modal-body">{confirmMessage}</div>
          <div className="modal-footer">
            <Button style={{ marginRight: 10 }} onClick={this.handleToggle}>
              {cancelText}
            </Button>
            <Button data-test-id="confirm-button" disabled={this.state.disableConfirmButton} priority={priority} onClick={this.handleConfirm} autoFocus>
              {confirmText}
            </Button>
          </div>
        </Modal>
      </React.Fragment>);
    };
    Confirm.propTypes = {
        onConfirm: PropTypes.func.isRequired,
        confirmText: PropTypes.string.isRequired,
        cancelText: PropTypes.string.isRequired,
        priority: PropTypes.oneOf(['primary', 'danger']).isRequired,
        /**
         * If true, will skip the confirmation modal and call `onConfirm`
         */
        bypass: PropTypes.bool,
        message: PropTypes.node,
        /**
         * Renderer that passes:
         * `confirm`: Allows renderer to perform confirm action
         * `close`: Allows renderer to toggle confirm modal
         */
        renderMessage: PropTypes.func,
        disabled: PropTypes.bool,
        disableConfirmButton: PropTypes.bool,
        onConfirming: PropTypes.func,
        onCancel: PropTypes.func,
        header: PropTypes.node,
        // Stop event propagation when opening the confirm modal
        stopPropagation: PropTypes.bool,
    };
    Confirm.defaultProps = defaultProps;
    return Confirm;
}(React.PureComponent));
export default Confirm;
//# sourceMappingURL=confirm.jsx.map