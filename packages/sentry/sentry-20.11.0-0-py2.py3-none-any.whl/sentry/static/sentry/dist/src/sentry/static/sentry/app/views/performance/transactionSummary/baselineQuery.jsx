import { __assign, __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import withApi from 'app/utils/withApi';
var BaselineQuery = /** @class */ (function (_super) {
    __extends(BaselineQuery, _super);
    function BaselineQuery() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            fetchID: undefined,
            error: null,
            results: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.generatePayload(_this.props.eventView);
            var otherAPIPayload = _this.generatePayload(prevProps.eventView);
            return !isEqual(thisAPIPayload, otherAPIPayload);
        };
        _this.fetchData = function () {
            var _a = _this.props, eventView = _a.eventView, orgSlug = _a.orgSlug;
            if (!eventView.isValid()) {
                return;
            }
            var url = "/organizations/" + orgSlug + "/event-baseline/";
            var fetchID = Symbol('fetchID');
            _this.setState({ isLoading: true, fetchID: fetchID });
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                query: __assign(__assign({}, eventView.getGlobalSelectionQuery()), { query: eventView.query }),
            })
                .then(function (data) {
                if (_this.state.fetchID !== fetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState({
                    isLoading: false,
                    fetchID: undefined,
                    error: null,
                    results: data,
                });
            })
                .catch(function (err) {
                var _a, _b;
                _this.setState({
                    isLoading: false,
                    fetchID: undefined,
                    error: (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                    results: null,
                });
            });
        };
        return _this;
    }
    BaselineQuery.prototype.componentDidMount = function () {
        this.fetchData();
    };
    BaselineQuery.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading,
        var refetchCondition = !this.state.isLoading && this.shouldRefetchData(prevProps);
        if (refetchCondition) {
            this.fetchData();
        }
    };
    BaselineQuery.prototype.generatePayload = function (eventView) {
        return __assign(__assign({}, eventView.getGlobalSelectionQuery()), { query: eventView.query });
    };
    BaselineQuery.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, error = _a.error, results = _a.results;
        var childrenProps = {
            isLoading: isLoading,
            error: error,
            results: results,
        };
        return this.props.children(childrenProps);
    };
    return BaselineQuery;
}(React.PureComponent));
export default withApi(BaselineQuery);
//# sourceMappingURL=baselineQuery.jsx.map