import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import { IconWarning } from 'app/icons';
import { Panel } from 'app/components/panels';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
import { t, tn } from 'app/locale';
import Alert from 'app/components/alert';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import EventView from 'app/utils/discover/eventView';
import SearchBar from 'app/components/searchBar';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { parseTrace, getTraceDateTimeRange } from './utils';
import TraceView from './traceView';
import Filter, { noFilter, toggleFilter, toggleAllFilters, } from './filter';
var SpansInterface = /** @class */ (function (_super) {
    __extends(SpansInterface, _super);
    function SpansInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchQuery: undefined,
            parsedTrace: parseTrace(_this.props.event),
            operationNameFilters: noFilter,
        };
        _this.handleSpanFilter = function (searchQuery) {
            _this.setState({
                searchQuery: searchQuery || undefined,
            });
        };
        _this.toggleOperationNameFilter = function (operationName) {
            _this.setState(function (prevState) { return ({
                operationNameFilters: toggleFilter(prevState.operationNameFilters, operationName),
            }); });
        };
        _this.toggleAllOperationNameFilters = function (operationNames) {
            _this.setState(function (prevState) {
                return {
                    operationNameFilters: toggleAllFilters(prevState.operationNameFilters, operationNames),
                };
            });
        };
        return _this;
    }
    SpansInterface.getDerivedStateFromProps = function (props, state) {
        return __assign(__assign({}, state), { parsedTrace: parseTrace(props.event) });
    };
    SpansInterface.prototype.renderTraceErrorsAlert = function (_a) {
        var isLoading = _a.isLoading, numOfErrors = _a.numOfErrors;
        if (isLoading) {
            return null;
        }
        if (numOfErrors === 0) {
            return null;
        }
        var label = tn('There is an error event associated with this transaction event.', "There are %s error events associated with this transaction event.", numOfErrors);
        return (<AlertContainer>
        <Alert type="error" icon={<IconWarning size="md"/>}>
          {label}
        </Alert>
      </AlertContainer>);
    };
    SpansInterface.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, orgId = _a.orgId, location = _a.location, organization = _a.organization;
        var parsedTrace = this.state.parsedTrace;
        // construct discover query to fetch error events associated with this transaction
        var _b = getTraceDateTimeRange({
            start: parsedTrace.traceStartTimestamp,
            end: parsedTrace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        var conditions = new QueryResults([
            'event.type:error',
            "trace:" + parsedTrace.traceID,
        ]);
        if (typeof event.title === 'string') {
            conditions.setTagValues('transaction', [event.title]);
        }
        var orgFeatures = new Set(organization.features);
        var traceErrorsEventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Errors related to transaction " + parsedTrace.rootSpanID,
            fields: [
                'title',
                'project',
                'timestamp',
                'trace',
                'trace.span',
                'trace.parent_span',
            ],
            orderby: '-timestamp',
            query: stringifyQueryObject(conditions),
            // if an org has no global-views, we make an assumption that errors are collected in the same
            // project as the current transaction event where spans are collected into
            projects: orgFeatures.has('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        return (<div>
        <DiscoverQuery location={location} eventView={traceErrorsEventView} orgSlug={orgId}>
          {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            var spansWithErrors = filterSpansWithErrors(parsedTrace, tableData);
            var numOfErrors = (spansWithErrors === null || spansWithErrors === void 0 ? void 0 : spansWithErrors.data.length) || 0;
            return (<React.Fragment>
                {_this.renderTraceErrorsAlert({
                isLoading: isLoading,
                numOfErrors: numOfErrors,
            })}
                <Search>
                  <Filter parsedTrace={parsedTrace} operationNameFilter={_this.state.operationNameFilters} toggleOperationNameFilter={_this.toggleOperationNameFilter} toggleAllOperationNameFilters={_this.toggleAllOperationNameFilters}/>
                  <StyledSearchBar defaultQuery="" query={_this.state.searchQuery || ''} placeholder={t('Search for spans')} onSearch={_this.handleSpanFilter}/>
                </Search>
                <Panel>
                  <TraceView event={event} searchQuery={_this.state.searchQuery} orgId={orgId} organization={organization} parsedTrace={parsedTrace} spansWithErrors={spansWithErrors} operationNameFilters={_this.state.operationNameFilters}/>
                </Panel>
              </React.Fragment>);
        }}
        </DiscoverQuery>
      </div>);
    };
    SpansInterface.propTypes = {
        event: SentryTypes.Event.isRequired,
        orgId: PropTypes.string.isRequired,
    };
    return SpansInterface;
}(React.Component));
var Search = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var AlertContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
function filterSpansWithErrors(parsedTrace, tableData) {
    var _a;
    if (!tableData) {
        return undefined;
    }
    var data = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) !== null && _a !== void 0 ? _a : [];
    var filtered = data.filter(function (row) {
        var spanId = row['trace.span'] || '';
        if (!spanId) {
            return false;
        }
        if (spanId === parsedTrace.rootSpanID) {
            return true;
        }
        var hasSpan = parsedTrace.spans.findIndex(function (span) {
            return spanId === span.span_id;
        }) >= 0;
        return hasSpan;
    });
    return __assign(__assign({}, tableData), { data: filtered });
}
export default ReactRouter.withRouter(withOrganization(SpansInterface));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map