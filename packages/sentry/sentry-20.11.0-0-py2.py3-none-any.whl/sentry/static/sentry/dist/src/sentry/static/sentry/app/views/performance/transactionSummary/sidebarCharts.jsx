import { __assign, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ChartZoom from 'app/components/charts/chartZoom';
import LineChart from 'app/components/charts/lineChart';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import QuestionTooltip from 'app/components/questionTooltip';
import { SectionHeading } from 'app/components/charts/styles';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import TransitionChart from 'app/components/charts/transitionChart';
import { getInterval } from 'app/components/charts/utils';
import { IconWarning } from 'app/icons';
import { getTermHelp } from 'app/views/performance/data';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { formatAbbreviatedNumber, formatFloat, formatPercentage, } from 'app/utils/formatters';
import { tooltipFormatter } from 'app/utils/discover/charts';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
function SidebarCharts(_a) {
    var api = _a.api, eventView = _a.eventView, organization = _a.organization, router = _a.router;
    var statsPeriod = eventView.statsPeriod;
    var start = eventView.start ? getUtcToLocalDateObject(eventView.start) : undefined;
    var end = eventView.end ? getUtcToLocalDateObject(eventView.end) : undefined;
    var utc = decodeScalar(router.location.query.utc);
    var colors = theme.charts.getColorPalette(3);
    var axisLineConfig = {
        scale: true,
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        splitLine: {
            show: false,
        },
    };
    var chartOptions = {
        height: 580,
        grid: [
            {
                top: '40px',
                left: '10px',
                right: '10px',
                height: '120px',
            },
            {
                top: '230px',
                left: '10px',
                right: '10px',
                height: '150px',
            },
            {
                top: '450px',
                left: '10px',
                right: '10px',
                height: '120px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1, 2] }],
        },
        xAxes: Array.from(new Array(3)).map(function (_i, index) { return ({
            gridIndex: index,
            type: 'time',
            show: false,
        }); }),
        yAxes: [
            __assign({ 
                // apdex
                gridIndex: 0, axisLabel: {
                    formatter: function (value) { return formatFloat(value, 1); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
            __assign({ 
                // throughput
                gridIndex: 1, axisLabel: {
                    formatter: formatAbbreviatedNumber,
                    color: theme.chartLabel,
                } }, axisLineConfig),
            __assign({ 
                // failure rate
                gridIndex: 2, axisLabel: {
                    formatter: function (value) { return formatPercentage(value, 0); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
        ],
        utc: utc,
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1], colors[2]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: tooltipFormatter,
            nameFormatter: function (value) {
                return value === 'epm()' ? 'tpm()' : value;
            },
        },
    };
    var datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    var project = eventView.project;
    var environment = eventView.environment;
    return (<RelativeBox>
      <ChartTitle top="0px" key="apdex">
        {t('Apdex')}
        <QuestionTooltip position="top" title={getTermHelp(organization, 'apdex')} size="sm"/>
      </ChartTitle>

      <ChartTitle top="190px" key="throughput">
        {t('TPM')}
        <QuestionTooltip position="top" title={getTermHelp(organization, 'tpm')} size="sm"/>
      </ChartTitle>

      <ChartTitle top="410px" key="failure-rate">
        {t('Failure Rate')}
        <QuestionTooltip position="top" title={getTermHelp(organization, 'failureRate')} size="sm"/>
      </ChartTitle>

      <ChartZoom router={router} period={statsPeriod} projects={project} environments={environment} xAxisIndex={[0, 1, 2]}>
        {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={__spread(project)} environment={__spread(environment)} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={eventView.query} includePrevious={false} yAxis={["apdex(" + organization.apdexThreshold + ")", 'epm()', 'failure_rate()']}>
            {function (_a) {
        var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
        if (errored) {
            return (<ErrorPanel>
                    <IconWarning color="gray300" size="lg"/>
                  </ErrorPanel>);
        }
        var series = results
            ? results.map(function (values, i) { return (__assign(__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); })
            : [];
        return (<TransitionChart loading={loading} reloading={reloading} height="550px">
                  <TransparentLoadingMask visible={reloading}/>
                  <LineChart {...zoomRenderProps} {...chartOptions} series={series}/>
                </TransitionChart>);
    }}
          </EventsRequest>); }}
      </ChartZoom>
    </RelativeBox>);
}
var RelativeBox = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  margin-bottom: ", ";\n"], ["\n  position: relative;\n  margin-bottom: ", ";\n"])), space(1));
var ChartTitle = styled(SectionHeading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  position: absolute;\n  top: ", ";\n  margin: 0;\n  z-index: 1;\n"], ["\n  background: ", ";\n  position: absolute;\n  top: ", ";\n  margin: 0;\n  z-index: 1;\n"])), function (p) { return p.theme.background; }, function (p) { return p.top; });
export default withApi(ReactRouter.withRouter(SidebarCharts));
var templateObject_1, templateObject_2;
//# sourceMappingURL=sidebarCharts.jsx.map