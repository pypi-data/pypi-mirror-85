import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import DiscoverButton from 'app/components/discoverButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import PanelTable from 'app/components/panels/panelTable';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { decodeScalar } from 'app/utils/queryString';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import { GridCell, GridCellNumber } from 'app/views/performance/styles';
var DEFAULT_TRANSACTION_LIMIT = 5;
var TransactionsList = /** @class */ (function (_super) {
    __extends(TransactionsList, _super);
    function TransactionsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCursor = function (cursor, pathname, query) {
            var _a;
            var cursorName = _this.props.cursorName;
            browserHistory.push({
                pathname: pathname,
                query: __assign(__assign({}, query), (_a = {}, _a[cursorName] = cursor, _a)),
            });
        };
        return _this;
    }
    TransactionsList.prototype.renderHeader = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, dropdownTitle = _a.dropdownTitle, selected = _a.selected, options = _a.options, handleDropdownChange = _a.handleDropdownChange;
        var sortedEventView = eventView.withSorts([selected.sort]);
        return (<Header>
        <DropdownControl data-test-id="filter-transactions" label={selected.label} buttonProps={{ prefix: dropdownTitle, size: 'small' }}>
          {options.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem data-test-id={"option-" + value} key={value} onSelect={handleDropdownChange} eventKey={value} isActive={value === selected.value}>
              {label}
            </DropdownItem>);
        })}
        </DropdownControl>
        <HeaderButtonContainer>
          <DiscoverButton to={sortedEventView.getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
            {t('Open in Discover')}
          </DiscoverButton>
        </HeaderButtonContainer>
      </Header>);
    };
    TransactionsList.prototype.renderTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, eventView = _b.eventView, location = _b.location, organization = _b.organization, selected = _b.selected, cursorName = _b.cursorName, limit = _b.limit, titles = _b.titles, linkDataTestId = _b.linkDataTestId, generateFirstLink = _b.generateFirstLink;
        var sortedEventView = eventView.withSorts([selected.sort]);
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<DiscoverQuery location={location} eventView={sortedEventView} orgSlug={organization.slug} limit={limit} cursor={cursor}>
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
            return (<React.Fragment>
            <TransactionsTable eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} titles={titles} linkDataTestId={linkDataTestId} generateFirstLink={generateFirstLink}/>
            <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
          </React.Fragment>);
        }}
      </DiscoverQuery>);
    };
    TransactionsList.prototype.render = function () {
        return (<React.Fragment>
        {this.renderHeader()}
        {this.renderTable()}
      </React.Fragment>);
    };
    TransactionsList.defaultProps = {
        cursorName: 'transactionCursor',
        limit: DEFAULT_TRANSACTION_LIMIT,
    };
    return TransactionsList;
}(React.Component));
var TransactionsTable = /** @class */ (function (_super) {
    __extends(TransactionsTable, _super);
    function TransactionsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionsTable.prototype.renderHeader = function () {
        var _a = this.props, eventView = _a.eventView, tableData = _a.tableData, titles = _a.titles;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var columnOrder = eventView.getColumns();
        var generateSortLink = function () { return undefined; };
        var tableTitles = titles !== null && titles !== void 0 ? titles : eventView.getFields().map(function (field) { return t(field); });
        return tableTitles.map(function (title, index) { return (<HeaderCell column={columnOrder[index]} tableMeta={tableMeta} key={index}>
        {function (_a) {
            var align = _a.align;
            return (<HeadCellContainer>
              <SortLink align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </HeadCellContainer>);
        }}
      </HeaderCell>); });
    };
    TransactionsTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _a = this.props, organization = _a.organization, location = _a.location, linkDataTestId = _a.linkDataTestId, generateFirstLink = _a.generateFirstLink;
        var resultsRow = columnOrder.map(function (column, index) {
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            if (generateFirstLink) {
                var isFirstCell = index === 0;
                if (isFirstCell) {
                    var target = generateFirstLink(organization, row, location.query);
                    rendered = (<Link data-test-id={linkDataTestId !== null && linkDataTestId !== void 0 ? linkDataTestId : 'transactions-list-link'} to={target}>
              {rendered}
            </Link>);
                }
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            return (<BodyCellContainer key={key}>
          {isNumeric ? (<GridCellNumber>{rendered}</GridCellNumber>) : (<GridCell>{rendered}</GridCell>)}
        </BodyCellContainer>);
        });
        return resultsRow;
    };
    TransactionsTable.prototype.renderResults = function () {
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
    TransactionsTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        var loader = <LoadingIndicator style={{ margin: '70px auto' }}/>;
        return (<StyledPanelTable isEmpty={!hasResults} emptyMessage={t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </StyledPanelTable>);
    };
    return TransactionsTable;
}(React.PureComponent));
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"])), space(1));
var HeaderButtonContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var StyledPanelTable = styled(PanelTable)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var HeadCellContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var BodyCellContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", " ", ";\n  ", ";\n"], ["\n  padding: ", " ", ";\n  ", ";\n"])), space(1), space(2), overflowEllipsis);
var StyledPagination = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n"], ["\n  margin: 0 0 ", " 0;\n"])), space(3));
export default TransactionsList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=transactionsList.jsx.map