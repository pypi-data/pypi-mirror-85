import Reflux from 'reflux';
var memberListStoreConfig = {
    // listenables: MemberActions,
    loaded: false,
    state: [],
    init: function () {
        this.state = [];
        this.loaded = false;
    },
    // TODO(dcramer): this should actually come from an action of some sorts
    loadInitialData: function (items) {
        this.state = items;
        this.loaded = true;
        this.trigger(this.state, 'initial');
    },
    isLoaded: function () {
        return this.loaded;
    },
    getById: function (id) {
        if (!this.state) {
            return undefined;
        }
        id = '' + id;
        for (var i = 0; i < this.state.length; i++) {
            if (this.state[i].id === id) {
                return this.state[i];
            }
        }
        return undefined;
    },
    getByEmail: function (email) {
        if (!this.state) {
            return undefined;
        }
        email = email.toLowerCase();
        for (var i = 0; i < this.state.length; i++) {
            if (this.state[i].email.toLowerCase() === email) {
                return this.state[i];
            }
        }
        return undefined;
    },
    getAll: function () {
        return this.state;
    },
};
export default Reflux.createStore(memberListStoreConfig);
//# sourceMappingURL=memberListStore.jsx.map