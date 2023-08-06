import { __read, __spread } from "tslib";
var removeFromList = function (item, list) {
    var idx = list.indexOf(item);
    if (idx !== -1) {
        list.splice(idx, 1);
    }
};
var StreamManager = /** @class */ (function () {
    // TODO(dcramer): this should listen to changes on GroupStore and remove
    // items that are removed there
    // TODO(ts) Add better typing for store. Generally this is GroupStore, but it could be other things.
    function StreamManager(store, options) {
        if (options === void 0) { options = {}; }
        this.idList = [];
        this.idList = [];
        this.store = store;
        this.limit = options.limit || 1000;
    }
    StreamManager.prototype.trim = function () {
        var excess = this.idList.splice(this.limit, this.idList.length - this.limit);
        excess.forEach(this.store.remove);
    };
    StreamManager.prototype.push = function (items) {
        var _this = this;
        if (items === void 0) { items = []; }
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return this;
        }
        items = items.filter(function (item) { return item.hasOwnProperty('id'); });
        items.forEach(function (item) { return removeFromList(item.id, _this.idList); });
        var ids = items.map(function (item) { return item.id; });
        this.idList = __spread(this.idList, ids);
        this.trim();
        this.store.add(items);
        return this;
    };
    StreamManager.prototype.getAllItems = function () {
        var _this = this;
        return this.store
            .getAllItems()
            .slice()
            .sort(function (a, b) { return _this.idList.indexOf(a.id) - _this.idList.indexOf(b.id); });
    };
    StreamManager.prototype.unshift = function (items) {
        var _this = this;
        if (items === void 0) { items = []; }
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return this;
        }
        items.forEach(function (item) { return removeFromList(item.id, _this.idList); });
        var ids = items.map(function (item) { return item.id; });
        this.idList = __spread(ids, this.idList);
        this.trim();
        this.store.add(items);
        return this;
    };
    return StreamManager;
}());
export default StreamManager;
//# sourceMappingURL=streamManager.jsx.map