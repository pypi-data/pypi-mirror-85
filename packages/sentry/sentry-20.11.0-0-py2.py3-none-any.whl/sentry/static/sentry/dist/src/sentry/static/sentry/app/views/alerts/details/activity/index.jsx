import { __assign, __awaiter, __extends, __generator, __read, __rest, __spread } from "tslib";
import React from 'react';
import { createIncidentNote, deleteIncidentNote, fetchIncidentActivities, updateIncidentNote, } from 'app/actionCreators/incident';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
import { DEFAULT_ERROR_JSON } from 'app/constants';
import { uniqueId } from 'app/utils/guid';
import ConfigStore from 'app/stores/configStore';
import withApi from 'app/utils/withApi';
import { IncidentActivityType, } from '../../types';
import Activity from './activity';
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
var ActivityContainer = /** @class */ (function (_super) {
    __extends(ActivityContainer, _super);
    function ActivityContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            noteInputId: uniqueId(),
            noteInputText: '',
            createBusy: false,
            createError: false,
            createErrorJSON: null,
            activities: null,
        };
        _this.handleCreateNote = function (note) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, newActivity, newNote_1, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        newActivity = {
                            comment: note.text,
                            type: IncidentActivityType.COMMENT,
                            dateCreated: new Date().toISOString(),
                            user: ConfigStore.get('user'),
                            id: uniqueId(),
                            incidentIdentifier: alertId,
                        };
                        this.setState(function (state) { return ({
                            createBusy: true,
                            // This is passed as a key to NoteInput that re-mounts
                            // (basically so we can reset text input to empty string)
                            noteInputId: uniqueId(),
                            activities: __spread([newActivity], (state.activities || [])),
                            noteInputText: '',
                        }); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, createIncidentNote(api, orgId, alertId, note)];
                    case 2:
                        newNote_1 = _b.sent();
                        this.setState(function (state) {
                            // Update activities to replace our fake new activity with activity object from server
                            var activities = __spread([
                                newNote_1
                            ], state.activities.filter(function (activity) { return activity !== newActivity; }));
                            return {
                                createBusy: false,
                                activities: activities,
                            };
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState(function (state) {
                            var activities = state.activities.filter(function (activity) { return activity !== newActivity; });
                            return {
                                // We clear the textarea immediately when submitting, restore
                                // value when there has been an error
                                noteInputText: note.text,
                                activities: activities,
                                createBusy: false,
                                createError: true,
                                createErrorJSON: error_1.responseJSON || DEFAULT_ERROR_JSON,
                            };
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.getIndexAndActivityFromState = function (activity) {
            // `index` should probably be found, if not let error hit Sentry
            var index = _this.state.activities !== null
                ? _this.state.activities.findIndex(function (_a) {
                    var id = _a.id;
                    return id === activity.id;
                })
                : '';
            return [index, _this.state.activities[index]];
        };
        _this.handleDeleteNote = function (activity) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, _b, index, oldActivity, error_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b = __read(this.getIndexAndActivityFromState(activity), 2), index = _b[0], oldActivity = _b[1];
                        this.setState(function (state) { return ({
                            activities: removeFromArrayIndex(state.activities, index),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, deleteIncidentNote(api, orgId, alertId, activity.id)];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _c.sent();
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex(state.activities, index, oldActivity),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleUpdateNote = function (note, activity) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, _b, index, oldActivity, error_3;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b = __read(this.getIndexAndActivityFromState(activity), 2), index = _b[0], oldActivity = _b[1];
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex(state.activities, index, __assign(__assign({}, oldActivity), { comment: note.text })),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, updateIncidentNote(api, orgId, alertId, activity.id, note)];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_3 = _c.sent();
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex(state.activities, index, oldActivity),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ActivityContainer.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ActivityContainer.prototype.componentDidUpdate = function (prevProps) {
        // Only refetch if incidentStatus changes.
        //
        // This component can mount before incident details is fully loaded.
        // In which case, `incidentStatus` is null and we will be fetching via `cDM`
        // There's no need to fetch this gets updated due to incident details being loaded
        if (prevProps.incidentStatus !== null &&
            prevProps.incidentStatus !== this.props.incidentStatus) {
            this.fetchData();
        }
    };
    ActivityContainer.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, activities, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchIncidentActivities(api, orgId, alertId)];
                    case 2:
                        activities = _b.sent();
                        this.setState({ activities: activities, loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        this.setState({ loading: false, error: !!err_1 });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ActivityContainer.prototype.render = function () {
        var _a = this.props, api = _a.api, params = _a.params, incident = _a.incident, props = __rest(_a, ["api", "params", "incident"]);
        var alertId = params.alertId;
        var me = ConfigStore.get('user');
        return (<Activity alertId={alertId} me={me} api={api} {...this.state} loading={this.state.loading || !incident} incident={incident} onCreateNote={this.handleCreateNote} onUpdateNote={this.handleUpdateNote} onDeleteNote={this.handleDeleteNote} {...props}/>);
    };
    return ActivityContainer;
}(React.PureComponent));
export default withApi(ActivityContainer);
function removeFromArrayIndex(array, index) {
    var newArray = __spread(array);
    newArray.splice(index, 1);
    return newArray;
}
//# sourceMappingURL=index.jsx.map