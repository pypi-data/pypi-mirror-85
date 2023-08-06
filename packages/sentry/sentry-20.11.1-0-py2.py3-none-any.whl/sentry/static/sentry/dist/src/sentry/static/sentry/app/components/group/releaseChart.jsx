import React from 'react';
import MiniBarChart from 'app/components/charts/miniBarChart';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import { formatVersion } from 'app/utils/formatters';
import SidebarSection from './sidebarSection';
function GroupReleaseChart(props) {
    var className = props.className, group = props.group, lastSeen = props.lastSeen, firstSeen = props.firstSeen, statsPeriod = props.statsPeriod, release = props.release, releaseStats = props.releaseStats, environment = props.environment, environmentStats = props.environmentStats, title = props.title;
    var stats = group.stats[statsPeriod];
    if (!stats || !stats.length) {
        return null;
    }
    var series = [];
    // Add all events.
    series.push({
        seriesName: t('Events'),
        data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
    });
    // Get the timestamp of the first point.
    var firstTime = series[0].data[0].value;
    if (environment && environmentStats) {
        series.push({
            seriesName: t('Events in %s', environment),
            data: environmentStats[statsPeriod].map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
        });
    }
    if (release && releaseStats) {
        series.push({
            seriesName: t('Events in release %s', formatVersion(release.version)),
            data: releaseStats[statsPeriod].map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
        });
    }
    var markers = [];
    if (firstSeen) {
        var firstSeenX = new Date(firstSeen).getTime();
        if (firstSeenX >= firstTime) {
            markers.push({
                name: t('First seen'),
                value: firstSeenX,
                color: theme.pink300,
            });
        }
    }
    if (lastSeen) {
        var lastSeenX = new Date(lastSeen).getTime();
        if (lastSeenX >= firstTime) {
            markers.push({
                name: t('Last seen'),
                value: lastSeenX,
                color: theme.green300,
            });
        }
    }
    return (<SidebarSection secondary title={title} className={className}>
      <MiniBarChart isGroupedByDate showTimeInTooltip height={42} series={series} markers={markers}/>
    </SidebarSection>);
}
export default GroupReleaseChart;
//# sourceMappingURL=releaseChart.jsx.map