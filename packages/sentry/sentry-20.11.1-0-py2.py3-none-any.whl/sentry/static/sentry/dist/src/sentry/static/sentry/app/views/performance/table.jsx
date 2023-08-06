import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import { IconStar } from 'app/icons';
import Pagination from 'app/components/pagination';
import Link from 'app/components/links/link';
import { isFieldSortable } from 'app/utils/discover/eventView';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { transactionSummaryRouteWithQuery } from './transactionSummary/utils';
import { COLUMN_TITLES } from './data';
export function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                updateQuery(searchConditions, action, column.name, value);
                ReactRouter.browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: stringifyQueryObject(searchConditions) }),
                });
            };
        };
        _this.renderBodyCellWithData = function (tableData) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta) {
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, COLUMN_TITLES[index]);
            };
        };
        _this.renderPrependCellWithData = function (tableData) {
            var eventView = _this.props.eventView;
            var keyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'key_transaction'; });
            return function (isHeader, dataRow) {
                if (!keyTransactionColumn) {
                    return [];
                }
                if (isHeader) {
                    var star = (<IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                    return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, keyTransactionColumn, star)];
                }
                else {
                    return [_this.renderBodyCell(tableData, keyTransactionColumn, dataRow)];
                }
            };
        };
        _this.handleSummaryClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spread(_this.state.widths);
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    Table.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location, summaryConditions = _a.summaryConditions;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        var allowActions = [
            Actions.ADD,
            Actions.EXCLUDE,
            Actions.SHOW_GREATER_THAN,
            Actions.SHOW_LESS_THAN,
        ];
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            summaryView.query = summaryConditions;
            var target = transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
            });
            return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <Link to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </Link>
        </CellAction>);
        }
        if (field.startsWith('key_transaction') || field.startsWith('user_misery')) {
            // don't display per cell actions for key_transaction or user_misery
            return rendered;
        }
        return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </CellAction>);
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _a = this.props, eventView = _a.eventView, location = _a.location;
        return (<HeaderCell column={column} tableMeta={tableMeta}>
        {function (_a) {
            var align = _a.align;
            var field = { field: column.name, width: column.width };
            function generateSortLink() {
                if (!tableMeta) {
                    return undefined;
                }
                var nextEventView = eventView.sortOnField(field, tableMeta);
                var queryStringObject = nextEventView.generateQueryStringObject();
                return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { sort: queryStringObject.sort }) });
            }
            var currentSort = eventView.sortForField(field, tableMeta);
            var canSort = isFieldSortable(field, tableMeta) && field.field !== 'key_transaction';
            return (<SortLink align={align} title={title || field.field} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
        }}
      </HeaderCell>);
    };
    Table.prototype.getSortedEventView = function () {
        var eventView = this.props.eventView;
        return eventView.withSorts(__spread([
            {
                field: 'key_transaction',
                kind: 'desc',
            }
        ], eventView.sorts));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var widths = this.state.widths;
        var columnOrder = eventView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter(function (col) { return col.name !== 'key_transaction'; })
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var sortedEventView = this.getSortedEventView();
        var columnSortBy = sortedEventView.getSorts();
        var prependColumnWidths = ['max-content'];
        return (<div>
        <DiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location}>
          {function (_a) {
            var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
            return (<React.Fragment>
              <GridEditable isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                onResizeColumn: _this.handleResizeColumn,
                renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                renderBodyCell: _this.renderBodyCellWithData(tableData),
                renderPrependColumns: _this.renderPrependCellWithData(tableData),
                prependColumnWidths: prependColumnWidths,
            }} location={location}/>
              <Pagination pageLinks={pageLinks}/>
            </React.Fragment>);
        }}
        </DiscoverQuery>
      </div>);
    };
    return Table;
}(React.Component));
export default Table;
//# sourceMappingURL=table.jsx.map