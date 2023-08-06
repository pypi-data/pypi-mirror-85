import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import { Panel } from 'app/components/panels';
import Pagination from 'app/components/pagination';
import LoadingIndicator from 'app/components/loadingIndicator';
import withOrganization from 'app/utils/withOrganization';
import { decodeScalar } from 'app/utils/queryString';
import space from 'app/styles/space';
import { RadioLineItem } from 'app/views/settings/components/forms/controls/radioGroup';
import Link from 'app/components/links/link';
import Button from 'app/components/button';
import Radio from 'app/components/radio';
import Tooltip from 'app/components/tooltip';
import Count from 'app/components/count';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { formatPercentage, getDuration } from 'app/utils/formatters';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withProjects from 'app/utils/withProjects';
import { IconEllipsis } from 'app/icons';
import MenuItem from 'app/components/menuItem';
import DropdownLink from 'app/components/dropdownLink';
import ProjectAvatar from 'app/components/avatar/projectAvatar';
import withApi from 'app/utils/withApi';
import QuestionTooltip from 'app/components/questionTooltip';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import TrendsDiscoverQuery from './trendsDiscoverQuery';
import Chart from './chart';
import { TrendChangeType, } from './types';
import { trendToColor, transformValueDelta, transformDeltaSpread, modifyTrendView, normalizeTrends, getSelectedQueryKey, getCurrentTrendFunction, getCurrentConfidenceLevel, StyledIconArrow, getTrendProjectId, trendCursorNames, } from './utils';
import { transactionSummaryRouteWithQuery } from '../transactionSummary/utils';
import { HeaderTitleLegend } from '../styles';
import { DisplayModes } from '../transactionSummary/charts';
function onTrendsCursor(trendChangeType) {
    return function onCursor(cursor, path, query, _direction) {
        var cursorQuery = {};
        if (trendChangeType === TrendChangeType.IMPROVED) {
            cursorQuery.improvedCursor = cursor;
        }
        else if (trendChangeType === TrendChangeType.REGRESSION) {
            cursorQuery.regressionCursor = cursor;
        }
        var selectedQueryKey = getSelectedQueryKey(trendChangeType);
        delete query[selectedQueryKey];
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), cursorQuery),
        });
    };
}
function getChartTitle(trendChangeType) {
    switch (trendChangeType) {
        case TrendChangeType.IMPROVED:
            return t('Most Improved Transactions');
        case TrendChangeType.REGRESSION:
            return t('Most Regressed Transactions');
        default:
            throw new Error('No trend type passed');
    }
}
function getSelectedTransaction(location, trendChangeType, transactions) {
    var queryKey = getSelectedQueryKey(trendChangeType);
    var selectedTransactionName = decodeScalar(location.query[queryKey]);
    if (!transactions) {
        return undefined;
    }
    var selectedTransaction = transactions.find(function (transaction) { return transaction.transaction === selectedTransactionName; });
    if (selectedTransaction) {
        return selectedTransaction;
    }
    return transactions.length > 0 ? transactions[0] : undefined;
}
function handleChangeSelected(location, trendChangeType) {
    return function updateSelected(transaction) {
        var selectedQueryKey = getSelectedQueryKey(trendChangeType);
        var query = __assign({}, location.query);
        if (!transaction) {
            delete query[selectedQueryKey];
        }
        else {
            query[selectedQueryKey] = transaction === null || transaction === void 0 ? void 0 : transaction.transaction;
        }
        browserHistory.push({
            pathname: location.pathname,
            query: query,
        });
    };
}
var FilterSymbols;
(function (FilterSymbols) {
    FilterSymbols["GREATER_THAN_EQUALS"] = ">=";
    FilterSymbols["LESS_THAN_EQUALS"] = "<=";
})(FilterSymbols || (FilterSymbols = {}));
function handleFilterTransaction(location, transaction) {
    var queryString = decodeScalar(location.query.query);
    var conditions = tokenizeSearch(queryString || '');
    conditions.addTagValues('!transaction', [transaction]);
    var query = stringifyQueryObject(conditions);
    trackAnalyticsEvent({
        eventKey: 'performance_views.trends.hide_transaction',
        eventName: 'Performance Views: Hide Transaction',
        confidence_level: getCurrentConfidenceLevel(location).label,
    });
    browserHistory.push({
        pathname: location.pathname,
        query: __assign(__assign({}, location.query), { query: String(query).trim() }),
    });
}
function handleSummaryClick(confidenceLevel) {
    trackAnalyticsEvent({
        eventKey: 'performance_views.trends.summary',
        eventName: 'Performance Views: Summary Navigation',
        confidence_level: confidenceLevel,
    });
}
function handleFilterDuration(location, value, symbol) {
    var durationTag = 'transaction.duration';
    var queryString = decodeScalar(location.query.query);
    var conditions = tokenizeSearch(queryString || '');
    var existingValues = conditions.getTagValues(durationTag);
    var alternateSymbol = symbol === FilterSymbols.GREATER_THAN_EQUALS ? '>' : '<';
    existingValues.forEach(function (existingValue) {
        if (existingValue.startsWith(symbol) || existingValue.startsWith(alternateSymbol)) {
            conditions.removeTagValue(durationTag, existingValue);
        }
    });
    conditions.addTagValues(durationTag, ["" + symbol + value]);
    var query = stringifyQueryObject(conditions);
    browserHistory.push({
        pathname: location.pathname,
        query: __assign(__assign({}, location.query), { query: String(query).trim() }),
    });
}
function ChangedTransactions(props) {
    var api = props.api, location = props.location, trendChangeType = props.trendChangeType, previousTrendFunction = props.previousTrendFunction, organization = props.organization, projects = props.projects, setError = props.setError;
    var trendView = props.trendView.clone();
    var chartTitle = getChartTitle(trendChangeType);
    modifyTrendView(trendView, location, trendChangeType);
    var onCursor = onTrendsCursor(trendChangeType);
    var cursor = decodeScalar(location.query[trendCursorNames[trendChangeType]]);
    return (<TrendsDiscoverQuery eventView={trendView} orgSlug={organization.slug} location={location} trendChangeType={trendChangeType} cursor={cursor} limit={5} setError={setError}>
      {function (_a) {
        var isLoading = _a.isLoading, trendsData = _a.trendsData, pageLinks = _a.pageLinks;
        var trendFunction = getCurrentTrendFunction(location);
        var events = normalizeTrends((trendsData && trendsData.events && trendsData.events.data) || []);
        var selectedTransaction = getSelectedTransaction(location, trendChangeType, events);
        var statsData = (trendsData === null || trendsData === void 0 ? void 0 : trendsData.stats) || {};
        var transactionsList = events && events.slice ? events.slice(0, 5) : [];
        var currentTrendFunction = isLoading && previousTrendFunction
            ? previousTrendFunction
            : trendFunction.field;
        var titleTooltipContent = t('This compares the baseline (%s) of the past with the present.', trendFunction.legendLabel);
        return (<TransactionsListContainer>
            <TrendsTransactionPanel>
              <StyledHeaderTitleLegend>
                {chartTitle}{' '}
                <QuestionTooltip size="sm" position="top" title={titleTooltipContent}/>
              </StyledHeaderTitleLegend>
              {isLoading ? (<LoadingIndicator style={{
            margin: '237px auto',
        }}/>) : (<React.Fragment>
                  {transactionsList.length ? (<React.Fragment>
                      <ChartContainer>
                        <Chart statsData={statsData} query={trendView.query} project={trendView.project} environment={trendView.environment} start={trendView.start} end={trendView.end} statsPeriod={trendView.statsPeriod} transaction={selectedTransaction} isLoading={isLoading} {...props}/>
                      </ChartContainer>
                      {transactionsList.map(function (transaction, index) { return (<TrendsListItem api={api} currentTrendFunction={currentTrendFunction} trendView={props.trendView} organization={organization} transaction={transaction} key={transaction.transaction} index={index} trendChangeType={trendChangeType} transactions={transactionsList} location={location} projects={projects} statsData={statsData} handleSelectTransaction={handleChangeSelected(location, trendChangeType)}/>); })}
                    </React.Fragment>) : (<StyledEmptyStateWarning small>
                      {t('No results')}
                    </StyledEmptyStateWarning>)}
                </React.Fragment>)}
            </TrendsTransactionPanel>
            <Pagination pageLinks={pageLinks} onCursor={onCursor}/>
          </TransactionsListContainer>);
    }}
    </TrendsDiscoverQuery>);
}
function TrendsListItem(props) {
    var transaction = props.transaction, transactions = props.transactions, trendChangeType = props.trendChangeType, currentTrendFunction = props.currentTrendFunction, index = props.index, location = props.location, projects = props.projects, handleSelectTransaction = props.handleSelectTransaction;
    var color = trendToColor[trendChangeType].default;
    var selectedTransaction = getSelectedTransaction(location, trendChangeType, transactions);
    var isSelected = selectedTransaction === transaction;
    var project = projects.find(function (_a) {
        var slug = _a.slug;
        return slug === transaction.project;
    });
    var currentPeriodValue = transaction.aggregate_range_2;
    var previousPeriodValue = transaction.aggregate_range_1;
    var absolutePercentChange = formatPercentage(Math.abs(transaction.trend_percentage - 1), 0);
    var previousDuration = getDuration(previousPeriodValue / 1000, previousPeriodValue < 1000 && previousPeriodValue > 10 ? 0 : 2);
    var currentDuration = getDuration(currentPeriodValue / 1000, currentPeriodValue < 1000 && currentPeriodValue > 10 ? 0 : 2);
    var percentChangeExplanation = t('Over this period, the duration for %s has %s %s from %s to %s', currentTrendFunction, trendChangeType === TrendChangeType.IMPROVED ? t('decreased') : t('increased'), absolutePercentChange, previousDuration, currentDuration);
    var longestPeriodValue = trendChangeType === TrendChangeType.IMPROVED
        ? previousPeriodValue
        : currentPeriodValue;
    var longestDuration = trendChangeType === TrendChangeType.IMPROVED ? previousDuration : currentDuration;
    return (<ListItemContainer data-test-id={'trends-list-item-' + trendChangeType}>
      <ItemRadioContainer color={color}>
        <Tooltip title={<TooltipContent>
              <span>{t('Total Events')}</span>
              <span>
                <Count value={transaction.count_range_1}/>
                <StyledIconArrow direction="right" size="xs"/>
                <Count value={transaction.count_range_2}/>
              </span>
            </TooltipContent>}>
          <RadioLineItem index={index} role="radio">
            <Radio checked={isSelected} onChange={function () { return handleSelectTransaction(transaction); }}/>
          </RadioLineItem>
        </Tooltip>
      </ItemRadioContainer>
      <TransactionSummaryLink {...props}/>
      <ItemTransactionPercentage>
        <Tooltip title={percentChangeExplanation}>
          <React.Fragment>
            {trendChangeType === TrendChangeType.REGRESSION ? '+' : ''}
            {formatPercentage(transaction.trend_percentage - 1, 0)}
          </React.Fragment>
        </Tooltip>
      </ItemTransactionPercentage>
      <DropdownLink caret={false} anchorRight title={<StyledButton size="xsmall" icon={<IconEllipsis data-test-id="trends-item-action" size="xs"/>}/>}>
        <MenuItem onClick={function () {
        return handleFilterDuration(location, longestPeriodValue, FilterSymbols.LESS_THAN_EQUALS);
    }}>
          <StyledMenuAction>{t('Show \u2264 %s', longestDuration)}</StyledMenuAction>
        </MenuItem>
        <MenuItem onClick={function () {
        return handleFilterDuration(location, longestPeriodValue, FilterSymbols.GREATER_THAN_EQUALS);
    }}>
          <StyledMenuAction>{t('Show \u2265 %s', longestDuration)}</StyledMenuAction>
        </MenuItem>
        <MenuItem onClick={function () { return handleFilterTransaction(location, transaction.transaction); }}>
          <StyledMenuAction>{t('Hide from list')}</StyledMenuAction>
        </MenuItem>
      </DropdownLink>
      <ItemTransactionDurationChange>
        {project && (<Tooltip title={transaction.project}>
            <ProjectAvatar project={project}/>
          </Tooltip>)}
        <CompareDurations {...props}/>
      </ItemTransactionDurationChange>
      <ItemTransactionStatus color={color}>
        <React.Fragment>
          {transformValueDelta(transaction.trend_difference, trendChangeType)}
        </React.Fragment>
      </ItemTransactionStatus>
    </ListItemContainer>);
}
var CompareDurations = function (props) {
    var transaction = props.transaction;
    return (<DurationChange>
      {transformDeltaSpread(transaction.aggregate_range_1, transaction.aggregate_range_2)}
    </DurationChange>);
};
var TransactionSummaryLink = function (props) {
    var organization = props.organization, eventView = props.trendView, transaction = props.transaction, projects = props.projects, location = props.location, currentTrendFunction = props.currentTrendFunction;
    var confidenceLevel = getCurrentConfidenceLevel(location).label;
    var summaryView = eventView.clone();
    var projectID = getTrendProjectId(transaction, projects);
    var target = transactionSummaryRouteWithQuery({
        orgSlug: organization.slug,
        transaction: String(transaction.transaction),
        query: summaryView.generateQueryStringObject(),
        projectID: projectID,
        display: DisplayModes.TREND,
        trendDisplay: currentTrendFunction,
    });
    return (<ItemTransactionName to={target} onClick={function () { return handleSummaryClick(confidenceLevel); }}>
      {transaction.transaction}
    </ItemTransactionName>);
};
var TransactionsListContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var TrendsTransactionPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n  flex-grow: 1;\n"], ["\n  margin: 0;\n  flex-grow: 1;\n"])));
var ChartContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(3));
var StyledHeaderTitleLegend = styled(HeaderTitleLegend)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 0;\n  margin: ", ";\n"], ["\n  padding: 0;\n  margin: ", ";\n"])), space(3));
var StyledButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
var StyledMenuAction = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  white-space: nowrap;\n  color: ", ";\n"], ["\n  white-space: nowrap;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var StyledEmptyStateWarning = styled(EmptyStateWarning)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  min-height: 300px;\n  justify-content: center;\n"], ["\n  min-height: 300px;\n  justify-content: center;\n"])));
var ListItemContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 24px auto 100px 30px;\n  grid-template-rows: repeat(2, auto);\n  grid-column-gap: ", ";\n  border-top: 1px solid ", ";\n  padding: ", " ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 24px auto 100px 30px;\n  grid-template-rows: repeat(2, auto);\n  grid-column-gap: ", ";\n  border-top: 1px solid ", ";\n  padding: ", " ", ";\n"])), space(1), function (p) { return p.theme.border; }, space(1), space(2));
var ItemRadioContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-row: 1/3;\n  input {\n    cursor: pointer;\n  }\n  input:checked::after {\n    background-color: ", ";\n  }\n"], ["\n  grid-row: 1/3;\n  input {\n    cursor: pointer;\n  }\n  input:checked::after {\n    background-color: ", ";\n  }\n"])), function (p) { return p.color; });
var ItemTransactionName = styled(Link)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-right: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  margin-right: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1), overflowEllipsis);
var ItemTransactionDurationChange = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var DurationChange = styled('span')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  color: ", ";\n  margin: 0 ", ";\n"], ["\n  color: ", ";\n  margin: 0 ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
var ItemTransactionPercentage = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  text-align: right;\n  font-size: ", ";\n"], ["\n  text-align: right;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ItemTransactionStatus = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  text-align: right;\n  font-size: ", ";\n"])), function (p) { return p.color; }, function (p) { return p.theme.fontSizeSmall; });
var TooltipContent = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
export default withApi(withProjects(withOrganization(ChangedTransactions)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=changedTransactions.jsx.map