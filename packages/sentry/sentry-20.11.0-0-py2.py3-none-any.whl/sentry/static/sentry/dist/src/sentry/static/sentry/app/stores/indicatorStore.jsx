import { __assign, __read, __rest, __spread } from "tslib";
import Reflux from 'reflux';
import { t } from 'app/locale';
import IndicatorActions from 'app/actions/indicatorActions';
var storeConfig = {
    items: [],
    lastId: 0,
    init: function () {
        this.items = [];
        this.lastId = 0;
        this.listenTo(IndicatorActions.append, this.append);
        this.listenTo(IndicatorActions.replace, this.add);
        this.listenTo(IndicatorActions.remove, this.remove);
        this.listenTo(IndicatorActions.clear, this.clear);
    },
    addSuccess: function (message) {
        return this.add(message, 'success', { duration: 2000 });
    },
    addError: function (message) {
        if (message === void 0) { message = t('An error occurred'); }
        return this.add(message, 'error', { duration: 2000 });
    },
    addMessage: function (message, type, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var append = _a.append, options = __rest(_a, ["append"]);
        var indicator = {
            id: this.lastId++,
            message: message,
            type: type,
            options: options,
            clearId: null,
        };
        if (options.duration) {
            indicator.clearId = window.setTimeout(function () {
                _this.remove(indicator);
            }, options.duration);
        }
        var newItems = append ? __spread(this.items, [indicator]) : [indicator];
        this.items = newItems;
        this.trigger(this.items);
        return indicator;
    },
    append: function (message, type, options) {
        return this.addMessage(message, type, __assign(__assign({}, options), { append: true }));
    },
    add: function (message, type, options) {
        if (type === void 0) { type = 'loading'; }
        if (options === void 0) { options = {}; }
        return this.addMessage(message, type, __assign(__assign({}, options), { append: false }));
    },
    clear: function () {
        this.items = [];
        this.trigger(this.items);
    },
    remove: function (indicator) {
        if (!indicator) {
            return;
        }
        this.items = this.items.filter(function (item) { return item !== indicator; });
        if (indicator.clearId) {
            window.clearTimeout(indicator.clearId);
            indicator.clearId = null;
        }
        this.trigger(this.items);
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=indicatorStore.jsx.map