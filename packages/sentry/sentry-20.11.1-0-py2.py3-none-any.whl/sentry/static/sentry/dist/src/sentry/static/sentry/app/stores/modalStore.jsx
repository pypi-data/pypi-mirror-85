import Reflux from 'reflux';
import ModalActions from 'app/actions/modalActions';
var ModalStore = Reflux.createStore({
    init: function () {
        this.reset();
        this.listenTo(ModalActions.closeModal, this.onCloseModal);
        this.listenTo(ModalActions.openModal, this.onOpenModal);
    },
    reset: function () {
        this.state = {
            renderer: null,
            options: {},
        };
    },
    onCloseModal: function () {
        var _a, _b;
        var onClose = (_b = (_a = this.state) === null || _a === void 0 ? void 0 : _a.options) === null || _b === void 0 ? void 0 : _b.onClose;
        // Trigger the options.onClose callback
        if (typeof onClose === 'function') {
            onClose();
        }
        this.reset();
        this.trigger(this.state);
    },
    onOpenModal: function (renderer, options) {
        this.state = { renderer: renderer, options: options };
        this.trigger(this.state);
    },
});
// TODO(ts): This should be properly typed
export default ModalStore;
//# sourceMappingURL=modalStore.jsx.map