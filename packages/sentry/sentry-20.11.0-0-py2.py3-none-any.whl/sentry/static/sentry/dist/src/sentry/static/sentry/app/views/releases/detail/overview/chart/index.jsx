import React from 'react';
import { Panel } from 'app/components/panels';
import EventsChart from 'app/components/charts/eventsChart';
import { t } from 'app/locale';
import ReleaseChartControls, { YAxis } from './releaseChartControls';
import HealthChartContainer from './healthChartContainer';
import { getReleaseEventView } from './utils';
var ReleaseChartContainer = function (_a) {
    var loading = _a.loading, errored = _a.errored, reloading = _a.reloading, chartData = _a.chartData, chartSummary = _a.chartSummary, selection = _a.selection, yAxis = _a.yAxis, onYAxisChange = _a.onYAxisChange, router = _a.router, organization = _a.organization, hasHealthData = _a.hasHealthData, location = _a.location, api = _a.api, version = _a.version, hasDiscover = _a.hasDiscover;
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
    var eventView = getReleaseEventView(selection, version);
    return (<Panel>
      {hasDiscover && yAxis === YAxis.EVENTS ? (<EventsChart router={router} organization={organization} showLegend yAxis={eventView.getYAxis()} query={eventView.getEventsAPIPayload(location).query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} disablePrevious disableReleases currentSeriesName={t('Events')}/>) : (<HealthChartContainer loading={loading} errored={errored} reloading={reloading} chartData={chartData} selection={selection} yAxis={yAxis} router={router}/>)}

      <ReleaseChartControls summary={chartSummary} yAxis={yAxis} onYAxisChange={onYAxisChange} hasDiscover={hasDiscover} hasHealthData={hasHealthData}/>
    </Panel>);
};
export default ReleaseChartContainer;
//# sourceMappingURL=index.jsx.map