import { __assign, __read, __rest, __spread } from "tslib";
import * as qs from 'query-string';
import { getExternal, getInternal } from 'app/views/discover/aggregations/utils';
import { getQueryStringFromQuery } from 'app/views/discover/utils';
export function getDiscoverUrlPathFromDiscoverQuery(_a) {
    var organization = _a.organization, selection = _a.selection, query = _a.query;
    var datetime = selection.datetime, _environments = selection.environments, restSelection = __rest(selection, ["datetime", "environments"]);
    // Discover does not support importing these
    var _groupby = query.groupby, _rollup = query.rollup, _name = query.name, orderby = query.orderby, restQuery = __rest(query, ["groupby", "rollup", "name", "orderby"]);
    var orderbyTimeIndex = orderby === null || orderby === void 0 ? void 0 : orderby.indexOf('time');
    var visual = orderbyTimeIndex === -1 ? 'table' : 'line-by-day';
    var aggregations = query.aggregations.map(function (aggregation) {
        return getExternal(getInternal(aggregation));
    });
    var _b = __read((aggregations.length && aggregations[0]) || [], 3), aggregationAlias = _b[2];
    // Discover expects the aggregation aliases to be in a specific format
    var discoverOrderby = "" + (orderbyTimeIndex === 0 ? '' : '-') + (aggregationAlias || '');
    return "/organizations/" + organization.slug + "/discover/" + getQueryStringFromQuery(__assign(__assign(__assign({}, restQuery), restSelection), { start: datetime.start, end: datetime.end, range: datetime.period, limit: 1000, aggregations: aggregations, orderby: discoverOrderby })) + "&visualization=" + visual;
}
export function getDiscover2UrlPathFromDiscoverQuery(_a) {
    var _b;
    var organization = _a.organization, selection = _a.selection, d1Query = _a.query;
    var d2Query = {
        name: d1Query.name,
        field: __spread(['title'], d1Query.fields),
        sort: d1Query.orderby,
        statsPeriod: (_b = selection === null || selection === void 0 ? void 0 : selection.datetime) === null || _b === void 0 ? void 0 : _b.period,
        query: '',
    };
    var queryQueries = (d1Query.conditions || []).map(function (c) {
        var tag = c[0] || '';
        var val = c[2] || '';
        var operator = c[1] || '';
        var isNot = operator.includes('!') || operator.includes('NOT');
        var isNull = operator.includes('NULL');
        var isLike = operator.includes('LIKE') || operator.includes('*');
        var hasSpace = val.includes(' ');
        // Put condition into the columns
        if (!d2Query.field.includes(tag)) {
            d2Query.field.push(tag);
        }
        // Build the query
        var q = [];
        if (isNot) {
            q.push('!');
        }
        q.push(tag);
        q.push(':');
        // Quote open
        if (isNull || hasSpace) {
            q.push('"');
        }
        // Wildcard open
        if (isLike) {
            q.push('*');
        }
        q.push(val);
        // Wildcard close
        if (isLike) {
            q.push('*');
        }
        // Quote close
        if (isNull || hasSpace) {
            q.push('"');
        }
        return q.join('');
    });
    d2Query.field.push('count()');
    d2Query.query = queryQueries.join(' ');
    return "/organizations/" + organization.slug + "/discover/results/?" + qs.stringify(d2Query);
}
//# sourceMappingURL=getDiscoverUrlPathFromDiscoverQuery.jsx.map