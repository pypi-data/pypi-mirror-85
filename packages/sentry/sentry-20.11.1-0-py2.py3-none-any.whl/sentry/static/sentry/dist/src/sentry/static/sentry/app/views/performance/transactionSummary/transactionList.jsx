import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import space from 'app/styles/space';
import { t } from 'app/locale';
import DiscoverButton from 'app/components/discoverButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import PanelTable from 'app/components/panels/panelTable';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import CellAction, { updateQuery } from 'app/views/eventsV2/table/cellAction';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import SortLink from 'app/components/gridEditable/sortLink';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { generateEventSlug } from 'app/utils/discover/urls';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getDuration } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { GridCell, GridCellNumber } from '../styles';
import { getTransactionDetailsUrl, getTransactionComparisonUrl } from '../utils';
import BaselineQuery from './baselineQuery';
var TOP_TRANSACTION_LIMIT = 5;
function getFilterOptions(_a) {
    var p95 = _a.p95;
    return [
        {
            query: null,
            sort: { kind: 'asc', field: 'transaction.duration' },
            value: 'fastest',
            label: t('Fastest Transactions'),
        },
        {
            query: [['transaction.duration', "<=" + p95.toFixed(0)]],
            sort: { kind: 'desc', field: 'transaction.duration' },
            value: 'slow',
            label: t('Slow Transactions (p95)'),
        },
        {
            query: null,
            sort: { kind: 'desc', field: 'transaction.duration' },
            value: 'outlier',
            label: t('Outlier Transactions (p100)'),
        },
        {
            query: null,
            sort: { kind: 'desc', field: 'timestamp' },
            value: 'recent',
            label: t('Recent Transactions'),
        },
    ];
}
function getTransactionSort(location, p95) {
    var options = getFilterOptions({ p95: p95 });
    var urlParam = decodeScalar(location.query.showTransactions) || 'slow';
    var selected = options.find(function (opt) { return opt.value === urlParam; }) || options[0];
    return { selected: selected, options: options };
}
var TransactionList = /** @class */ (function (_super) {
    __extends(TransactionList, _super);
    function TransactionList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCursor = function (cursor, pathname, query) {
            browserHistory.push({
                pathname: pathname,
                query: __assign(__assign({}, query), { transactionCursor: cursor }),
            });
        };
        _this.handleTransactionFilterChange = function (value) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.filter_transactions',
                eventName: 'Performance Views: Filter transactions table',
                organization_id: parseInt(organization.id, 10),
                value: value,
            });
            var target = {
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            browserHistory.push(target);
        };
        _this.handleDiscoverViewClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_in_discover',
                eventName: 'Performance Views: View in Discover from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        return _this;
    }
    TransactionList.prototype.renderTable = function (eventView) {
        var _this = this;
        var _a;
        var _b = this.props, location = _b.location, organization = _b.organization, transactionName = _b.transactionName;
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a.transactionCursor);
        if (!organization.features.includes('transaction-comparison')) {
            return (<DiscoverQuery location={location} eventView={eventView} orgSlug={organization.slug} limit={TOP_TRANSACTION_LIMIT} cursor={cursor}>
          {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
              <TransactionTable organization={organization} location={location} transactionName={transactionName} eventView={eventView} tableData={tableData} isLoading={isLoading} baselineTransaction={null}/>
              <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
            </React.Fragment>);
            }}
        </DiscoverQuery>);
        }
        return (<DiscoverQuery location={location} eventView={eventView} orgSlug={organization.slug} limit={TOP_TRANSACTION_LIMIT} cursor={cursor}>
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
            return (<BaselineQuery eventView={eventView} orgSlug={organization.slug}>
            {function (baselineQueryProps) {
                return (<React.Fragment>
                  <TransactionTable organization={organization} location={location} transactionName={transactionName} eventView={eventView} tableData={tableData} isLoading={isLoading || baselineQueryProps.isLoading} baselineTransaction={baselineQueryProps.results}/>
                  <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
                </React.Fragment>);
            }}
          </BaselineQuery>);
        }}
      </DiscoverQuery>);
    };
    TransactionList.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, slowDuration = _a.slowDuration;
        var _b = getTransactionSort(location, slowDuration || 0), selected = _b.selected, options = _b.options;
        var sortedEventView = eventView.withSorts([selected.sort]);
        if (selected.query) {
            var query_1 = tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = stringifyQueryObject(query_1);
        }
        return (<React.Fragment>
        <Header>
          <DropdownControl data-test-id="filter-transactions" label={selected.label} buttonProps={{ prefix: t('Filter'), size: 'small' }}>
            {options.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem key={value} onSelect={_this.handleTransactionFilterChange} eventKey={value} isActive={value === selected.value}>
                {label}
              </DropdownItem>);
        })}
          </DropdownControl>
          <HeaderButtonContainer>
            <DiscoverButton onClick={this.handleDiscoverViewClick} to={sortedEventView.getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
              {t('Open in Discover')}
            </DiscoverButton>
          </HeaderButtonContainer>
        </Header>
        {this.renderTable(sortedEventView)}
      </React.Fragment>);
    };
    return TransactionList;
}(React.Component));
var TransactionTable = /** @class */ (function (_super) {
    __extends(TransactionTable, _super);
    function TransactionTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleViewDetailsClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_details',
                eventName: 'Performance Views: View Details from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeTag('transaction');
                updateQuery(searchConditions, action, column.name, value);
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: stringifyQueryObject(searchConditions) }),
                });
            };
        };
        return _this;
    }
    TransactionTable.prototype.renderHeader = function () {
        var _a = this.props, eventView = _a.eventView, tableData = _a.tableData, organization = _a.organization;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var columnOrder = eventView.getColumns();
        var generateSortLink = function () { return undefined; };
        var titles = [t('id'), t('user'), t('duration'), t('timestamp')];
        var headerColumns = titles.map(function (title, index) { return (<HeaderCell column={columnOrder[index]} tableMeta={tableMeta} key={index}>
        {function (_a) {
            var align = _a.align;
            return (<HeadCellContainer>
              <SortLink align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </HeadCellContainer>);
        }}
      </HeaderCell>); });
        // add baseline transaction column
        if (organization.features.includes('transaction-comparison')) {
            headerColumns.push(<HeadCellContainer key="baseline">
          <SortLink align="right" title={t('Compared to Baseline')} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        }
        return headerColumns;
    };
    TransactionTable.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        var columnOrder = this.props.eventView.getColumns();
        tableData.data.forEach(function (row, i) {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(_this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    };
    TransactionTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, baselineTransaction = _a.baselineTransaction;
        var resultsRow = columnOrder.map(function (column, index) {
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            var isFirstCell = index === 0;
            if (isFirstCell) {
                // The first column of the row should link to the transaction details view
                var eventSlug = generateEventSlug(row);
                var target = getTransactionDetailsUrl(organization, eventSlug, transactionName, location.query);
                rendered = (<Link data-test-id="view-details" to={target} onClick={_this.handleViewDetailsClick}>
            {rendered}
          </Link>);
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            return (<BodyCellContainer key={key}>
          <CellAction column={column} dataRow={row} handleCellAction={_this.handleCellAction(column)}>
            {isNumeric ? (<GridCellNumber>{rendered}</GridCellNumber>) : (<GridCell>{rendered}</GridCell>)}
          </CellAction>
        </BodyCellContainer>);
        });
        // add baseline transaction column
        if (organization.features.includes('transaction-comparison')) {
            if (baselineTransaction) {
                var currentTransactionDuration = Number(row['transaction.duration']) || 0;
                var delta = Math.abs(currentTransactionDuration - baselineTransaction['transaction.duration']);
                var relativeSpeed = currentTransactionDuration < baselineTransaction['transaction.duration']
                    ? t('faster')
                    : currentTransactionDuration > baselineTransaction['transaction.duration']
                        ? t('slower')
                        : '';
                var target = getTransactionComparisonUrl({
                    organization: organization,
                    baselineEventSlug: generateEventSlug(baselineTransaction),
                    regressionEventSlug: generateEventSlug(row),
                    transaction: transactionName,
                    query: location.query,
                });
                resultsRow.push(<BodyCellContainer key={rowIndex + "-baseline"} style={{ textAlign: 'right' }}>
            <GridCell>
              <Link to={target} onClick={this.handleViewDetailsClick}>
                {getDuration(delta / 1000, delta < 1000 ? 0 : 2) + " " + relativeSpeed}
              </Link>
            </GridCell>
          </BodyCellContainer>);
            }
            else {
                resultsRow.push(<BodyCellContainer key={rowIndex + "-baseline"}>-</BodyCellContainer>);
            }
        }
        return resultsRow;
    };
    TransactionTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        var loader = <LoadingIndicator style={{ margin: '70px auto' }}/>;
        return (<StyledPanelTable isEmpty={!hasResults} emptyMessage={t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </StyledPanelTable>);
    };
    return TransactionTable;
}(React.PureComponent));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"])), space(1));
var HeaderButtonContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var HeadCellContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var BodyCellContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", " ", ";\n  ", ";\n"], ["\n  padding: ", " ", ";\n  ", ";\n"])), space(1), space(2), overflowEllipsis);
var StyledPagination = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n"], ["\n  margin: 0 0 ", " 0;\n"])), space(3));
export default TransactionList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=transactionList.jsx.map