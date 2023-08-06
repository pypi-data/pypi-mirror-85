import { __assign, __read, __spread } from "tslib";
import pick from 'lodash/pick';
import * as qs from 'query-string';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
var DEFAULT_STATUS = 'unresolved';
/**
 * Get query for API given the current location.search string
 */
export function getQuery(search) {
    var query = qs.parse(search);
    var status = typeof query.status !== 'undefined' ? query.status : DEFAULT_STATUS;
    var queryParams = __assign({ status: status }, pick(query, __spread(['cursor'], Object.values(URL_PARAM))));
    return queryParams;
}
//# sourceMappingURL=utils.jsx.map