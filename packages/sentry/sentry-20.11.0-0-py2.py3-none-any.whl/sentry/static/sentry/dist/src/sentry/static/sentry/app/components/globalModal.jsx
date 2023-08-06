import { __extends } from "tslib";
import { ClassNames } from '@emotion/core';
import { browserHistory } from 'react-router';
import Modal from 'react-bootstrap/lib/Modal';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import { closeModal } from 'app/actionCreators/modal';
import Confirm from 'app/components/confirm';
import ModalStore from 'app/stores/modalStore';
var GlobalModal = /** @class */ (function (_super) {
    __extends(GlobalModal, _super);
    function GlobalModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCloseModal = function () {
            var _a = _this.props, options = _a.options, onClose = _a.onClose;
            // onClose callback for calling component
            if (typeof options.onClose === 'function') {
                options.onClose();
            }
            // Action creator
            closeModal();
            // Read description in propTypes
            if (typeof onClose === 'function') {
                onClose();
            }
        };
        return _this;
    }
    GlobalModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, visible = _a.visible, children = _a.children, options = _a.options;
        var renderedChild = typeof children === 'function'
            ? children({
                closeModal: closeModal,
                Header: Modal.Header,
                Body: Modal.Body,
                Footer: Modal.Footer,
            })
            : undefined;
        if (options && options.type === 'confirm') {
            return <Confirm onConfirm={function () { }}>{function () { return renderedChild; }}</Confirm>;
        }
        return (<ClassNames>
        {function (_a) {
            var css = _a.css, cx = _a.cx;
            return (<Modal className={cx(options === null || options === void 0 ? void 0 : options.modalClassName, (options === null || options === void 0 ? void 0 : options.modalCss) && css(options.modalCss))} dialogClassName={options && options.dialogClassName} show={visible} animation={false} onHide={_this.handleCloseModal}>
            {renderedChild}
          </Modal>);
        }}
      </ClassNames>);
    };
    GlobalModal.defaultProps = {
        visible: false,
        options: {},
    };
    return GlobalModal;
}(React.Component));
var GlobalModalContainer = createReactClass({
    displayName: 'GlobalModalContainer',
    mixins: [Reflux.connect(ModalStore, 'modalStore')],
    getInitialState: function () {
        return {
            modalStore: {},
            error: false,
            busy: false,
        };
    },
    componentDidMount: function () {
        // Listen for route changes so we can dismiss modal
        this.unlistenBrowserHistory = browserHistory.listen(function () { return closeModal(); });
    },
    componentWillUnmount: function () {
        if (this.unlistenBrowserHistory) {
            this.unlistenBrowserHistory();
        }
    },
    render: function () {
        var modalStore = this.state.modalStore;
        var visible = !!modalStore && typeof modalStore.renderer === 'function';
        return (<GlobalModal {...this.props} {...modalStore} visible={visible}>
        {visible ? modalStore.renderer : null}
      </GlobalModal>);
    },
});
export default GlobalModalContainer;
//# sourceMappingURL=globalModal.jsx.map