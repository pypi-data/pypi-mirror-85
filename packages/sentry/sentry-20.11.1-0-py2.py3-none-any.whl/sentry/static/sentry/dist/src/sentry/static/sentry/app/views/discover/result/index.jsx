import { __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import throttle from 'lodash/throttle';
import { t } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
import BarChart from 'app/components/charts/barChart';
import LineChart from 'app/components/charts/lineChart';
import PageHeading from 'app/components/pageHeading';
import { IconEdit } from 'app/icons';
import { getChartData, getChartDataByDay, getRowsPageRange, downloadAsCsv, getVisualization, } from './utils';
import Table from './table';
import Pagination from './pagination';
import VisualizationsToggle from './visualizationsToggle';
import { HeadingContainer, ResultSummary, ResultContainer, ResultInnerContainer, ChartWrapper, ChartNote, SavedQueryAction, ResultSummaryAndButtons, } from '../styles';
import { NUMBER_OF_SERIES_BY_DAY } from '../data';
import { queryHasChanged, getQueryFromQueryString, getQueryStringFromQuery, } from '../utils';
var Result = /** @class */ (function (_super) {
    __extends(Result, _super);
    function Result(props) {
        var _this = _super.call(this, props) || this;
        _this.setDimensions = function (ref) {
            _this.container = ref;
            if (ref && _this.state.height === null) {
                _this.updateDimensions();
            }
        };
        _this.updateDimensions = function () {
            if (!_this.container) {
                return;
            }
            _this.setState({
                height: _this.container.clientHeight,
                width: _this.container.clientWidth,
            });
        };
        _this.throttledUpdateDimensions = throttle(_this.updateDimensions, 200, { trailing: true });
        _this.handleToggleVisualizations = function (opt) {
            var location = _this.props.location;
            _this.setState({
                view: opt,
            });
            var search = getQueryStringFromQuery(getQueryFromQueryString(location.search), {
                visualization: opt,
            });
            browserHistory.push({
                pathname: location.pathname,
                search: search,
            });
        };
        _this.state = {
            view: getVisualization(props.data, props.location.query.visualization),
            height: null,
            width: null,
        };
        return _this;
    }
    Result.prototype.componentDidMount = function () {
        window.addEventListener('resize', this.throttledUpdateDimensions);
    };
    Result.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        var data = nextProps.data, location = nextProps.location;
        var visualization = getVisualization(data, location.query.visualization);
        if (queryHasChanged(this.props.location.search, nextProps.location.search)) {
            var search = getQueryStringFromQuery(getQueryFromQueryString(location.search), {
                visualization: visualization,
            });
            this.setState({ view: visualization });
            browserHistory.replace({
                pathname: location.pathname,
                search: search,
            });
        }
    };
    Result.prototype.componentWillUnmount = function () {
        window.removeEventListener('resize', this.throttledUpdateDimensions);
    };
    Result.prototype.renderToggle = function () {
        var _a = this.props.data, baseQuery = _a.baseQuery, byDayQuery = _a.byDayQuery;
        var options = [{ id: 'table', name: t('Table') }];
        if (baseQuery.query.aggregations.length) {
            options.push({ id: 'line', name: t('Line') }, { id: 'bar', name: t('Bar') });
        }
        if (byDayQuery.data) {
            options.push({ id: 'line-by-day', name: t('Line by Day') }, { id: 'bar-by-day', name: t('Bar by Day') });
        }
        var handleCsvDownload = function () { return downloadAsCsv(baseQuery.data); };
        return (<div>
        <VisualizationsToggle options={options} handleChange={this.handleToggleVisualizations} handleCsvDownload={handleCsvDownload} visualization={this.state.view}/>
      </div>);
    };
    Result.prototype.renderSummary = function () {
        var _a = this.props.data, baseQuery = _a.baseQuery, byDayQuery = _a.byDayQuery;
        var baseViews = ['table', 'line', 'bar'];
        var summaryData = baseViews.includes(this.state.view)
            ? baseQuery.data
            : byDayQuery.data;
        var summary = [
            "query time: " + getDynamicText({
                value: summaryData.timing.duration_ms,
                fixed: '10',
            }) + "ms",
        ];
        if (this.state.view === 'table') {
            summary.push(getRowsPageRange(baseQuery));
        }
        return <ResultSummary>{summary.join(', ')}</ResultSummary>;
    };
    Result.prototype.renderNote = function () {
        return (<ChartNote>{t("Displaying up to " + NUMBER_OF_SERIES_BY_DAY + " results")}</ChartNote>);
    };
    Result.prototype.renderSavedQueryHeader = function () {
        return (<React.Fragment>
        <PageHeading>
          {getDynamicText({ value: this.props.savedQuery.name, fixed: 'saved query' })}
        </PageHeading>
        <SavedQueryAction to="" onClick={this.props.onToggleEdit}>
          <IconEdit />
        </SavedQueryAction>
      </React.Fragment>);
    };
    Result.prototype.renderQueryResultHeader = function () {
        return <PageHeading>{t('Result')}</PageHeading>;
    };
    Result.prototype.render = function () {
        var _a = this.props, _b = _a.data, baseQuery = _b.baseQuery, byDayQuery = _b.byDayQuery, savedQuery = _a.savedQuery, onFetchPage = _a.onFetchPage, utc = _a.utc;
        var view = this.state.view;
        var basicChartData = getChartData(baseQuery.data.data, baseQuery.query);
        var byDayChartData = byDayQuery.data && getChartDataByDay(byDayQuery.data.data, byDayQuery.query);
        var legendData = byDayChartData
            ? { data: byDayChartData.map(function (entry) { return entry.seriesName; }), truncate: 80 }
            : undefined;
        var tooltipOptions = {
            filter: function (value) { return value !== null; },
            truncate: 80,
        };
        return (<ResultContainer data-test-id="result">
        <div>
          <HeadingContainer>
            {savedQuery ? this.renderSavedQueryHeader() : this.renderQueryResultHeader()}
          </HeadingContainer>
          {this.renderToggle()}
        </div>
        <ResultInnerContainer ref={this.setDimensions}>
          {view === 'table' && (<Table data={baseQuery.data} query={baseQuery.query} height={this.state.height} width={this.state.width}/>)}
          {view === 'line' && (<ChartWrapper>
              <LineChart series={basicChartData} height={300} tooltip={tooltipOptions} legend={{ data: [baseQuery.query.aggregations[0][2]], truncate: 80 }} xAxis={{ truncate: 80 }} renderer="canvas"/>
            </ChartWrapper>)}
          {view === 'bar' && (<ChartWrapper>
              <BarChart series={basicChartData} height={300} tooltip={tooltipOptions} legend={{ data: [baseQuery.query.aggregations[0][2]], truncate: 80 }} xAxis={{ truncate: 80 }} renderer="canvas" options={{ animation: false }}/>
            </ChartWrapper>)}
          {view === 'line-by-day' && (<ChartWrapper>
              <LineChart series={byDayChartData} height={300} tooltip={tooltipOptions} legend={legendData} renderer="canvas" isGroupedByDate utc={utc}/>
              {this.renderNote()}
            </ChartWrapper>)}
          {view === 'bar-by-day' && (<ChartWrapper>
              <BarChart series={byDayChartData} stacked height={300} tooltip={tooltipOptions} legend={legendData} renderer="canvas" isGroupedByDate utc={utc !== null && utc !== undefined ? utc : undefined} options={{ animation: false }}/>
              {this.renderNote()}
            </ChartWrapper>)}
          <ResultSummaryAndButtons>
            {this.renderSummary()}
            {!baseQuery.query.aggregations.length && (<Pagination previous={baseQuery.previous} next={baseQuery.next} getNextPage={function () {
            onFetchPage('next');
        }} getPreviousPage={function () {
            onFetchPage('previous');
        }}/>)}
          </ResultSummaryAndButtons>
        </ResultInnerContainer>
      </ResultContainer>);
    };
    return Result;
}(React.Component));
export default Result;
//# sourceMappingURL=index.jsx.map