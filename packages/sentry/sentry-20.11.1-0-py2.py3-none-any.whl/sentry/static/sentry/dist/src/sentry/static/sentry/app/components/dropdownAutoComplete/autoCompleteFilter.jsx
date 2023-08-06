import { __assign, __read, __spread } from "tslib";
import flatMap from 'lodash/flatMap';
function hasRootGroup(items) {
    var _a;
    return !!((_a = items[0]) === null || _a === void 0 ? void 0 : _a.items);
}
function filterItems(items, inputValue) {
    return items.filter(function (item) {
        return (item.searchKey || item.value + " " + item.label)
            .toLowerCase()
            .indexOf(inputValue.toLowerCase()) > -1;
    });
}
function filterGroupedItems(groups, inputValue) {
    return groups
        .map(function (group) { return (__assign(__assign({}, group), { items: filterItems(group.items, inputValue) })); })
        .filter(function (group) { return group.items.length > 0; });
}
function autoCompleteFilter(items, inputValue) {
    var itemCount = 0;
    if (!items) {
        return [];
    }
    if (hasRootGroup(items)) {
        //if the first item has children, we assume it is a group
        return flatMap(filterGroupedItems(items, inputValue), function (item) {
            var groupItems = item.items.map(function (groupedItem) { return (__assign(__assign({}, groupedItem), { index: itemCount++ })); });
            // Make sure we don't add the group label to list of items
            // if we try to hide it, otherwise it will render if the list
            // is using virtualized rows (because of fixed row heights)
            if (item.hideGroupLabel) {
                return groupItems;
            }
            return __spread([__assign(__assign({}, item), { groupLabel: true })], groupItems);
        });
    }
    return filterItems(items, inputValue).map(function (item, index) { return (__assign(__assign({}, item), { index: index })); });
}
export default autoCompleteFilter;
//# sourceMappingURL=autoCompleteFilter.jsx.map