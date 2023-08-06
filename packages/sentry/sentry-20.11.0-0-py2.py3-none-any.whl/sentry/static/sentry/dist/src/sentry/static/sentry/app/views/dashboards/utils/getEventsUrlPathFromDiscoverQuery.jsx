import { __assign, __rest } from "tslib";
import pickBy from 'lodash/pickBy';
import * as qs from 'query-string';
import { getUtcDateString } from 'app/utils/dates';
import { getDiscoverConditionsToSearchString } from './getDiscoverConditionsToSearchString';
export function getEventsUrlPathFromDiscoverQuery(_a) {
    var organization = _a.organization, selection = _a.selection, query = _a.query;
    var projects = selection.projects, datetime = selection.datetime, _environments = selection.environments, restSelection = __rest(selection, ["projects", "datetime", "environments"]);
    return "/organizations/" + organization.slug + "/events/?" + qs.stringify(pickBy(__assign(__assign({}, restSelection), { project: projects, start: datetime.start && getUtcDateString(datetime.start), end: datetime.end && getUtcDateString(datetime.end), statsPeriod: datetime.period, query: getDiscoverConditionsToSearchString(query.conditions) })));
}
//# sourceMappingURL=getEventsUrlPathFromDiscoverQuery.jsx.map