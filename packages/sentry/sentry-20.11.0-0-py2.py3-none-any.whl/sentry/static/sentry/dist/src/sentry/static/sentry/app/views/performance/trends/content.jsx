import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { generateAggregateFields } from 'app/utils/discover/fields';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import SearchBar from 'app/views/events/searchBar';
import space from 'app/styles/space';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { decodeScalar } from 'app/utils/queryString';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { getTransactionSearchQuery } from '../utils';
import { TrendChangeType } from './types';
import { DEFAULT_MAX_DURATION, TRENDS_FUNCTIONS, CONFIDENCE_LEVELS, resetCursors, getCurrentTrendFunction, getCurrentConfidenceLevel, getSelectedQueryKey, } from './utils';
import ChangedTransactions from './changedTransactions';
import { FilterViews } from '../landing';
var TrendsContent = /** @class */ (function (_super) {
    __extends(TrendsContent, _super);
    function TrendsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleSearch = function (searchQuery) {
            var location = _this.props.location;
            var cursors = resetCursors();
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign(__assign({}, location.query), cursors), { query: String(searchQuery).trim() || undefined }),
            });
        };
        _this.handleTrendFunctionChange = function (field) {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            var offsets = {};
            Object.values(TrendChangeType).forEach(function (trendChangeType) {
                var queryKey = getSelectedQueryKey(trendChangeType);
                offsets[queryKey] = undefined;
            });
            trackAnalyticsEvent({
                eventKey: 'performance_views.trends.change_function',
                eventName: 'Performance Views: Change Function',
                organization_id: parseInt(organization.id, 10),
                function_name: field,
            });
            _this.setState({
                previousTrendFunction: getCurrentTrendFunction(location).field,
            });
            var cursors = resetCursors();
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign(__assign(__assign({}, location.query), offsets), cursors), { trendFunction: field }),
            });
        };
        _this.handleConfidenceChange = function (label) {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            trackAnalyticsEvent({
                eventKey: 'performance_views.trends.change_confidence',
                eventName: 'Performance Views: Change confidence',
                organization_id: parseInt(organization.id, 10),
                confidence_level: label,
            });
            var cursors = resetCursors();
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign(__assign({}, location.query), cursors), { confidenceLevel: label }),
            });
        };
        return _this;
    }
    TrendsContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, eventView = _a.eventView, location = _a.location, setError = _a.setError;
        var previousTrendFunction = this.state.previousTrendFunction;
        var trendView = eventView.clone();
        var fields = generateAggregateFields(organization, [
            {
                field: 'absolute_correlation()',
            },
            {
                field: 'trend_percentage()',
            },
            {
                field: 'trend_difference()',
            },
            {
                field: 'count_percentage()',
            },
            {
                field: 'tpm()',
            },
            {
                field: 'tps()',
            },
        ], ['epm()', 'eps()']);
        var currentTrendFunction = getCurrentTrendFunction(location);
        var currentConfidenceLevel = getCurrentConfidenceLevel(location);
        var query = getTransactionSearchQuery(location);
        return (<DefaultTrends location={location} eventView={eventView}>
        <StyledSearchContainer>
          <StyledSearchBar organization={organization} projectIds={trendView.project} query={query} fields={fields} onSearch={this.handleSearch}/>
          <TrendsDropdown>
            <DropdownControl buttonProps={{ prefix: t('Confidence') }} label={currentConfidenceLevel.label}>
              {CONFIDENCE_LEVELS.map(function (_a) {
            var label = _a.label;
            return (<DropdownItem key={label} onSelect={_this.handleConfidenceChange} eventKey={label} data-test-id={label} isActive={label === currentConfidenceLevel.label}>
                  {label}
                </DropdownItem>);
        })}
            </DropdownControl>
          </TrendsDropdown>
          <TrendsDropdown>
            <DropdownControl buttonProps={{ prefix: t('Display') }} label={currentTrendFunction.label}>
              {TRENDS_FUNCTIONS.map(function (_a) {
            var label = _a.label, field = _a.field;
            return (<DropdownItem key={field} onSelect={_this.handleTrendFunctionChange} eventKey={field} data-test-id={field} isActive={field === currentTrendFunction.field}>
                  {label}
                </DropdownItem>);
        })}
            </DropdownControl>
          </TrendsDropdown>
        </StyledSearchContainer>
        <TrendsLayoutContainer>
          <ChangedTransactions trendChangeType={TrendChangeType.IMPROVED} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={setError}/>
          <ChangedTransactions trendChangeType={TrendChangeType.REGRESSION} previousTrendFunction={previousTrendFunction} trendView={trendView} location={location} setError={setError}/>
        </TrendsLayoutContainer>
      </DefaultTrends>);
    };
    return TrendsContent;
}(React.Component));
var DefaultTrends = /** @class */ (function (_super) {
    __extends(DefaultTrends, _super);
    function DefaultTrends() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasPushedDefaults = false;
        return _this;
    }
    DefaultTrends.prototype.render = function () {
        var _a = this.props, children = _a.children, location = _a.location, eventView = _a.eventView;
        var queryString = decodeScalar(location.query.query);
        var conditions = tokenizeSearch(queryString || '');
        if (queryString || this.hasPushedDefaults) {
            this.hasPushedDefaults = true;
            return <React.Fragment>{children}</React.Fragment>;
        }
        else {
            this.hasPushedDefaults = true;
            conditions.setTagValues('tpm()', ['>0.01']);
            conditions.setTagValues('transaction.duration', ['>0', "<" + DEFAULT_MAX_DURATION]);
        }
        var query = stringifyQueryObject(conditions);
        eventView.query = query;
        browserHistory.push({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { cursor: undefined, query: String(query).trim() || undefined, view: FilterViews.TRENDS }),
        });
        return null;
    };
    return DefaultTrends;
}(React.Component));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"])), space(2));
var TrendsDropdown = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n  flex-grow: 0;\n"], ["\n  margin-left: ", ";\n  flex-grow: 0;\n"])), space(1));
var StyledSearchContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var TrendsLayoutContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(0, 1fr));\n    align-items: stretch;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(0, 1fr));\n    align-items: stretch;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; });
export default withGlobalSelection(TrendsContent);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=content.jsx.map