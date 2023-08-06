import Reflux from 'reflux';
var DebugMetaActions = Reflux.createActions(['updateFilter']);
var storeConfig = {
    filter: null,
    init: function () {
        this.reset();
        this.listenTo(DebugMetaActions.updateFilter, this.updateFilter);
    },
    reset: function () {
        this.filter = null;
        this.trigger(this.get());
    },
    updateFilter: function (word) {
        this.filter = word;
        this.trigger(this.get());
    },
    get: function () {
        return {
            filter: this.filter,
        };
    },
};
var DebugMetaStore = Reflux.createStore(storeConfig);
export { DebugMetaActions, DebugMetaStore };
export default DebugMetaStore;
//# sourceMappingURL=debugMetaStore.jsx.map