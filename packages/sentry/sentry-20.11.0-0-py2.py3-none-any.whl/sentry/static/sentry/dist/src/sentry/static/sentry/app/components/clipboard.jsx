import { __extends } from "tslib";
import Clip from 'clipboard';
import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
var Clipboard = /** @class */ (function (_super) {
    __extends(Clipboard, _super);
    function Clipboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleMount = function (ref) {
            if (!ref) {
                return;
            }
            var _a = _this.props, hideMessages = _a.hideMessages, successMessage = _a.successMessage, errorMessage = _a.errorMessage, onSuccess = _a.onSuccess, onError = _a.onError;
            var hasSuccessCb = typeof onSuccess === 'function';
            var hasErrorCb = typeof onError === 'function';
            var bindEventHandlers = !hideMessages || hasSuccessCb || hasErrorCb;
            // eslint-disable-next-line react/no-find-dom-node
            _this.clipboard = new Clip(ReactDOM.findDOMNode(ref), {
                text: function () { return _this.props.value; },
            });
            if (!bindEventHandlers) {
                return;
            }
            _this.clipboard
                .on('success', function () {
                if (!hideMessages) {
                    addSuccessMessage(successMessage);
                }
                if (onSuccess && hasSuccessCb) {
                    onSuccess();
                }
            })
                .on('error', function () {
                if (!hideMessages) {
                    addErrorMessage(errorMessage);
                }
                if (onError && hasErrorCb) {
                    onError();
                }
            });
        };
        return _this;
    }
    Clipboard.prototype.componentWillUnmount = function () {
        if (this.clipboard) {
            this.clipboard.destroy();
        }
    };
    Clipboard.prototype.render = function () {
        var _a = this.props, children = _a.children, hideUnsupported = _a.hideUnsupported;
        // Browser doesn't support `execCommand`
        if (hideUnsupported && !Clip.isSupported()) {
            return null;
        }
        if (!React.isValidElement(children)) {
            return null;
        }
        return React.cloneElement(children, {
            ref: this.handleMount,
        });
    };
    Clipboard.propTypes = {
        value: PropTypes.string,
        successMessage: PropTypes.string,
        errorMessage: PropTypes.string,
        hideMessages: PropTypes.bool,
        /**
         * Hide component if browser does not support "execCommand"
         */
        hideUnsupported: PropTypes.bool,
        onSuccess: PropTypes.func,
        onError: PropTypes.func,
    };
    Clipboard.defaultProps = {
        hideMessages: false,
        successMessage: 'Copied to clipboard',
        errorMessage: 'Error copying to clipboard',
    };
    return Clipboard;
}(React.Component));
export default Clipboard;
//# sourceMappingURL=clipboard.jsx.map