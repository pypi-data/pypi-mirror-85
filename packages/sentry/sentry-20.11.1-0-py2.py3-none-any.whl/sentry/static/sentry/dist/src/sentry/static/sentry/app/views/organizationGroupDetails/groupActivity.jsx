import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { createNote, deleteNote, updateNote } from 'app/actionCreators/group';
import { t } from 'app/locale';
import { uniqueId } from 'app/utils/guid';
import ActivityAuthor from 'app/components/activity/author';
import ActivityItem from 'app/components/activity/item';
import ConfigStore from 'app/stores/configStore';
import ErrorBoundary from 'app/components/errorBoundary';
import Note from 'app/components/activity/note';
import NoteInputWithStorage from 'app/components/activity/note/inputWithStorage';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import { DEFAULT_ERROR_JSON } from 'app/constants';
import GroupActivityItem from './groupActivityItem';
var GroupActivity = /** @class */ (function (_super) {
    __extends(GroupActivity, _super);
    function GroupActivity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // TODO(dcramer): only re-render on group/activity change
        _this.state = {
            createBusy: false,
            error: false,
            errorJSON: null,
            inputId: uniqueId(),
        };
        _this.handleNoteDelete = function (_a) {
            var modelId = _a.modelId, oldText = _a.text;
            return __awaiter(_this, void 0, void 0, function () {
                var _b, api, group, _err_1;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _b = this.props, api = _b.api, group = _b.group;
                            addLoadingMessage(t('Removing comment...'));
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, deleteNote(api, group, modelId, oldText)];
                        case 2:
                            _c.sent();
                            clearIndicators();
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _c.sent();
                            addErrorMessage(t('Failed to delete comment'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        /**
         * Note: This is nearly the same logic as `app/views/alerts/details/activity`
         * This can be abstracted a bit if we create more objects that can have activities
         */
        _this.handleNoteCreate = function (note) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, group, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group;
                        this.setState({
                            createBusy: true,
                        });
                        addLoadingMessage(t('Posting comment...'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, createNote(api, group, note)];
                    case 2:
                        _b.sent();
                        this.setState({
                            createBusy: false,
                            // This is used as a `key` to Note Input so that after successful post
                            // we reset the value of the input
                            inputId: uniqueId(),
                        });
                        clearIndicators();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            createBusy: false,
                            error: true,
                            errorJSON: error_1.responseJSON || DEFAULT_ERROR_JSON,
                        });
                        addErrorMessage(t('Unable to post comment'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleNoteUpdate = function (note, _a) {
            var modelId = _a.modelId, oldText = _a.text;
            return __awaiter(_this, void 0, void 0, function () {
                var _b, api, group, error_2;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _b = this.props, api = _b.api, group = _b.group;
                            addLoadingMessage(t('Updating comment...'));
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, updateNote(api, group, note, modelId, oldText)];
                        case 2:
                            _c.sent();
                            clearIndicators();
                            return [3 /*break*/, 4];
                        case 3:
                            error_2 = _c.sent();
                            this.setState({
                                error: true,
                                errorJSON: error_2.responseJSON || DEFAULT_ERROR_JSON,
                            });
                            addErrorMessage(t('Unable to update comment'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    GroupActivity.prototype.render = function () {
        var _this = this;
        var group = this.props.group;
        var me = ConfigStore.get('user');
        var projectSlugs = group && group.project ? [group.project.slug] : [];
        var noteProps = {
            minHeight: 140,
            group: group,
            projectSlugs: projectSlugs,
            placeholder: t('Add details or updates to this event. \nTag users with @, or teams with #'),
        };
        return (<div className="row">
        <div className="col-md-9">
          <div>
            <ActivityItem author={{ type: 'user', user: me }}>
              {function () { return (<NoteInputWithStorage key={_this.state.inputId} storageKey="groupinput:latest" itemKey={group.id} onCreate={_this.handleNoteCreate} busy={_this.state.createBusy} error={_this.state.error} errorJSON={_this.state.errorJSON} {...noteProps}/>); }}
            </ActivityItem>

            {group.activity.map(function (item) {
            var authorName = item.user ? item.user.name : 'Sentry';
            if (item.type === 'note') {
                return (<ErrorBoundary mini key={"note-" + item.id}>
                    <Note showTime={false} text={item.data.text} modelId={item.id} user={item.user} dateCreated={item.dateCreated} authorName={authorName} onDelete={_this.handleNoteDelete} onUpdate={_this.handleNoteUpdate} {...noteProps}/>
                  </ErrorBoundary>);
            }
            else {
                return (<ErrorBoundary mini key={"item-" + item.id}>
                    <ActivityItem author={{ type: item.user ? 'user' : 'system', user: item.user }} date={item.dateCreated} header={<GroupActivityItem author={<ActivityAuthor>{authorName}</ActivityAuthor>} item={item} orgSlug={_this.props.params.orgId} projectId={group.project.id}/>}/>
                  </ErrorBoundary>);
            }
        })}
          </div>
        </div>
      </div>);
    };
    return GroupActivity;
}(React.Component));
export { GroupActivity };
export default withApi(withOrganization(GroupActivity));
//# sourceMappingURL=groupActivity.jsx.map