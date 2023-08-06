import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { MultiGrid, AutoSizer } from 'react-virtualized';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ExternalLink from 'app/components/links/externalLink';
import Tooltip from 'app/components/tooltip';
import Panel from 'app/components/panels/panel';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import withOrganization from 'app/utils/withOrganization';
import { getDisplayValue, getDisplayText } from './utils';
var TABLE_ROW_HEIGHT = 30;
var TABLE_ROW_BORDER = 1;
var TABLE_ROW_HEIGHT_WITH_BORDER = TABLE_ROW_HEIGHT + TABLE_ROW_BORDER;
var MIN_COL_WIDTH = 100;
var MAX_COL_WIDTH = 500;
var CELL_PADDING = 22;
var MIN_VISIBLE_ROWS = 6;
var MAX_VISIBLE_ROWS = 30;
var OTHER_ELEMENTS_HEIGHT = 70; // pagination buttons, query summary
/**
 * Renders results in a table as well as a query summary (timing, rows returned)
 * from any Snuba result
 */
var ResultTable = /** @class */ (function (_super) {
    __extends(ResultTable, _super);
    function ResultTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getCellRenderer = function (cols) { return function (_a) {
            var key = _a.key, rowIndex = _a.rowIndex, columnIndex = _a.columnIndex, style = _a.style;
            var _b = _this.props.data, data = _b.data, meta = _b.meta;
            var isSpacingCol = columnIndex === cols.length;
            var colName = isSpacingCol ? null : cols[columnIndex].name;
            var isNumberCol = !isSpacingCol && ['number', 'integer'].includes(meta[columnIndex].type);
            var align = isNumberCol && colName !== 'issue.id' ? 'right' : 'left';
            if (rowIndex === 0) {
                return (<TableHeader key={key} style={style} align={align}>
          <strong>{colName}</strong>
        </TableHeader>);
            }
            var value = isSpacingCol ? null : getDisplayValue(data[rowIndex - 1][colName]);
            // check for id column
            if (columnIndex < cols.length && cols[columnIndex].name === 'id') {
                value = _this.getEventLink(data[rowIndex - 1]);
            }
            // check for issue.id columm
            if (columnIndex < cols.length && cols[columnIndex].name === 'issue.id') {
                value = _this.getIssueLink(data[rowIndex - 1]);
            }
            return (<Cell key={key} style={style} isOddRow={rowIndex % 2 === 1} align={align}>
        {value}
      </Cell>);
        }; };
        _this.getEventLink = function (event) {
            var _a = _this.props.organization, slug = _a.slug, projects = _a.projects;
            var projectSlug = projects.find(function (project) { return project.id === "" + event['project.id']; })
                .slug;
            var basePath = "/organizations/" + slug + "/projects/" + projectSlug + "/";
            return (<Tooltip title={t('Open event')}>
        <ExternalLink href={basePath + "events/" + event.id + "/"}>{event.id}</ExternalLink>
      </Tooltip>);
        };
        _this.getIssueLink = function (event) {
            var slug = _this.props.organization.slug;
            var basePath = "/organizations/" + slug + "/";
            return (<Tooltip title={t('Open issue')}>
        <ExternalLink href={basePath + "issues/" + event['issue.id']}>
          {event['issue.id']}
        </ExternalLink>
      </Tooltip>);
        };
        // Returns an array of column widths for each column in the table.
        // Estimates the column width based on the header row and the longest three
        // rows of data. Since this might be expensive, we'll only do this if there\
        // are less than 20 columns of data to check in total.
        // Adds an empty column at the end with the remaining table width if any.
        _this.getColumnWidths = function (tableWidth) {
            var data = _this.props.data.data;
            var cols = _this.getColumnList();
            var widths = [];
            if (cols.length < 20) {
                cols.forEach(function (col) {
                    var colName = col.name;
                    var sizes = [_this.measureText(colName, true)];
                    // Get top 3 unique results sorted by string length
                    // We want to avoid calling measureText() too much so only do this
                    // for the top 3 longest strings
                    var uniqs = __spread(new Set(data.map(function (row) { return row[colName]; }))).map(function (colData) { return getDisplayText(colData); })
                        .sort(function (a, b) { return b.length - a.length; })
                        .slice(0, 3);
                    uniqs.forEach(function (colData) {
                        sizes.push(_this.measureText(colData, false));
                    });
                    // Ensure size is within max and min bounds, add 20px for cell padding
                    var width = Math.max(Math.min(Math.max.apply(Math, __spread(sizes)) + CELL_PADDING, MAX_COL_WIDTH), MIN_COL_WIDTH);
                    widths.push(width);
                });
            }
            else {
                cols.forEach(function () {
                    widths.push(MIN_COL_WIDTH);
                });
            }
            var sumOfWidths = widths.reduce(function (sum, w) { return sum + w; }, 0) + 2;
            // Add a fake column of remaining width
            widths.push(Math.max(tableWidth - sumOfWidths, 0));
            return widths;
        };
        _this.getRowHeight = function (rowIndex, columnsToCheck) {
            var data = _this.props.data.data;
            if (rowIndex === 0) {
                return TABLE_ROW_HEIGHT_WITH_BORDER;
            }
            var row = data[rowIndex - 1]; // -1 offset due to header row
            var colWidths = columnsToCheck.map(function (col) {
                return _this.measureText(getDisplayText(row[col]), false);
            });
            var maxColWidth = Math.max.apply(Math, __spread(colWidths, [0]));
            // Number of rows to be rendered based on text content divided by cell width
            // Apply a min of 1 and max of 3
            var rows = Math.max(Math.min(Math.ceil(maxColWidth / (MAX_COL_WIDTH - CELL_PADDING)), 3), 1);
            return TABLE_ROW_HEIGHT * rows + TABLE_ROW_BORDER;
        };
        _this.getColumnList = function () {
            var _a = _this.props, query = _a.query, meta = _a.data.meta;
            var fields = new Set(__spread((query.fields || []), query.aggregations.map(function (agg) { return agg[2]; })));
            return meta.filter(function (_a) {
                var name = _a.name;
                return fields.has(name);
            });
        };
        _this.measureText = function (text, isHeader) {
            // Create canvas once in order to measure column widths
            if (!_this.canvas) {
                _this.canvas = document.createElement('canvas');
            }
            var context = _this.canvas.getContext('2d');
            context.font = isHeader ? 'bold 14px Rubik' : 'normal 14px Rubik';
            // The measureText function sometimes slightly miscalculates text width.
            // Add 5px to compensate since we want to avoid rows breaking unnecessarily.
            // (better to over than under estimate)
            return Math.ceil(context.measureText(text).width) + 5;
        };
        _this.getMaxVisibleRows = function (elementHeight) {
            if (!elementHeight) {
                return MIN_VISIBLE_ROWS;
            }
            // subtract header row, pagination buttons and query summary
            var height = elementHeight - TABLE_ROW_HEIGHT_WITH_BORDER - OTHER_ELEMENTS_HEIGHT;
            var visibleRows = Math.floor(height / TABLE_ROW_HEIGHT_WITH_BORDER);
            // Apply min/max
            return Math.max(Math.min(visibleRows, MAX_VISIBLE_ROWS), MIN_VISIBLE_ROWS);
        };
        return _this;
    }
    ResultTable.prototype.componentDidUpdate = function (prevProps) {
        var _this = this;
        if (this.props.data.meta !== prevProps.data.meta) {
            this.grid.recomputeGridSize();
        }
        if (this.props.width !== prevProps.width) {
            this.forceUpdate(function () { return _this.grid.recomputeGridSize(); });
        }
    };
    ResultTable.prototype.renderTable = function () {
        var _this = this;
        var _a = this.props, data = _a.data.data, height = _a.height;
        var cols = this.getColumnList();
        // Add one column at the end to make sure table spans full width
        var colCount = cols.length + 1;
        var visibleRows = this.getMaxVisibleRows(height);
        var cellRenderer = this.getCellRenderer(cols);
        return (<Panel>
        <Grid visibleRows={Math.min(data.length, visibleRows) + 1}>
          <AutoSizer>
            {function (size) {
            var columnWidths = _this.getColumnWidths(size.width);
            // Since calculating row height might be expensive, we'll only
            // perform the check against a subset of columns (where col width
            // has exceeded the max value)
            var columnsToCheck = columnWidths.reduce(function (acc, colWidth, idx) {
                if (colWidth === MAX_COL_WIDTH) {
                    acc.push(cols[idx].name);
                }
                return acc;
            }, []);
            return (<MultiGrid ref={function (ref) { return (_this.grid = ref); }} width={size.width - 1} height={size.height} rowCount={data.length + 1} columnCount={colCount} fixedRowCount={1} rowHeight={function (_a) {
                var index = _a.index;
                return _this.getRowHeight(index, columnsToCheck);
            }} columnWidth={function (_a) {
                var index = _a.index;
                return columnWidths[index];
            }} cellRenderer={cellRenderer} overscanByPixels={800}/>);
        }}
          </AutoSizer>
        </Grid>
        {!data.length && <EmptyStateWarning small>{t('No results')}</EmptyStateWarning>}
      </Panel>);
    };
    ResultTable.prototype.render = function () {
        var error = this.props.data.error;
        if (error) {
            return <div>{error}</div>;
        }
        return <div>{this.renderTable()}</div>;
    };
    return ResultTable;
}(React.Component));
export { ResultTable };
export default withOrganization(ResultTable);
var Grid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* cell height + cell border + top and bottom Panel border */\n  height: ", ";\n  overflow: hidden;\n\n  .ReactVirtualized__Grid {\n    outline: none;\n  }\n"], ["\n  /* cell height + cell border + top and bottom Panel border */\n  height: ", ";\n  overflow: hidden;\n\n  .ReactVirtualized__Grid {\n    outline: none;\n  }\n"])), function (p) { return p.visibleRows * TABLE_ROW_HEIGHT_WITH_BORDER + 2 + "px"; });
var Cell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  ", ";\n  overflow: scroll;\n  font-size: 14px;\n  line-height: ", "px;\n  padding: 0 10px;\n  border-top: 1px solid ", ";\n\n  ::-webkit-scrollbar {\n    display: none;\n  }\n\n  @-moz-document url-prefix() {\n    overflow: hidden;\n  }\n\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n"], ["\n  ", ";\n  ", ";\n  overflow: scroll;\n  font-size: 14px;\n  line-height: ", "px;\n  padding: 0 10px;\n  border-top: 1px solid ", ";\n\n  ::-webkit-scrollbar {\n    display: none;\n  }\n\n  @-moz-document url-prefix() {\n    overflow: hidden;\n  }\n\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n"])), function (p) { return !p.isOddRow && "background-color: " + p.theme.backgroundSecondary + ";"; }, function (p) { return "text-align: " + p.align + ";"; }, TABLE_ROW_HEIGHT, function (p) { return p.theme.innerBorder; });
var TableHeader = styled(Cell)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  border-top: none;\n  border-bottom: 1px solid ", ";\n  &:first-of-type {\n    border-top-left-radius: 3px;\n  }\n"], ["\n  background: ", ";\n  color: ", ";\n  border-top: none;\n  border-bottom: 1px solid ", ";\n  &:first-of-type {\n    border-top-left-radius: 3px;\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.border; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=table.jsx.map