import { __assign, __read, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { IconClock, IconStar, IconTag, IconToggle, IconUser } from 'app/icons';
export function addSpace(query) {
    if (query === void 0) { query = ''; }
    if (query.length !== 0 && query[query.length - 1] !== ' ') {
        return query + ' ';
    }
    else {
        return query;
    }
}
export function removeSpace(query) {
    if (query === void 0) { query = ''; }
    if (query[query.length - 1] === ' ') {
        return query.slice(0, query.length - 1);
    }
    else {
        return query;
    }
}
function getTitleForType(type) {
    if (type === 'tag-value') {
        return t('Tag Values');
    }
    if (type === 'recent-search') {
        return t('Recent Searches');
    }
    if (type === 'default') {
        return t('Common Search Terms');
    }
    return t('Tags');
}
function getIconForTypeAndTag(type, tagName) {
    if (type === 'recent-search') {
        return <IconClock size="xs"/>;
    }
    if (type === 'default') {
        return <IconStar size="xs"/>;
    }
    // Change based on tagName and default to "icon-tag"
    switch (tagName) {
        case 'is':
            return <IconToggle size="xs"/>;
        case 'assigned':
        case 'bookmarks':
            return <IconUser size="xs"/>;
        case 'firstSeen':
        case 'lastSeen':
        case 'event.timestamp':
            return <IconClock size="xs"/>;
        default:
            return <IconTag size="xs"/>;
    }
}
export function createSearchGroups(searchItems, recentSearchItems, tagName, type, maxSearchItems) {
    var activeSearchItem = 0;
    if (maxSearchItems && maxSearchItems > 0) {
        searchItems = searchItems.slice(0, maxSearchItems);
    }
    var searchGroup = {
        title: getTitleForType(type),
        type: type === 'invalid-tag' ? type : 'header',
        icon: getIconForTypeAndTag(type, tagName),
        children: __spread(searchItems),
    };
    var recentSearchGroup = recentSearchItems && {
        title: t('Recent Searches'),
        type: 'header',
        icon: <IconClock size="xs"/>,
        children: __spread(recentSearchItems),
    };
    if (searchGroup.children && !!searchGroup.children.length) {
        searchGroup.children[activeSearchItem] = __assign({}, searchGroup.children[activeSearchItem]);
    }
    return {
        searchGroups: __spread([searchGroup], (recentSearchGroup ? [recentSearchGroup] : [])),
        flatSearchItems: __spread(searchItems, (recentSearchItems ? recentSearchItems : [])),
        activeSearchItem: -1,
    };
}
/**
 * Items is a list of dropdown groups that have a `children` field. Only the
 * `children` are selectable, so we need to find which child is selected given
 * an index that is in range of the sum of all `children` lengths
 *
 * @return Returns a tuple of [groupIndex, childrenIndex]
 */
export function filterSearchGroupsByIndex(items, index) {
    var _index = index;
    var foundSearchItem = [undefined, undefined];
    items.find(function (_a, i) {
        var children = _a.children;
        if (!children || !children.length) {
            return false;
        }
        if (_index < children.length) {
            foundSearchItem = [i, _index];
            return true;
        }
        _index -= children.length;
        return false;
    });
    return foundSearchItem;
}
//# sourceMappingURL=utils.jsx.map