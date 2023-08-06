import { __extends } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
var FetchEvent = /** @class */ (function (_super) {
    __extends(FetchEvent, _super);
    function FetchEvent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            event: undefined,
        };
        return _this;
    }
    FetchEvent.prototype.componentDidMount = function () {
        this.fetchData();
    };
    FetchEvent.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugChanged = prevProps.orgSlug !== this.props.orgSlug;
        var eventSlugChanged = prevProps.eventSlug !== this.props.eventSlug;
        if (!this.state.isLoading && (orgSlugChanged || eventSlugChanged)) {
            this.fetchData();
        }
    };
    FetchEvent.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, orgSlug = _a.orgSlug, eventSlug = _a.eventSlug;
        // note: eventSlug is of the form <project-slug>:<event-id>
        var url = "/organizations/" + orgSlug + "/events/" + eventSlug + "/";
        var tableFetchID = Symbol('tableFetchID');
        this.setState({ isLoading: true, tableFetchID: tableFetchID });
        this.props.api
            .requestPromise(url, {
            method: 'GET',
        })
            .then(function (data) {
            if (_this.state.tableFetchID !== tableFetchID) {
                // invariant: a different request was initiated after this request
                return;
            }
            _this.setState({
                isLoading: false,
                tableFetchID: undefined,
                error: null,
                event: data,
            });
        })
            .catch(function (err) {
            var _a, _b;
            _this.setState({
                isLoading: false,
                tableFetchID: undefined,
                error: (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                event: undefined,
            });
        });
    };
    FetchEvent.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, error = _a.error, event = _a.event;
        var childrenProps = {
            isLoading: isLoading,
            error: error,
            event: event,
        };
        return this.props.children(childrenProps);
    };
    return FetchEvent;
}(React.Component));
export default withApi(FetchEvent);
//# sourceMappingURL=fetchEvent.jsx.map