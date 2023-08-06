export var AlertRuleThreshold;
(function (AlertRuleThreshold) {
    AlertRuleThreshold[AlertRuleThreshold["INCIDENT"] = 0] = "INCIDENT";
    AlertRuleThreshold[AlertRuleThreshold["RESOLUTION"] = 1] = "RESOLUTION";
})(AlertRuleThreshold || (AlertRuleThreshold = {}));
export var AlertRuleThresholdType;
(function (AlertRuleThresholdType) {
    AlertRuleThresholdType[AlertRuleThresholdType["ABOVE"] = 0] = "ABOVE";
    AlertRuleThresholdType[AlertRuleThresholdType["BELOW"] = 1] = "BELOW";
})(AlertRuleThresholdType || (AlertRuleThresholdType = {}));
export var Dataset;
(function (Dataset) {
    Dataset["ERRORS"] = "events";
    Dataset["TRANSACTIONS"] = "transactions";
})(Dataset || (Dataset = {}));
export var EventTypes;
(function (EventTypes) {
    EventTypes["DEFAULT"] = "default";
    EventTypes["ERROR"] = "error";
    EventTypes["TRANSACTION"] = "transaction";
})(EventTypes || (EventTypes = {}));
export var Datasource;
(function (Datasource) {
    Datasource["ERROR_DEFAULT"] = "error_default";
    Datasource["DEFAULT"] = "default";
    Datasource["ERROR"] = "error";
    Datasource["TRANSACTION"] = "transaction";
})(Datasource || (Datasource = {}));
export var TimePeriod;
(function (TimePeriod) {
    TimePeriod["SIX_HOURS"] = "6h";
    TimePeriod["ONE_DAY"] = "1d";
    TimePeriod["THREE_DAYS"] = "3d";
    // Seven days is actually 10080m but we have a max of 10000 events
    TimePeriod["SEVEN_DAYS"] = "10000m";
    TimePeriod["FOURTEEN_DAYS"] = "14d";
    TimePeriod["THIRTY_DAYS"] = "30d";
})(TimePeriod || (TimePeriod = {}));
export var TimeWindow;
(function (TimeWindow) {
    TimeWindow[TimeWindow["ONE_MINUTE"] = 1] = "ONE_MINUTE";
    TimeWindow[TimeWindow["FIVE_MINUTES"] = 5] = "FIVE_MINUTES";
    TimeWindow[TimeWindow["TEN_MINUTES"] = 10] = "TEN_MINUTES";
    TimeWindow[TimeWindow["FIFTEEN_MINUTES"] = 15] = "FIFTEEN_MINUTES";
    TimeWindow[TimeWindow["THIRTY_MINUTES"] = 30] = "THIRTY_MINUTES";
    TimeWindow[TimeWindow["ONE_HOUR"] = 60] = "ONE_HOUR";
    TimeWindow[TimeWindow["TWO_HOURS"] = 120] = "TWO_HOURS";
    TimeWindow[TimeWindow["FOUR_HOURS"] = 240] = "FOUR_HOURS";
    TimeWindow[TimeWindow["ONE_DAY"] = 1440] = "ONE_DAY";
})(TimeWindow || (TimeWindow = {}));
export var ActionType;
(function (ActionType) {
    ActionType["EMAIL"] = "email";
    ActionType["SLACK"] = "slack";
    ActionType["PAGERDUTY"] = "pagerduty";
    ActionType["MSTEAMS"] = "msteams";
    ActionType["SENTRY_APP"] = "sentry_app";
})(ActionType || (ActionType = {}));
export var TargetType;
(function (TargetType) {
    // A direct reference, like an email address, Slack channel, or PagerDuty service
    TargetType["SPECIFIC"] = "specific";
    // A specific user. This could be used to grab the user's email address.
    TargetType["USER"] = "user";
    // A specific team. This could be used to send an email to everyone associated with a team.
    TargetType["TEAM"] = "team";
    // A Sentry App instead of any of the above.
    TargetType["SENTRY_APP"] = "sentry_app";
})(TargetType || (TargetType = {}));
//# sourceMappingURL=types.jsx.map