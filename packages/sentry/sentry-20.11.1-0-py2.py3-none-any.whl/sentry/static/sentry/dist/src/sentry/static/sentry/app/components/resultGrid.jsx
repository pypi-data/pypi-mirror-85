import { __assign, __extends, __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { browserHistory } from 'react-router';
import withApi from 'app/utils/withApi';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import Pagination from 'app/components/pagination';
import { IconSearch } from 'app/icons';
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getSelector = function () { return (<DropdownLink title={_this.getCurrentLabel()}>
      {_this.getDefaultItem()}
      {_this.props.options.map(function (_a) {
            var _b;
            var _c = __read(_a, 2), value = _c[0], label = _c[1];
            var filterQuery = (_b = {},
                _b[_this.props.queryKey] = value,
                _b.cursor = '',
                _b);
            var query = __assign(__assign({}, _this.props.location.query), filterQuery);
            return (<MenuItem key={value} isActive={_this.props.value === value} to={{ pathname: _this.props.path, query: query }}>
            {label}
          </MenuItem>);
        })}
    </DropdownLink>); };
        return _this;
    }
    Filter.prototype.getCurrentLabel = function () {
        var _this = this;
        var selected = this.props.options.find(function (item) { var _a; return item[0] === ((_a = _this.props.value) !== null && _a !== void 0 ? _a : ''); });
        if (selected) {
            return this.props.name + ': ' + selected[1];
        }
        return this.props.name + ': ' + 'Any';
    };
    Filter.prototype.getDefaultItem = function () {
        var query = __assign(__assign({}, this.props.location.query), { cursor: '' });
        delete query[this.props.queryKey];
        return (<MenuItem key="" isActive={this.props.value === '' || !this.props.value} to={{ pathname: this.props.path, query: query }}>
        Any
      </MenuItem>);
    };
    Filter.prototype.render = function () {
        return (<div className="filter-options">
        {this.props.options.length === 1 ? (<strong>{this.getCurrentLabel()}</strong>) : (this.getSelector())}
      </div>);
    };
    return Filter;
}(React.Component));
var SortBy = /** @class */ (function (_super) {
    __extends(SortBy, _super);
    function SortBy() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SortBy.prototype.getCurrentSortLabel = function () {
        var _this = this;
        var _a;
        return (_a = this.props.options.find(function (_a) {
            var _b = __read(_a, 1), value = _b[0];
            return value === _this.props.value;
        })) === null || _a === void 0 ? void 0 : _a[1];
    };
    SortBy.prototype.getSortBySelector = function () {
        var _this = this;
        return (<DropdownLink title={this.getCurrentSortLabel()} className="sorted-by">
        {this.props.options.map(function (_a) {
            var _b = __read(_a, 2), value = _b[0], label = _b[1];
            var query = __assign(__assign({}, _this.props.location.query), { sortBy: value, cursor: '' });
            return (<MenuItem isActive={_this.props.value === value} key={value} to={{ pathname: _this.props.path, query: query }}>
              {label}
            </MenuItem>);
        })}
      </DropdownLink>);
    };
    SortBy.prototype.render = function () {
        if (this.props.options.length === 0) {
            return null;
        }
        return (<div className="sort-options">
        Showing results sorted by
        {this.props.options.length === 1 ? (<strong className="sorted-by">{this.getCurrentSortLabel()}</strong>) : (this.getSortBySelector())}
      </div>);
    };
    SortBy.propTypes = {
        options: PropTypes.array.isRequired,
        path: PropTypes.string.isRequired,
        location: PropTypes.object,
        value: PropTypes.any,
    };
    return SortBy;
}(React.Component));
var ResultGrid = /** @class */ (function (_super) {
    __extends(ResultGrid, _super);
    function ResultGrid() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.defaultState;
        return _this;
    }
    ResultGrid.prototype.componentWillMount = function () {
        this.fetchData();
    };
    ResultGrid.prototype.componentWillReceiveProps = function () {
        var _a, _b;
        var queryParams = this.query;
        this.setState({
            query: (_a = queryParams.query) !== null && _a !== void 0 ? _a : '',
            sortBy: (_b = queryParams.sortBy) !== null && _b !== void 0 ? _b : this.props.defaultSort,
            filters: __assign({}, queryParams),
            pageLinks: null,
            loading: true,
            error: false,
        }, this.fetchData);
    };
    Object.defineProperty(ResultGrid.prototype, "defaultState", {
        get: function () {
            var _a, _b;
            var queryParams = this.query;
            return {
                rows: [],
                loading: true,
                error: false,
                pageLinks: null,
                query: (_a = queryParams.query) !== null && _a !== void 0 ? _a : '',
                sortBy: (_b = queryParams.sortBy) !== null && _b !== void 0 ? _b : this.props.defaultSort,
                filters: __assign({}, queryParams),
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ResultGrid.prototype, "query", {
        get: function () {
            var _a, _b;
            return ((_b = ((_a = this.props.location) !== null && _a !== void 0 ? _a : {}).query) !== null && _b !== void 0 ? _b : {});
        },
        enumerable: false,
        configurable: true
    });
    ResultGrid.prototype.remountComponent = function () {
        this.setState(this.defaultState, this.fetchData);
    };
    ResultGrid.prototype.refresh = function () {
        this.setState({ loading: true }, this.fetchData);
    };
    ResultGrid.prototype.fetchData = function () {
        var _this = this;
        // TODO(dcramer): this should explicitly allow filters/sortBy/cursor/perPage
        var queryParams = __assign(__assign(__assign({}, this.props.defaultParams), { sortBy: this.state.sortBy }), this.query);
        this.props.api.request(this.props.endpoint, {
            method: this.props.method,
            data: queryParams,
            success: function (data, _, jqXHR) {
                var _a;
                _this.setState({
                    loading: false,
                    error: false,
                    rows: data,
                    pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                });
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
    };
    ResultGrid.prototype.onSearch = function (e) {
        var _a, _b;
        var location = (_a = this.props.location) !== null && _a !== void 0 ? _a : {};
        var query = this.state.query;
        var targetQueryParams = __assign(__assign({}, ((_b = location.query) !== null && _b !== void 0 ? _b : {})), { query: query, cursor: '' });
        e.preventDefault();
        browserHistory.push({
            pathname: this.props.path,
            query: targetQueryParams,
        });
    };
    ResultGrid.prototype.onQueryChange = function (evt) {
        this.setState({ query: evt.target.value });
    };
    ResultGrid.prototype.renderLoading = function () {
        return (<tr>
        <td colSpan={this.props.columns.length}>
          <div className="loading">
            <div className="loading-indicator"/>
            <div className="loading-message">Hold on to your butts!</div>
          </div>
        </td>
      </tr>);
    };
    ResultGrid.prototype.renderError = function () {
        return (<tr>
        <td colSpan={this.props.columns.length}>
          <div className="alert-block alert-error">Something bad happened :(</div>
        </td>
      </tr>);
    };
    ResultGrid.prototype.renderNoResults = function () {
        return (<tr>
        <td colSpan={this.props.columns.length}>No results found.</td>
      </tr>);
    };
    ResultGrid.prototype.renderResults = function () {
        var _this = this;
        return this.state.rows.map(function (row) {
            var _a, _b, _c, _d;
            return (<tr key={(_b = (_a = _this.props).keyForRow) === null || _b === void 0 ? void 0 : _b.call(_a, row)}>{(_d = (_c = _this.props).columnsForRow) === null || _d === void 0 ? void 0 : _d.call(_c, row)}</tr>);
        });
    };
    ResultGrid.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var filters = this.props.filters;
        return (<div className="result-grid">
        <div className="table-options">
          {this.props.hasSearch && (<div className="result-grid-search">
              <form onSubmit={this.onSearch}>
                <div className="form-group">
                  <input type="text" className="form-control input-search" placeholder="search" style={{ width: 300 }} name="query" autoComplete="off" value={this.state.query} onChange={this.onQueryChange}/>
                  <button type="submit" className="btn btn-sm btn-primary">
                    <IconSearch size="xs"/>
                  </button>
                </div>
              </form>
            </div>)}
          <SortBy options={(_a = this.props.sortOptions) !== null && _a !== void 0 ? _a : []} value={this.state.sortBy} path={(_b = this.props.path) !== null && _b !== void 0 ? _b : ''} location={this.props.location}/>
          {Object.keys(filters !== null && filters !== void 0 ? filters : {}).map(function (filterKey) {
            var _a;
            return (<Filter key={filterKey} queryKey={filterKey} value={_this.state.filters[filterKey]} path={(_a = _this.props.path) !== null && _a !== void 0 ? _a : ''} location={_this.props.location} {...filters === null || filters === void 0 ? void 0 : filters[filterKey]}/>);
        })}
        </div>

        <table className="table table-grid">
          <thead>
            <tr>{this.props.columns}</tr>
          </thead>
          <tbody>
            {this.state.loading
            ? this.renderLoading()
            : this.state.error
                ? this.renderError()
                : this.state.rows.length === 0
                    ? this.renderNoResults()
                    : this.renderResults()}
          </tbody>
        </table>
        {this.props.hasPagination && this.state.pageLinks && (<Pagination pageLinks={this.state.pageLinks}/>)}
      </div>);
    };
    ResultGrid.defaultProps = {
        path: '',
        endpoint: '',
        method: 'GET',
        columns: [],
        sortOptions: [],
        filters: {},
        defaultSort: '',
        keyForRow: function (row) { return row.id; },
        columnsForRow: function () { return []; },
        defaultParams: {
            per_page: 50,
        },
        hasPagination: true,
        hasSearch: false,
    };
    return ResultGrid;
}(React.Component));
export { ResultGrid };
export default withApi(ResultGrid);
//# sourceMappingURL=resultGrid.jsx.map