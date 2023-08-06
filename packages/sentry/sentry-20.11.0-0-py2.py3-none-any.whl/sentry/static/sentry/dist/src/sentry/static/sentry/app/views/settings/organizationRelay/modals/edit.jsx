import { __assign, __extends } from "tslib";
import { t } from 'app/locale';
import ModalManager from './modalManager';
var Edit = /** @class */ (function (_super) {
    __extends(Edit, _super);
    function Edit() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Edit.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { values: {
                name: this.props.relay.name,
                publicKey: this.props.relay.publicKey,
                description: this.props.relay.description || '',
            }, disables: { publicKey: true } });
    };
    Edit.prototype.getTitle = function () {
        return t('Edit Key');
    };
    Edit.prototype.getData = function () {
        var savedRelays = this.props.savedRelays;
        var updatedRelay = this.state.values;
        var trustedRelays = savedRelays.map(function (relay) {
            if (relay.publicKey === updatedRelay.publicKey) {
                return updatedRelay;
            }
            return relay;
        });
        return { trustedRelays: trustedRelays };
    };
    return Edit;
}(ModalManager));
export default Edit;
//# sourceMappingURL=edit.jsx.map