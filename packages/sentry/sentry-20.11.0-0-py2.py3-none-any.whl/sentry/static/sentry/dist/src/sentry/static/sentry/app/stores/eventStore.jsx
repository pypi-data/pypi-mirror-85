import Reflux from 'reflux';
import isArray from 'lodash/isArray';
import extend from 'lodash/extend';
var storeConfig = {
    items: [],
    itemsById: {},
    init: function () {
        this.reset();
    },
    reset: function () {
        this.items = [];
    },
    loadInitialData: function (items) {
        var _this = this;
        this.reset();
        var itemIds = new Set();
        items.forEach(function (item) {
            itemIds.add(item.id);
            _this.items.push(item);
        });
        this.trigger(itemIds);
    },
    add: function (items) {
        var _this = this;
        if (!isArray(items)) {
            items = [items];
        }
        var itemsById = {};
        var itemIds = new Set();
        items.forEach(function (item) {
            itemsById[item.id] = item;
            itemIds.add(item.id);
        });
        items.forEach(function (item, idx) {
            if (itemsById[item.id]) {
                _this.items[idx] = extend(true, {}, item, itemsById[item.id]);
                delete itemsById[item.id];
            }
        });
        for (var itemId in itemsById) {
            this.items.push(itemsById[itemId]);
        }
        this.trigger(itemIds);
    },
    remove: function (itemId) {
        var _this = this;
        this.items.forEach(function (item, idx) {
            if (item.id === itemId) {
                _this.items.splice(idx, idx + 1);
            }
        });
        this.trigger(new Set([itemId]));
    },
    get: function (id) {
        for (var i = 0; i < this.items.length; i++) {
            if (this.items[i].id === id) {
                return this.items[i];
            }
        }
        return undefined;
    },
    getAllItemIds: function () {
        return this.items.map(function (item) { return item.id; });
    },
    getAllItems: function () {
        return this.items;
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=eventStore.jsx.map