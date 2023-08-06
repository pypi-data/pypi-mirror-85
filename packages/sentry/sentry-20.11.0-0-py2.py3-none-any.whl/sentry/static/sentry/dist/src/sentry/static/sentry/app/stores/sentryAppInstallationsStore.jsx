import Reflux from 'reflux';
var SentryAppInstallationStore = Reflux.createStore({
    init: function () {
        this.items = [];
    },
    getInitialState: function () {
        return this.items;
    },
    load: function (items) {
        this.items = items;
        this.trigger(items);
    },
    get: function (uuid) {
        var items = this.items;
        return items.find(function (item) { return item.uuid === uuid; });
    },
    getAll: function () {
        return this.items;
    },
});
export default SentryAppInstallationStore;
//# sourceMappingURL=sentryAppInstallationsStore.jsx.map