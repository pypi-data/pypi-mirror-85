import Reflux from 'reflux';
import SentryAppComponentsActions from 'app/actions/sentryAppComponentActions';
var SentryAppComponentsStore = Reflux.createStore({
    init: function () {
        this.items = [];
        this.listenTo(SentryAppComponentsActions.loadComponents, this.onLoadComponents);
    },
    getInitialState: function () {
        return this.items;
    },
    onLoadComponents: function (items) {
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
    getComponentByType: function (type) {
        if (!type) {
            return this.getAll();
        }
        var items = this.items;
        return items.filter(function (item) { return item.type === type; });
    },
});
export default SentryAppComponentsStore;
//# sourceMappingURL=sentryAppComponentsStore.jsx.map