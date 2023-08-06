import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { List, CellMeasurer, CellMeasurerCache, AutoSizer, } from 'react-virtualized';
import isEqual from 'lodash/isEqual';
import { aroundContentStyle } from './styles';
import ListHeader from './listHeader';
import ListBody from './listBody';
var LIST_MAX_HEIGHT = 400;
var cache = new CellMeasurerCache({
    fixedWidth: true,
    minHeight: 42,
});
var ListContainer = /** @class */ (function (_super) {
    __extends(ListContainer, _super);
    function ListContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            scrollToIndex: _this.props.breadcrumbs.length - 1,
        };
        _this.listRef = null;
        _this.updateGrid = function () {
            if (_this.listRef) {
                cache.clearAll();
                _this.listRef.forceUpdateGrid();
            }
        };
        _this.setScrollbarSize = function (_a) {
            var size = _a.size;
            _this.setState({ scrollbarSize: size });
        };
        _this.renderRow = function (_a) {
            var index = _a.index, key = _a.key, parent = _a.parent, style = _a.style;
            var breadcrumbs = _this.props.breadcrumbs;
            var breadcrumb = breadcrumbs[index];
            var isLastItem = breadcrumbs[breadcrumbs.length - 1].id === breadcrumb.id;
            return (<CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        {function (_a) {
                var measure = _a.measure;
                return isLastItem ? (<Row style={style} onLoad={measure} data-test-id="last-crumb">
              {_this.renderBody(breadcrumb, isLastItem)}
            </Row>) : (<Row style={style} onLoad={measure}>
              {_this.renderBody(breadcrumb)}
            </Row>);
            }}
      </CellMeasurer>);
        };
        return _this;
    }
    ListContainer.prototype.componentDidMount = function () {
        this.updateGrid();
    };
    ListContainer.prototype.componentDidUpdate = function (prevProps) {
        this.updateGrid();
        if (!isEqual(prevProps.breadcrumbs, this.props.breadcrumbs) &&
            !this.state.scrollToIndex) {
            this.setScrollToIndex(undefined);
        }
    };
    ListContainer.prototype.setScrollToIndex = function (scrollToIndex) {
        this.setState({ scrollToIndex: scrollToIndex });
    };
    ListContainer.prototype.renderBody = function (breadcrumb, isLastItem) {
        if (isLastItem === void 0) { isLastItem = false; }
        var _a = this.props, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm, relativeTime = _a.relativeTime, displayRelativeTime = _a.displayRelativeTime;
        return (<ListBody orgId={orgId} searchTerm={searchTerm} breadcrumb={breadcrumb} event={event} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} isLastItem={isLastItem}/>);
    };
    ListContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, breadcrumbs = _a.breadcrumbs, displayRelativeTime = _a.displayRelativeTime, onSwitchTimeFormat = _a.onSwitchTimeFormat;
        var _b = this.state, scrollToIndex = _b.scrollToIndex, scrollbarSize = _b.scrollbarSize;
        // onResize is required in case the user rotates the device.
        return (<Wrapper>
        <AutoSizer disableHeight onResize={this.updateGrid}>
          {function (_a) {
            var width = _a.width;
            return (<React.Fragment>
              <RowSticky width={width} scrollbarSize={scrollbarSize}>
                <ListHeader displayRelativeTime={!!displayRelativeTime} onSwitchTimeFormat={onSwitchTimeFormat}/>
              </RowSticky>
              <StyledList ref={function (el) {
                _this.listRef = el;
            }} deferredMeasurementCache={cache} height={LIST_MAX_HEIGHT} overscanRowCount={5} rowCount={breadcrumbs.length} rowHeight={cache.rowHeight} rowRenderer={_this.renderRow} width={width} onScrollbarPresenceChange={_this.setScrollbarSize} 
            // when the component mounts, it scrolls to the last item
            scrollToIndex={scrollToIndex} scrollToAlignment={scrollToIndex ? 'end' : undefined}/>
            </React.Fragment>);
        }}
        </AutoSizer>
      </Wrapper>);
    };
    return ListContainer;
}(React.Component));
export default ListContainer;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n  ", "\n"], ["\n  overflow: hidden;\n  ", "\n"])), aroundContentStyle);
// it makes the list have a dynamic height; otherwise, in the case of filtered options, a list will be displayed with an empty space
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"], ["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"])), function (p) { return p.height; });
var Row = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 45px minmax(55px, 1fr) 6fr 86px 67px;\n  @media (min-width: ", ") {\n    grid-template-columns: 63px minmax(132px, 1fr) 6fr 75px 85px;\n  }\n  ", "\n"], ["\n  display: grid;\n  grid-template-columns: 45px minmax(55px, 1fr) 6fr 86px 67px;\n  @media (min-width: ", ") {\n    grid-template-columns: 63px minmax(132px, 1fr) 6fr 75px 85px;\n  }\n  ", "\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.width && "width: " + p.width + "px;"; });
var RowSticky = styled(Row)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.scrollbarSize &&
        "padding-right: " + p.scrollbarSize + ";\n     grid-template-columns: 45px minmax(55px, 1fr) 6fr 86px calc(67px + " + p.scrollbarSize + "px);\n     @media (min-width: " + p.theme.breakpoints[0] + ") {\n      grid-template-columns: 63px minmax(132px, 1fr) 6fr 75px calc(85px + " + p.scrollbarSize + "px);\n    }\n  ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=list.jsx.map