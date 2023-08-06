import { __assign, __read, __spread } from "tslib";
import Reflux from 'reflux';
import OrganizationsActions from 'app/actions/organizationsActions';
var organizationsStoreConfig = {
    listenables: [OrganizationsActions],
    state: [],
    loaded: false,
    // So we can use Reflux.connect in a component mixin
    getInitialState: function () {
        return this.state;
    },
    init: function () {
        this.state = [];
        this.loaded = false;
    },
    onUpdate: function (org) {
        this.add(org);
    },
    onChangeSlug: function (prev, next) {
        if (prev.slug === next.slug) {
            return;
        }
        this.remove(prev.slug);
        this.add(next);
    },
    onRemoveSuccess: function (slug) {
        this.remove(slug);
    },
    get: function (slug) {
        return this.state.find(function (item) { return item.slug === slug; });
    },
    getAll: function () {
        return this.state;
    },
    remove: function (slug) {
        this.state = this.state.filter(function (item) { return slug !== item.slug; });
        this.trigger(this.state);
    },
    add: function (item) {
        var _this = this;
        var match = false;
        this.state.forEach(function (existing, idx) {
            if (existing.id === item.id) {
                item = __assign(__assign({}, existing), item);
                _this.state[idx] = item;
                match = true;
            }
        });
        if (!match) {
            this.state = __spread(this.state, [item]);
        }
        this.trigger(this.state);
    },
    load: function (items) {
        this.state = items;
        this.loaded = true;
        this.trigger(items);
    },
};
export default Reflux.createStore(organizationsStoreConfig);
//# sourceMappingURL=organizationsStore.jsx.map