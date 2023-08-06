import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import EventsChart from 'app/components/charts/eventsChart';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel } from 'app/components/panels';
import getDynamicText from 'app/utils/getDynamicText';
import { TOP_N, DisplayModes } from 'app/utils/discover/types';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import ChartFooter from './chartFooter';
var ResultsChart = /** @class */ (function (_super) {
    __extends(ResultsChart, _super);
    function ResultsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResultsChart.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, eventView = _a.eventView, restProps = __rest(_a, ["eventView"]);
        var nextEventView = nextProps.eventView, restNextProps = __rest(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView)) {
            return true;
        }
        return !isEqual(restProps, restNextProps);
    };
    ResultsChart.prototype.render = function () {
        var _a = this.props, api = _a.api, eventView = _a.eventView, location = _a.location, organization = _a.organization, router = _a.router, confirmedQuery = _a.confirmedQuery;
        var yAxisValue = eventView.getYAxis();
        var globalSelection = eventView.getGlobalSelection();
        var start = globalSelection.datetime.start
            ? getUtcToLocalDateObject(globalSelection.datetime.start)
            : null;
        var end = globalSelection.datetime.end
            ? getUtcToLocalDateObject(globalSelection.datetime.end)
            : null;
        var utc = getParams(location.query).utc;
        var apiPayload = eventView.getEventsAPIPayload(location);
        var display = eventView.getDisplayMode();
        var isTopEvents = display === DisplayModes.TOP5 || display === DisplayModes.DAILYTOP5;
        var isPeriod = display === DisplayModes.DEFAULT || display === DisplayModes.TOP5;
        var isDaily = display === DisplayModes.DAILYTOP5 || display === DisplayModes.DAILY;
        var isPrevious = display === DisplayModes.PREVIOUS;
        return (<React.Fragment>
        {getDynamicText({
            value: (<EventsChart api={api} router={router} query={apiPayload.query} organization={organization} showLegend yAxis={yAxisValue} projects={globalSelection.projects} environments={globalSelection.environments} start={start} end={end} period={globalSelection.datetime.period} disablePrevious={!isPrevious} disableReleases={!isPeriod} field={isTopEvents ? apiPayload.field : undefined} interval={eventView.interval} showDaily={isDaily} topEvents={isTopEvents ? TOP_N : undefined} orderby={isTopEvents ? decodeScalar(apiPayload.sort) : undefined} utc={utc === 'true'} confirmedQuery={confirmedQuery}/>),
            fixed: 'events chart',
        })}
      </React.Fragment>);
    };
    return ResultsChart;
}(React.Component));
var ResultsChartContainer = /** @class */ (function (_super) {
    __extends(ResultsChartContainer, _super);
    function ResultsChartContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResultsChartContainer.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, eventView = _a.eventView, restProps = __rest(_a, ["eventView"]);
        var nextEventView = nextProps.eventView, restNextProps = __rest(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView) ||
            this.props.confirmedQuery !== nextProps.confirmedQuery) {
            return true;
        }
        return !isEqual(restProps, restNextProps);
    };
    ResultsChartContainer.prototype.render = function () {
        var _a = this.props, api = _a.api, eventView = _a.eventView, location = _a.location, router = _a.router, total = _a.total, onAxisChange = _a.onAxisChange, onDisplayChange = _a.onDisplayChange, organization = _a.organization, confirmedQuery = _a.confirmedQuery;
        var yAxisValue = eventView.getYAxis();
        var hasQueryFeature = organization.features.includes('discover-query');
        var displayOptions = eventView.getDisplayOptions().filter(function (opt) {
            // top5 modes are only available with larger packages in saas.
            // We remove instead of disable here as showing tooltips in dropdown
            // menus is clunky.
            if ([DisplayModes.TOP5, DisplayModes.DAILYTOP5].includes(opt.value) &&
                !hasQueryFeature) {
                return false;
            }
            return true;
        });
        return (<StyledPanel>
        <ResultsChart api={api} eventView={eventView} location={location} organization={organization} router={router} confirmedQuery={confirmedQuery}/>
        <ChartFooter total={total} yAxisValue={yAxisValue} yAxisOptions={eventView.getYAxisOptions()} onAxisChange={onAxisChange} displayOptions={displayOptions} displayMode={eventView.getDisplayMode()} onDisplayChange={onDisplayChange}/>
      </StyledPanel>);
    };
    return ResultsChartContainer;
}(React.Component));
export default withApi(ResultsChartContainer);
export var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1;
//# sourceMappingURL=resultsChart.jsx.map