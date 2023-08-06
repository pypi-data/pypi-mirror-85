import Reflux from 'reflux';
import GroupStore from 'app/stores/groupStore';
var storeConfig = {
    records: {},
    init: function () {
        this.records = {};
        this.listenTo(GroupStore, this.onGroupChange, this.onGroupChange);
    },
    onGroupChange: function (itemIds) {
        this.prune();
        this.add(itemIds);
        this.trigger();
    },
    add: function (ids) {
        var _this = this;
        var allSelected = this.allSelected();
        ids.forEach(function (id) {
            if (!_this.records.hasOwnProperty(id)) {
                _this.records[id] = allSelected;
            }
        });
    },
    prune: function () {
        var existingIds = new Set(GroupStore.getAllItemIds());
        // Remove ids that no longer exist
        for (var itemId in this.records) {
            if (!existingIds.has(itemId)) {
                delete this.records[itemId];
            }
        }
    },
    allSelected: function () {
        var itemIds = this.getSelectedIds();
        var numRecords = this.numSelected();
        return itemIds.size > 0 && itemIds.size === numRecords;
    },
    numSelected: function () {
        return Object.keys(this.records).length;
    },
    anySelected: function () {
        var itemIds = this.getSelectedIds();
        return itemIds.size > 0;
    },
    multiSelected: function () {
        var itemIds = this.getSelectedIds();
        return itemIds.size > 1;
    },
    getSelectedIds: function () {
        var selected = new Set();
        for (var itemId in this.records) {
            if (this.records[itemId]) {
                selected.add(itemId);
            }
        }
        return selected;
    },
    isSelected: function (itemId) {
        return this.records[itemId] === true;
    },
    deselectAll: function () {
        for (var itemId in this.records) {
            this.records[itemId] = false;
        }
        this.trigger();
    },
    toggleSelect: function (itemId) {
        if (!this.records.hasOwnProperty(itemId)) {
            return;
        }
        this.records[itemId] = !this.records[itemId];
        this.trigger();
    },
    toggleSelectAll: function () {
        var allSelected = !this.allSelected();
        for (var itemId in this.records) {
            this.records[itemId] = allSelected;
        }
        this.trigger();
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=selectedGroupStore.jsx.map