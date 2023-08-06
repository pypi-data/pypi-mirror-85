import moment from 'moment';
/**
 * Given a snoozed unix timestamp in seconds, returns the number of days since
 * the prompt was snoozed.
 *
 * @param snoozedTs Snoozed timestamp
 */
export function snoozedDays(snoozedTs) {
    var now = moment.utc();
    var snoozedDay = moment.unix(snoozedTs).utc();
    return now.diff(snoozedDay, 'days');
}
//# sourceMappingURL=promptsActivity.jsx.map