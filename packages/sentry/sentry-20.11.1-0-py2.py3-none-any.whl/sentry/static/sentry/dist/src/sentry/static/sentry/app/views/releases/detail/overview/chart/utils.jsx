import { getDiffInMinutes } from 'app/components/charts/utils';
import EventView from 'app/utils/discover/eventView';
import { formatVersion } from 'app/utils/formatters';
import { getUtcDateString } from 'app/utils/dates';
import { t } from 'app/locale';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
// In minutes
var FOURTEEN_DAYS = 20160;
export function getInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes > FOURTEEN_DAYS) {
        return '6h';
    }
    else {
        return '1h';
    }
}
export function getReleaseEventView(selection, version) {
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var discoverQuery = {
        id: undefined,
        version: 2,
        name: t('Release') + " " + formatVersion(version),
        fields: ['title', 'count()', 'event.type', 'issue', 'last_seen()'],
        query: stringifyQueryObject(new QueryResults(["release:" + version, '!event.type:transaction'])),
        orderby: '-last_seen',
        range: period,
        environment: environments,
        projects: projects,
        start: start ? getUtcDateString(start) : undefined,
        end: end ? getUtcDateString(end) : undefined,
    };
    return EventView.fromSavedQuery(discoverQuery);
}
//# sourceMappingURL=utils.jsx.map