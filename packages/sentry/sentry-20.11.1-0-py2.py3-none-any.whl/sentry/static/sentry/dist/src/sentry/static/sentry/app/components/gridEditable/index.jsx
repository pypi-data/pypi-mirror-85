import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconWarning } from 'app/icons';
import { Header, HeaderTitle, HeaderButtonContainer, Body, Grid, GridRow, GridHead, GridHeadCell, GridHeadCellStatic, GridBody, GridBodyCell, GridBodyCellStatus, GridResizer, } from './styles';
import { COL_WIDTH_MINIMUM, COL_WIDTH_UNDEFINED } from './utils';
var GridEditable = /** @class */ (function (_super) {
    __extends(GridEditable, _super);
    function GridEditable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            numColumn: 0,
        };
        _this.refGrid = React.createRef();
        _this.resizeWindowLifecycleEvents = {
            mousemove: [],
            mouseup: [],
        };
        _this.onResetColumnSize = function (e, i) {
            e.stopPropagation();
            var nextColumnOrder = __spread(_this.props.columnOrder);
            nextColumnOrder[i] = __assign(__assign({}, nextColumnOrder[i]), { width: COL_WIDTH_UNDEFINED });
            _this.setGridTemplateColumns(nextColumnOrder);
            var onResizeColumn = _this.props.grid.onResizeColumn;
            if (onResizeColumn) {
                onResizeColumn(i, __assign(__assign({}, nextColumnOrder[i]), { width: COL_WIDTH_UNDEFINED }));
            }
        };
        _this.onResizeMouseDown = function (e, i) {
            if (i === void 0) { i = -1; }
            e.stopPropagation();
            // Block right-click and other funky stuff
            if (i === -1 || e.type === 'contextmenu') {
                return;
            }
            // <GridResizer> is nested 1 level down from <GridHeadCell>
            var cell = e.currentTarget.parentElement;
            if (!cell) {
                return;
            }
            // HACK: Do not put into state to prevent re-rendering of component
            _this.resizeMetadata = {
                columnIndex: i,
                columnWidth: cell.offsetWidth,
                cursorX: e.clientX,
            };
            window.addEventListener('mousemove', _this.onResizeMouseMove);
            _this.resizeWindowLifecycleEvents.mousemove.push(_this.onResizeMouseMove);
            window.addEventListener('mouseup', _this.onResizeMouseUp);
            _this.resizeWindowLifecycleEvents.mouseup.push(_this.onResizeMouseUp);
        };
        _this.onResizeMouseUp = function (e) {
            var metadata = _this.resizeMetadata;
            var onResizeColumn = _this.props.grid.onResizeColumn;
            if (!metadata || !onResizeColumn) {
                return;
            }
            var columnOrder = _this.props.columnOrder;
            var widthChange = e.clientX - metadata.cursorX;
            onResizeColumn(metadata.columnIndex, __assign(__assign({}, columnOrder[metadata.columnIndex]), { width: metadata.columnWidth + widthChange }));
            _this.resizeMetadata = undefined;
            _this.clearWindowLifecycleEvents();
        };
        _this.onResizeMouseMove = function (e) {
            var resizeMetadata = _this.resizeMetadata;
            if (!resizeMetadata) {
                return;
            }
            window.requestAnimationFrame(function () { return _this.resizeGridColumn(e, resizeMetadata); });
        };
        /**
         * Recalculate the dimensions of Grid and Columns and redraws them
         */
        _this.redrawGridColumn = function () {
            _this.setGridTemplateColumns(_this.props.columnOrder);
        };
        _this.renderGridBodyRow = function (dataRow, row) {
            var _a = _this.props, columnOrder = _a.columnOrder, grid = _a.grid;
            var prependColumns = grid.renderPrependColumns
                ? grid.renderPrependColumns(false, dataRow, row)
                : [];
            return (<GridRow key={row}>
        {prependColumns &&
                prependColumns.map(function (item, i) { return (<GridBodyCell key={"prepend-" + i}>{item}</GridBodyCell>); })}
        {columnOrder.map(function (col, i) { return (<GridBodyCell key={"" + col.key + i}>
            {grid.renderBodyCell
                ? grid.renderBodyCell(col, dataRow, row, i)
                : dataRow[col.key]}
          </GridBodyCell>); })}
      </GridRow>);
        };
        return _this;
    }
    // Static methods do not allow the use of generics bounded to the parent class
    // For more info: https://github.com/microsoft/TypeScript/issues/14600
    GridEditable.getDerivedStateFromProps = function (props, prevState) {
        return __assign(__assign({}, prevState), { numColumn: props.columnOrder.length });
    };
    GridEditable.prototype.componentDidMount = function () {
        window.addEventListener('resize', this.redrawGridColumn);
        this.setGridTemplateColumns(this.props.columnOrder);
    };
    GridEditable.prototype.componentDidUpdate = function () {
        // Redraw columns whenever new props are received
        this.setGridTemplateColumns(this.props.columnOrder);
    };
    GridEditable.prototype.componentWillUnmount = function () {
        this.clearWindowLifecycleEvents();
        window.removeEventListener('resize', this.redrawGridColumn);
    };
    GridEditable.prototype.clearWindowLifecycleEvents = function () {
        var _this = this;
        Object.keys(this.resizeWindowLifecycleEvents).forEach(function (e) {
            _this.resizeWindowLifecycleEvents[e].forEach(function (c) { return window.removeEventListener(e, c); });
            _this.resizeWindowLifecycleEvents[e] = [];
        });
    };
    GridEditable.prototype.resizeGridColumn = function (e, metadata) {
        var grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        var widthChange = e.clientX - metadata.cursorX;
        var nextColumnOrder = __spread(this.props.columnOrder);
        nextColumnOrder[metadata.columnIndex] = __assign(__assign({}, nextColumnOrder[metadata.columnIndex]), { width: Math.max(metadata.columnWidth + widthChange, 0) });
        this.setGridTemplateColumns(nextColumnOrder);
    };
    /**
     * Set the CSS for Grid Column
     */
    GridEditable.prototype.setGridTemplateColumns = function (columnOrder) {
        var grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        var prependColumns = this.props.grid.prependColumnWidths || [];
        var prepend = prependColumns.join(' ');
        var widths = columnOrder.map(function (item) {
            if (item.width === COL_WIDTH_UNDEFINED) {
                return "minmax(" + COL_WIDTH_MINIMUM + "px, auto)";
            }
            else if (typeof item.width === 'number' && item.width > COL_WIDTH_MINIMUM) {
                return item.width + "px";
            }
            return COL_WIDTH_MINIMUM + "px";
        });
        // The last column has no resizer and should always be a flexible column
        // to prevent underflows.
        if (widths.length > 0) {
            widths[widths.length - 1] = "minmax(" + COL_WIDTH_MINIMUM + "px, auto)";
        }
        grid.style.gridTemplateColumns = prepend + " " + widths.join(' ');
    };
    GridEditable.prototype.renderGridHead = function () {
        var _this = this;
        var _a = this.props, error = _a.error, isLoading = _a.isLoading, columnOrder = _a.columnOrder, grid = _a.grid, data = _a.data;
        // Ensure that the last column cannot be removed
        var numColumn = columnOrder.length;
        var prependColumns = grid.renderPrependColumns
            ? grid.renderPrependColumns(true)
            : [];
        return (<GridRow>
        {prependColumns &&
            prependColumns.map(function (item, i) { return (<GridHeadCellStatic key={"prepend-" + i}>{item}</GridHeadCellStatic>); })}
        {
        /* Note that this.onResizeMouseDown assumes GridResizer is nested
          1 levels under GridHeadCell */
        columnOrder.map(function (column, i) { return (<GridHeadCell key={i + "." + column.key} isFirst={i === 0}>
              {grid.renderHeadCell ? grid.renderHeadCell(column, i) : column.name}
              {i !== numColumn - 1 && (<GridResizer dataRows={!error && !isLoading && data ? data.length : 0} onMouseDown={function (e) { return _this.onResizeMouseDown(e, i); }} onDoubleClick={function (e) { return _this.onResetColumnSize(e, i); }} onContextMenu={_this.onResizeMouseDown}/>)}
            </GridHeadCell>); })}
      </GridRow>);
    };
    GridEditable.prototype.renderGridBody = function () {
        var _a = this.props, data = _a.data, error = _a.error, isLoading = _a.isLoading;
        if (error) {
            return this.renderError();
        }
        if (isLoading) {
            return this.renderLoading();
        }
        if (!data || data.length === 0) {
            return this.renderEmptyData();
        }
        return data.map(this.renderGridBodyRow);
    };
    GridEditable.prototype.renderError = function () {
        return (<GridRow>
        <GridBodyCellStatus>
          <IconWarning color="gray300" size="lg"/>
        </GridBodyCellStatus>
      </GridRow>);
    };
    GridEditable.prototype.renderLoading = function () {
        return (<GridRow>
        <GridBodyCellStatus>
          <LoadingIndicator />
        </GridBodyCellStatus>
      </GridRow>);
    };
    GridEditable.prototype.renderEmptyData = function () {
        return (<GridRow>
        <GridBodyCellStatus>
          <EmptyStateWarning>
            <p>{t('No results found')}</p>
          </EmptyStateWarning>
        </GridBodyCellStatus>
      </GridRow>);
    };
    GridEditable.prototype.render = function () {
        var _a = this.props, title = _a.title, headerButtons = _a.headerButtons;
        var showHeader = title || headerButtons;
        return (<React.Fragment>
        {showHeader && (<Header>
            {title && <HeaderTitle>{title}</HeaderTitle>}
            {headerButtons && (<HeaderButtonContainer>{headerButtons()}</HeaderButtonContainer>)}
          </Header>)}
        <Body>
          <Grid data-test-id="grid-editable" ref={this.refGrid}>
            <GridHead>{this.renderGridHead()}</GridHead>
            <GridBody>{this.renderGridBody()}</GridBody>
          </Grid>
        </Body>
      </React.Fragment>);
    };
    return GridEditable;
}(React.Component));
export default GridEditable;
export { COL_WIDTH_MINIMUM, COL_WIDTH_UNDEFINED, };
//# sourceMappingURL=index.jsx.map