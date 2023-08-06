import { __assign, __extends, __read } from "tslib";
import React from 'react';
import { isAPIPayloadSimilar, } from 'app/utils/discover/eventView';
/**
 * Generic component for discover queries
 */
var GenericDiscoverQuery = /** @class */ (function (_super) {
    __extends(GenericDiscoverQuery, _super);
    function GenericDiscoverQuery() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            tableData: null,
            pageLinks: null,
        };
        _this._shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.getPayload(_this.props);
            var otherAPIPayload = _this.getPayload(prevProps);
            return (!isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload) ||
                prevProps.limit !== _this.props.limit ||
                prevProps.route !== _this.props.route ||
                prevProps.cursor !== _this.props.cursor);
        };
        _this.fetchData = function () {
            var _a = _this.props, api = _a.api, beforeFetch = _a.beforeFetch, afterFetch = _a.afterFetch, eventView = _a.eventView, orgSlug = _a.orgSlug, route = _a.route, limit = _a.limit, cursor = _a.cursor, setError = _a.setError;
            if (!eventView.isValid()) {
                return;
            }
            var url = "/organizations/" + orgSlug + "/" + route + "/";
            var tableFetchID = Symbol("tableFetchID");
            var apiPayload = _this.getPayload(_this.props);
            _this.setState({ isLoading: true, tableFetchID: tableFetchID });
            setError === null || setError === void 0 ? void 0 : setError(undefined);
            if (limit) {
                apiPayload.per_page = limit;
            }
            if (cursor) {
                apiPayload.cursor = cursor;
            }
            beforeFetch === null || beforeFetch === void 0 ? void 0 : beforeFetch(api);
            api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: __assign({}, apiPayload),
            })
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                if (_this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                var tableData = afterFetch ? afterFetch(data, _this.props) : data;
                _this.setState(function (prevState) {
                    var _a;
                    return ({
                        isLoading: false,
                        tableFetchID: undefined,
                        error: null,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : prevState.pageLinks,
                        tableData: tableData,
                    });
                });
            })
                .catch(function (err) {
                var _a, _b;
                var error = (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null;
                _this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: error,
                    tableData: null,
                });
                if (setError) {
                    setError(error);
                }
            });
        };
        return _this;
    }
    GenericDiscoverQuery.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GenericDiscoverQuery.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading,
        var refetchCondition = !this.state.isLoading && this._shouldRefetchData(prevProps);
        // or if we've moved from an invalid view state to a valid one,
        var eventViewValidation = prevProps.eventView.isValid() === false && this.props.eventView.isValid();
        var shouldRefetchExternal = this.props.shouldRefetchData
            ? this.props.shouldRefetchData(prevProps, this.props)
            : false;
        if (refetchCondition || eventViewValidation || shouldRefetchExternal) {
            this.fetchData();
        }
    };
    GenericDiscoverQuery.prototype.getPayload = function (props) {
        if (this.props.getRequestPayload) {
            return this.props.getRequestPayload(props);
        }
        return props.eventView.getEventsAPIPayload(props.location);
    };
    GenericDiscoverQuery.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData, pageLinks = _a.pageLinks;
        var childrenProps = {
            isLoading: isLoading,
            error: error,
            tableData: tableData,
            pageLinks: pageLinks,
        };
        var children = this.props.children; // Explicitly setting type due to issues with generics and React's children
        return children === null || children === void 0 ? void 0 : children(childrenProps);
    };
    return GenericDiscoverQuery;
}(React.Component));
export default GenericDiscoverQuery;
//# sourceMappingURL=genericDiscoverQuery.jsx.map