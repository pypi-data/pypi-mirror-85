import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import * as ReactRouter from 'react-router';
import debounce from 'lodash/debounce';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import LoadingIndicator from 'app/components/loadingIndicator';
/**
 * This is a search input that can be easily used in AsyncComponent/Views.
 *
 * It probably doesn't make too much sense outside of an AsyncComponent atm.
 */
var AsyncComponentSearchInput = /** @class */ (function (_super) {
    __extends(AsyncComponentSearchInput, _super);
    function AsyncComponentSearchInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: '',
            busy: false,
        };
        _this.immediateQuery = function (searchQuery) { return __awaiter(_this, void 0, void 0, function () {
            var _a, location, api, _b, data, jqXHR, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, location = _a.location, api = _a.api;
                        this.setState({ busy: true });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("" + this.props.url, {
                                includeAllArgs: true,
                                method: 'GET',
                                query: __assign(__assign({}, location.query), { query: searchQuery }),
                            })];
                    case 2:
                        _b = __read.apply(void 0, [_d.sent(), 3]), data = _b[0], jqXHR = _b[2];
                        // only update data if the request's query matches the current query
                        if (this.state.query === searchQuery) {
                            this.props.onSuccess(data, jqXHR);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        this.props.onError();
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.query = debounce(_this.immediateQuery, _this.props.debounceWait);
        _this.handleChange = function (query) {
            _this.query(query);
            _this.setState({ query: query });
        };
        _this.handleInputChange = function (evt) {
            return _this.handleChange(evt.target.value);
        };
        /**
         * This is called when "Enter" (more specifically a form "submit" event) is pressed.
         */
        _this.handleSearch = function (evt) {
            var _a = _this.props, updateRoute = _a.updateRoute, onSearchSubmit = _a.onSearchSubmit;
            evt.preventDefault();
            // Update the URL to reflect search term.
            if (updateRoute) {
                var _b = _this.props, router = _b.router, location_1 = _b.location;
                router.push({
                    pathname: location_1.pathname,
                    query: {
                        query: _this.state.query,
                    },
                });
            }
            if (typeof onSearchSubmit !== 'function') {
                return;
            }
            onSearchSubmit(_this.state.query, evt);
        };
        return _this;
    }
    AsyncComponentSearchInput.prototype.render = function () {
        var _a = this.props, placeholder = _a.placeholder, children = _a.children, className = _a.className;
        var _b = this.state, busy = _b.busy, query = _b.query;
        var defaultSearchBar = (<Form onSubmit={this.handleSearch}>
        <Input value={query} onChange={this.handleInputChange} className={className} placeholder={placeholder}/>
        {busy && <StyledLoadingIndicator size={18} hideMessage mini/>}
      </Form>);
        return children === undefined
            ? defaultSearchBar
            : children({ defaultSearchBar: defaultSearchBar, busy: busy, value: query, handleChange: this.handleChange });
    };
    AsyncComponentSearchInput.defaultProps = {
        placeholder: t('Search...'),
        debounceWait: 200,
    };
    return AsyncComponentSearchInput;
}(React.Component));
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  right: 25px;\n  top: 50%;\n  transform: translateY(-13px);\n"], ["\n  position: absolute;\n  right: 25px;\n  top: 50%;\n  transform: translateY(-13px);\n"])));
var Form = styled('form')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
export default ReactRouter.withRouter(AsyncComponentSearchInput);
var templateObject_1, templateObject_2;
//# sourceMappingURL=asyncComponentSearchInput.jsx.map