import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { metric } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withTags from 'app/utils/withTags';
import Measurements from 'app/utils/measurements/measurements';
import Pagination from 'app/components/pagination';
import { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
import TableView from './tableView';
/**
 * `Table` is a container element that handles 2 things
 * 1. Fetch data from source
 * 2. Handle pagination of data
 *
 * It will pass the data it fetched to `TableView`, where the state of the
 * Table is maintained and controlled
 */
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            pageLinks: null,
            tableData: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getEventsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.fetchData = function () {
            var _a = _this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError, confirmedQuery = _a.confirmedQuery;
            if (!eventView.isValid() || !confirmedQuery) {
                return;
            }
            // note: If the eventView has no aggregates, the endpoint will automatically add the event id in
            // the API payload response
            var url = "/organizations/" + organization.slug + "/eventsv2/";
            var tableFetchID = Symbol('tableFetchID');
            var apiPayload = eventView.getEventsAPIPayload(location);
            setError('', 200);
            _this.setState({ isLoading: true, tableFetchID: tableFetchID });
            metric.mark({ name: "discover-events-start-" + apiPayload.query });
            _this.props.api.clear();
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: apiPayload,
            })
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                // We want to measure this metric regardless of whether we use the result
                metric.measure({
                    name: 'app.api.discover-query',
                    start: "discover-events-start-" + apiPayload.query,
                    data: {
                        status: jqXHR && jqXHR.status,
                    },
                });
                if (_this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState(function (prevState) { return ({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: null,
                    pageLinks: jqXHR ? jqXHR.getResponseHeader('Link') : prevState.pageLinks,
                    tableData: data,
                }); });
            })
                .catch(function (err) {
                var _a;
                metric.measure({
                    name: 'app.api.discover-query',
                    start: "discover-events-start-" + apiPayload.query,
                    data: {
                        status: err.status,
                    },
                });
                var message = ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) || t('An unknown error occurred.');
                _this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: message,
                    pageLinks: null,
                    tableData: null,
                });
                setError(message, err.status);
            });
        };
        return _this;
    }
    Table.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Table.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading, or if we've moved
        // from an invalid view state to a valid one.
        if ((!this.state.isLoading && this.shouldRefetchData(prevProps)) ||
            (prevProps.eventView.isValid() === false && this.props.eventView.isValid()) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, tags = _a.tags;
        var _b = this.state, pageLinks = _b.pageLinks, tableData = _b.tableData, isLoading = _b.isLoading, error = _b.error;
        var tagKeys = Object.values(tags).map(function (_a) {
            var key = _a.key;
            return key;
        });
        return (<Container>
        <Measurements>
          {function (_a) {
            var measurements = _a.measurements;
            var measurementKeys = Object.values(measurements).map(function (_a) {
                var key = _a.key;
                return key;
            });
            return (<TableView {..._this.props} isLoading={isLoading} error={error} eventView={eventView} tableData={tableData} tagKeys={tagKeys} measurementKeys={measurementKeys}/>);
        }}
        </Measurements>
        <Pagination pageLinks={pageLinks}/>
      </Container>);
    };
    return Table;
}(React.PureComponent));
export default withApi(withTags(Table));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  min-width: 0;\n  overflow: hidden;\n"], ["\n  min-width: 0;\n  overflow: hidden;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map