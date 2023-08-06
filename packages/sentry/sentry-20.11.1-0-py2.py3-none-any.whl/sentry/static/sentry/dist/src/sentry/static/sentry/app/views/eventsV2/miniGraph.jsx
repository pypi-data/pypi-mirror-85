import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import withApi from 'app/utils/withApi';
import EventsRequest from 'app/components/charts/eventsRequest';
import AreaChart from 'app/components/charts/areaChart';
import { getInterval } from 'app/components/charts/utils';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import LoadingIndicator from 'app/components/loadingIndicator';
import LoadingContainer from 'app/components/loading/loadingContainer';
import { IconWarning } from 'app/icons';
import theme from 'app/utils/theme';
var MiniGraph = /** @class */ (function (_super) {
    __extends(MiniGraph, _super);
    function MiniGraph() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MiniGraph.prototype.shouldComponentUpdate = function (nextProps) {
        // We pay for the cost of the deep comparison here since it is cheaper
        // than the cost for rendering the graph, which can take ~200ms to ~300ms to
        // render.
        return !isEqual(this.getRefreshProps(this.props), this.getRefreshProps(nextProps));
    };
    MiniGraph.prototype.getRefreshProps = function (props) {
        // get props that are relevant to the API payload for the graph
        var organization = props.organization, location = props.location, eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(location);
        var query = apiPayload.query;
        var start = apiPayload.start ? getUtcToLocalDateObject(apiPayload.start) : null;
        var end = apiPayload.end ? getUtcToLocalDateObject(apiPayload.end) : null;
        var period = apiPayload.statsPeriod;
        return {
            organization: organization,
            apiPayload: apiPayload,
            query: query,
            start: start,
            end: end,
            period: period,
            project: eventView.project,
            environment: eventView.environment,
            yAxis: eventView.getYAxis(),
        };
    };
    MiniGraph.prototype.render = function () {
        var api = this.props.api;
        var _a = this.getRefreshProps(this.props), query = _a.query, start = _a.start, end = _a.end, period = _a.period, organization = _a.organization, project = _a.project, environment = _a.environment, yAxis = _a.yAxis;
        var colors = theme.charts.getColorPalette(1);
        return (<EventsRequest organization={organization} api={api} query={query} start={start} end={end} period={period} interval={getInterval({ start: start, end: end, period: period }, true)} project={project} environment={environment} includePrevious={false} yAxis={yAxis}>
        {function (_a) {
            var loading = _a.loading, timeseriesData = _a.timeseriesData, errored = _a.errored;
            if (errored) {
                return (<StyledGraphContainer>
                <IconWarning color="gray300" size="md"/>
              </StyledGraphContainer>);
            }
            if (loading) {
                return (<StyledGraphContainer>
                <LoadingIndicator mini/>
              </StyledGraphContainer>);
            }
            var data = (timeseriesData || []).map(function (series) { return (__assign(__assign({}, series), { areaStyle: {
                    color: colors[0],
                    opacity: 1,
                }, lineStyle: {
                    opacity: 0,
                }, smooth: true })); });
            return (<AreaChart height={100} series={__spread(data)} xAxis={{
                show: false,
                axisPointer: {
                    show: false,
                },
            }} yAxis={{
                show: true,
                axisLine: {
                    show: false,
                },
                axisLabel: {
                    color: theme.chartLabel,
                    fontFamily: theme.text.family,
                    fontSize: 12,
                    formatter: function (value) { return axisLabelFormatter(value, yAxis, true); },
                    inside: true,
                    showMinLabel: false,
                    showMaxLabel: false,
                },
                splitNumber: 3,
                splitLine: {
                    show: false,
                },
                zlevel: theme.zIndex.header,
            }} tooltip={{
                show: false,
            }} toolBox={{
                show: false,
            }} grid={{
                left: 0,
                top: 0,
                right: 0,
                bottom: 0,
                containLabel: false,
            }}/>);
        }}
      </EventsRequest>);
    };
    return MiniGraph;
}(React.Component));
var StyledGraphContainer = styled(function (props) { return (<LoadingContainer {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
export default withApi(MiniGraph);
var templateObject_1;
//# sourceMappingURL=miniGraph.jsx.map