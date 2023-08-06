import { __assign, __read, __spread } from "tslib";
/**
 * Generate a URL to the events page for a discover query that
 * contains a condition.
 *
 * @param {Object} query The discover query object
 * @param {String[]} values A list of strings that represent field values
 *   e.g. if the query has multiple fields (browser, device), values could be ["Chrome", "iPhone"]
 * @return {String} Returns a url to the "events" page with any discover conditions tranformed to search query syntax
 */
import zipWith from 'lodash/zipWith';
import { OPERATOR } from 'app/views/discover/data';
import { escapeQuotes } from 'app/components/events/interfaces/utils';
import { getEventsUrlPathFromDiscoverQuery } from './getEventsUrlPathFromDiscoverQuery';
export function getEventsUrlFromDiscoverQueryWithConditions(_a) {
    var values = _a.values, query = _a.query, selection = _a.selection, organization = _a.organization;
    return getEventsUrlPathFromDiscoverQuery({
        organization: organization,
        selection: selection,
        query: __assign(__assign({}, query), { conditions: __spread(query.conditions, zipWith(query.fields, values, function (field, value) {
                return [
                    field,
                    OPERATOR.EQUAL,
                    value === null ? '""' : "\"" + escapeQuotes(value) + "\"",
                ];
            })) }),
    });
}
//# sourceMappingURL=getEventsUrlFromDiscoverQueryWithConditions.jsx.map