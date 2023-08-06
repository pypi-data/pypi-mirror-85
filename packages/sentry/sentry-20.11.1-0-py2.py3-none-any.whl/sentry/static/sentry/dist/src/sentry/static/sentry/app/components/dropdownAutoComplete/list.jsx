import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { AutoSizer, List as ReactVirtualizedList } from 'react-virtualized';
import Row from './row';
function getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight) {
    var minHeight = virtualizedLabelHeight
        ? items.reduce(function (a, r) { return a + (r.groupLabel ? virtualizedLabelHeight : virtualizedHeight); }, 0)
        : items.length * virtualizedHeight;
    return Math.min(minHeight, maxHeight);
}
var List = function (_a) {
    var virtualizedHeight = _a.virtualizedHeight, virtualizedLabelHeight = _a.virtualizedLabelHeight, onScroll = _a.onScroll, items = _a.items, itemSize = _a.itemSize, highlightedIndex = _a.highlightedIndex, inputValue = _a.inputValue, getItemProps = _a.getItemProps, maxHeight = _a.maxHeight;
    if (virtualizedHeight) {
        return (<AutoSizer disableHeight>
        {function (_a) {
            var width = _a.width;
            return (<StyledList width={width} height={getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight)} onScroll={onScroll} rowCount={items.length} rowHeight={function (_a) {
                var index = _a.index;
                return items[index].groupLabel && virtualizedLabelHeight
                    ? virtualizedLabelHeight
                    : virtualizedHeight;
            }} rowRenderer={function (_a) {
                var key = _a.key, index = _a.index, style = _a.style;
                return (<Row key={key} item={items[index]} style={style} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>);
            }}/>);
        }}
      </AutoSizer>);
    }
    return (<React.Fragment>
      {items.map(function (item, index) { return (<Row 
    // Using only the index of the row might not re-render properly,
    // because the items shift around the list
    key={item.value + "-" + index} item={item} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>); })}
    </React.Fragment>);
};
export default List;
var StyledList = styled(ReactVirtualizedList)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  outline: none;\n"], ["\n  outline: none;\n"])));
var templateObject_1;
//# sourceMappingURL=list.jsx.map