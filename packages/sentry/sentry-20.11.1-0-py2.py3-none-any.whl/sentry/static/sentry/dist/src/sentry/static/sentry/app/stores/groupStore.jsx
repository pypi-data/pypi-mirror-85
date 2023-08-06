import { __assign } from "tslib";
import isArray from 'lodash/isArray';
import isUndefined from 'lodash/isUndefined';
import Reflux from 'reflux';
import GroupActions from 'app/actions/groupActions';
import IndicatorStore from 'app/stores/indicatorStore';
import { t } from 'app/locale';
function showAlert(msg, type) {
    IndicatorStore.addMessage(msg, type, {
        duration: 4000,
    });
}
var PendingChangeQueue = /** @class */ (function () {
    function PendingChangeQueue() {
        this.changes = [];
    }
    PendingChangeQueue.prototype.getForItem = function (itemId) {
        return this.changes.filter(function (change) { return change[1] === itemId; });
    };
    PendingChangeQueue.prototype.push = function (changeId, itemId, data) {
        this.changes.push([changeId, itemId, data]);
    };
    PendingChangeQueue.prototype.remove = function (changeId, itemId) {
        this.changes = this.changes.filter(function (change) { return change[0] !== changeId || change[1] !== itemId; });
    };
    PendingChangeQueue.prototype.forEach = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        this.changes.forEach.apply(this.changes, args);
    };
    return PendingChangeQueue;
}());
var storeConfig = {
    listenables: [GroupActions],
    pendingChanges: new PendingChangeQueue(),
    items: [],
    statuses: {},
    init: function () {
        this.reset();
    },
    reset: function () {
        this.pendingChanges = new PendingChangeQueue();
        this.items = [];
        this.statuses = {};
    },
    // TODO(dcramer): this should actually come from an action of some sorts
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
        // See if any existing items are updated by this new set of items
        this.items.forEach(function (item, idx) {
            if (itemsById[item.id]) {
                _this.items[idx] = __assign(__assign({}, item), itemsById[item.id]);
                delete itemsById[item.id];
            }
        });
        // New items
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
    addStatus: function (id, status) {
        if (isUndefined(this.statuses[id])) {
            this.statuses[id] = {};
        }
        this.statuses[id][status] = true;
    },
    clearStatus: function (id, status) {
        if (isUndefined(this.statuses[id])) {
            return;
        }
        this.statuses[id][status] = false;
    },
    hasStatus: function (id, status) {
        if (isUndefined(this.statuses[id])) {
            return false;
        }
        return this.statuses[id][status] || false;
    },
    indexOfActivity: function (group_id, id) {
        var group = this.get(group_id);
        if (!group) {
            return -1;
        }
        for (var i = 0; i < group.activity.length; i++) {
            if (group.activity[i].id === id) {
                return i;
            }
        }
        return -1;
    },
    addActivity: function (id, data, index) {
        if (index === void 0) { index = -1; }
        var group = this.get(id);
        if (!group) {
            return;
        }
        // insert into beginning by default
        if (index === -1) {
            group.activity.unshift(data);
        }
        else {
            group.activity.splice(index, 0, data);
        }
        if (data.type === 'note') {
            group.numComments++;
        }
        this.trigger(new Set([id]));
    },
    updateActivity: function (group_id, id, data) {
        var group = this.get(group_id);
        if (!group) {
            return;
        }
        var index = this.indexOfActivity(group_id, id);
        if (index === -1) {
            return;
        }
        // Here, we want to merge the new `data` being passed in
        // into the existing `data` object. This effectively
        // allows passing in an object of only changes.
        group.activity[index].data = Object.assign(group.activity[index].data, data);
        this.trigger(new Set([group.id]));
    },
    removeActivity: function (group_id, id) {
        var group = this.get(group_id);
        if (!group) {
            return -1;
        }
        var index = this.indexOfActivity(group.id, id);
        if (index === -1) {
            return -1;
        }
        var activity = group.activity.splice(index, 1);
        if (activity[0].type === 'note') {
            group.numComments--;
        }
        this.trigger(new Set([group.id]));
        return index;
    },
    get: function (id) {
        // TODO(ts) This needs to be constrained further. It was left as any
        // because the PendingChanges signatures and this were not aligned.
        var pendingForId = [];
        this.pendingChanges.forEach(function (change) {
            if (change.id === id) {
                pendingForId.push(change);
            }
        });
        for (var i = 0; i < this.items.length; i++) {
            if (this.items[i].id === id) {
                var rItem = this.items[i];
                if (pendingForId.length) {
                    // copy the object so dirty state doesnt mutate original
                    rItem = __assign({}, rItem);
                    for (var c = 0; c < pendingForId.length; c++) {
                        rItem = __assign(__assign({}, rItem), pendingForId[c].params);
                    }
                }
                return rItem;
            }
        }
        return undefined;
    },
    getAllItemIds: function () {
        return this.items.map(function (item) { return item.id; });
    },
    getAllItems: function () {
        // regroup pending changes by their itemID
        var pendingById = {};
        this.pendingChanges.forEach(function (change) {
            if (isUndefined(pendingById[change.id])) {
                pendingById[change.id] = [];
            }
            pendingById[change.id].push(change);
        });
        return this.items.map(function (item) {
            var rItem = item;
            if (!isUndefined(pendingById[item.id])) {
                // copy the object so dirty state doesnt mutate original
                rItem = __assign({}, rItem);
                pendingById[item.id].forEach(function (change) {
                    rItem = __assign(__assign({}, rItem), change.params);
                });
            }
            return rItem;
        });
    },
    onAssignTo: function (_changeId, itemId, _data) {
        this.addStatus(itemId, 'assignTo');
        this.trigger(new Set([itemId]));
    },
    // TODO(dcramer): This is not really the best place for this
    onAssignToError: function (_changeId, itemId, _error) {
        this.clearStatus(itemId, 'assignTo');
        showAlert(t('Unable to change assignee. Please try again.'), 'error');
    },
    onAssignToSuccess: function (_changeId, itemId, response) {
        var item = this.get(itemId);
        if (!item) {
            return;
        }
        item.assignedTo = response.assignedTo;
        this.clearStatus(itemId, 'assignTo');
        this.trigger(new Set([itemId]));
    },
    onDelete: function (_changeId, itemIds) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        itemIds.forEach(function (itemId) {
            _this.addStatus(itemId, 'delete');
        });
        this.trigger(new Set(itemIds));
    },
    onDeleteError: function (_changeId, itemIds, _response) {
        var _this = this;
        showAlert(t('Unable to delete events. Please try again.'), 'error');
        if (!itemIds) {
            return;
        }
        itemIds.forEach(function (itemId) {
            _this.clearStatus(itemId, 'delete');
        });
        this.trigger(new Set(itemIds));
    },
    onDeleteSuccess: function (_changeId, itemIds, _response) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        var itemIdSet = new Set(itemIds);
        itemIds.forEach(function (itemId) {
            delete _this.statuses[itemId];
            _this.clearStatus(itemId, 'delete');
        });
        this.items = this.items.filter(function (item) { return !itemIdSet.has(item.id); });
        showAlert(t('The selected events have been scheduled for deletion.'), 'success');
        this.trigger(new Set(itemIds));
    },
    onDiscard: function (_changeId, itemId) {
        this.addStatus(itemId, 'discard');
        this.trigger(new Set([itemId]));
    },
    onDiscardError: function (_changeId, itemId, _response) {
        this.clearStatus(itemId, 'discard');
        showAlert(t('Unable to discard event. Please try again.'), 'error');
        this.trigger(new Set([itemId]));
    },
    onDiscardSuccess: function (_changeId, itemId, _response) {
        delete this.statuses[itemId];
        this.clearStatus(itemId, 'discard');
        this.items = this.items.filter(function (item) { return item.id !== itemId; });
        showAlert(t('Similar events will be filtered and discarded.'), 'success');
        this.trigger(new Set([itemId]));
    },
    onMerge: function (_changeId, itemIds) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        itemIds.forEach(function (itemId) {
            _this.addStatus(itemId, 'merge');
        });
        // XXX(billy): Not sure if this is a bug or not but do we need to publish all itemIds?
        // Seems like we only need to publish parent id
        this.trigger(new Set(itemIds));
    },
    onMergeError: function (_changeId, itemIds, _response) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        itemIds.forEach(function (itemId) {
            _this.clearStatus(itemId, 'merge');
        });
        showAlert(t('Unable to merge events. Please try again.'), 'error');
        this.trigger(new Set(itemIds));
    },
    onMergeSuccess: function (_changeId, mergedIds, response) {
        var _this = this;
        mergedIds = this._itemIdsOrAll(mergedIds); // everything on page
        mergedIds.forEach(function (itemId) {
            _this.clearStatus(itemId, 'merge');
        });
        // Remove all but parent id (items were merged into this one)
        var mergedIdSet = new Set(mergedIds);
        // Looks like the `PUT /api/0/projects/:orgId/:projectId/issues/` endpoint
        // actually returns a 204, so there is no `response` body
        this.items = this.items.filter(function (item) {
            return !mergedIdSet.has(item.id) ||
                (response && response.merge && item.id === response.merge.parent);
        });
        showAlert(t('The selected events have been scheduled for merge.'), 'success');
        this.trigger(new Set(mergedIds));
    },
    /**
     * If itemIds is undefined, returns all ids in the store
     */
    _itemIdsOrAll: function (itemIds) {
        if (isUndefined(itemIds)) {
            itemIds = this.items.map(function (item) { return item.id; });
        }
        return itemIds;
    },
    onUpdate: function (changeId, itemIds, data) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        itemIds.forEach(function (itemId) {
            _this.addStatus(itemId, 'update');
            _this.pendingChanges.push(changeId, itemId, data);
        });
        this.trigger(new Set(itemIds));
    },
    onUpdateError: function (changeId, itemIds, _error, failSilently) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        this.pendingChanges.remove(changeId);
        itemIds.forEach(function (itemId) {
            _this.clearStatus(itemId, 'update');
        });
        if (!failSilently) {
            showAlert(t('Unable to update events. Please try again.'), 'error');
        }
        this.trigger(new Set(itemIds));
    },
    onUpdateSuccess: function (changeId, itemIds, response) {
        var _this = this;
        itemIds = this._itemIdsOrAll(itemIds);
        this.items.forEach(function (item, idx) {
            if (itemIds.indexOf(item.id) !== -1) {
                _this.items[idx] = __assign(__assign({}, item), response);
                _this.clearStatus(item.id, 'update');
            }
        });
        this.pendingChanges.remove(changeId);
        this.trigger(new Set(itemIds));
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=groupStore.jsx.map