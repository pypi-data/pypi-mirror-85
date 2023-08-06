import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import groupBy from 'lodash/groupBy';
import moment from 'moment';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ActivityItem from 'app/components/activity/item';
import ErrorBoundary from 'app/components/errorBoundary';
import LoadingError from 'app/components/loadingError';
import Note from 'app/components/activity/note';
import NoteInputWithStorage from 'app/components/activity/note/inputWithStorage';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import { IncidentActivityType } from '../../types';
import ActivityPlaceholder from './activityPlaceholder';
import DateDivider from './dateDivider';
import StatusItem from './statusItem';
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
var Activity = /** @class */ (function (_super) {
    __extends(Activity, _super);
    function Activity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateNote = function (note, _a) {
            var activity = _a.activity;
            var onUpdateNote = _this.props.onUpdateNote;
            onUpdateNote(note, activity);
        };
        _this.handleDeleteNote = function (_a) {
            var activity = _a.activity;
            var onDeleteNote = _this.props.onDeleteNote;
            onDeleteNote(activity);
        };
        return _this;
    }
    Activity.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, error = _a.error, me = _a.me, alertId = _a.alertId, incident = _a.incident, activities = _a.activities, noteInputId = _a.noteInputId, createBusy = _a.createBusy, createError = _a.createError, createErrorJSON = _a.createErrorJSON, onCreateNote = _a.onCreateNote;
        var noteProps = __assign({ minHeight: 80, projectSlugs: (incident && incident.projects) || [] }, this.props.noteInputProps);
        var activitiesByDate = groupBy(activities, function (_a) {
            var dateCreated = _a.dateCreated;
            return moment(dateCreated).format('ll');
        });
        var today = moment().format('ll');
        return (<div>
        <ActivityItem author={{ type: 'user', user: me }}>
          {function () { return (<NoteInputWithStorage key={noteInputId} storageKey="incidentIdinput" itemKey={alertId} onCreate={onCreateNote} busy={createBusy} error={createError} errorJSON={createErrorJSON} placeholder={t('Leave a comment, paste a tweet, or link any other relevant information about this alert...')} {...noteProps}/>); }}
        </ActivityItem>

        {error && <LoadingError message={t('There was a problem loading activities')}/>}

        {loading && (<React.Fragment>
            <ActivityPlaceholder />
            <ActivityPlaceholder />
            <ActivityPlaceholder />
          </React.Fragment>)}

        {!loading &&
            !error &&
            Object.entries(activitiesByDate).map(function (_a) {
                var _b = __read(_a, 2), date = _b[0], activitiesForDate = _b[1];
                var title = date === today ? (t('Today')) : (<React.Fragment>
                  {date} <StyledTimeSince date={date}/>
                </React.Fragment>);
                return (<React.Fragment key={date}>
                <DateDivider>{title}</DateDivider>
                {activitiesForDate &&
                    activitiesForDate.map(function (activity) {
                        var _a, _b;
                        var authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
                        if (activity.type === IncidentActivityType.COMMENT) {
                            return (<ErrorBoundary mini key={"note-" + activity.id}>
                          <Note showTime user={activity.user} modelId={activity.id} text={activity.comment || ''} dateCreated={activity.dateCreated} activity={activity} authorName={authorName} onDelete={_this.handleDeleteNote} onUpdate={_this.handleUpdateNote} {...noteProps}/>
                        </ErrorBoundary>);
                        }
                        else {
                            return (<ErrorBoundary mini key={"note-" + activity.id}>
                          <StatusItem showTime incident={incident} authorName={authorName} activity={activity}/>
                        </ErrorBoundary>);
                        }
                    })}
              </React.Fragment>);
            })}
      </div>);
    };
    return Activity;
}(React.Component));
export default Activity;
var StyledTimeSince = styled(TimeSince)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space(0.5));
var templateObject_1;
//# sourceMappingURL=activity.jsx.map