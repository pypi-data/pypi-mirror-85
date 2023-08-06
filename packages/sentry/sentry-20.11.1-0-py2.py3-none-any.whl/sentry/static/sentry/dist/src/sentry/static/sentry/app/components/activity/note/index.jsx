import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ActivityItem from 'app/components/activity/item';
import space from 'app/styles/space';
import EditorTools from './editorTools';
import NoteBody from './body';
import NoteHeader from './header';
import NoteInput from './input';
var Note = /** @class */ (function (_super) {
    __extends(Note, _super);
    function Note() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            editing: false,
        };
        _this.handleEdit = function () {
            _this.setState({ editing: true });
        };
        _this.handleEditFinish = function () {
            _this.setState({ editing: false });
        };
        _this.handleDelete = function () {
            var onDelete = _this.props.onDelete;
            onDelete(_this.props);
        };
        _this.handleCreate = function (note) {
            var onCreate = _this.props.onCreate;
            if (onCreate) {
                onCreate(note);
            }
        };
        _this.handleUpdate = function (note) {
            var onUpdate = _this.props.onUpdate;
            onUpdate(note, _this.props);
            _this.setState({ editing: false });
        };
        return _this;
    }
    Note.prototype.render = function () {
        var _this = this;
        var _a = this.props, modelId = _a.modelId, user = _a.user, dateCreated = _a.dateCreated, text = _a.text, authorName = _a.authorName, hideDate = _a.hideDate, minHeight = _a.minHeight, showTime = _a.showTime, projectSlugs = _a.projectSlugs;
        var activityItemProps = {
            hideDate: hideDate,
            showTime: showTime,
            id: "activity-item-" + modelId,
            author: {
                type: 'user',
                user: user,
            },
            date: dateCreated,
        };
        if (!this.state.editing) {
            return (<ActivityItemWithEditing {...activityItemProps} header={<NoteHeader authorName={authorName} user={user} onEdit={this.handleEdit} onDelete={this.handleDelete}/>}>
          <NoteBody text={text}/>
        </ActivityItemWithEditing>);
        }
        // When editing, `NoteInput` has its own header, pass render func
        // to control rendering of bubble body
        return (<StyledActivityItem {...activityItemProps}>
        {function () { return (<NoteInput modelId={modelId} minHeight={minHeight} text={text} onEditFinish={_this.handleEditFinish} onUpdate={_this.handleUpdate} onCreate={_this.handleCreate} projectSlugs={projectSlugs}/>); }}
      </StyledActivityItem>);
    };
    return Note;
}(React.Component));
var StyledActivityItem = styled(ActivityItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* this was nested under \".activity-note.activity-bubble\" */\n  ul {\n    list-style: disc;\n  }\n\n  h1,\n  h2,\n  h3,\n  h4,\n  p,\n  ul:not(.nav),\n  ol,\n  pre,\n  hr,\n  blockquote {\n    margin-bottom: ", ";\n  }\n\n  ul:not(.nav),\n  ol {\n    padding-left: 20px;\n  }\n\n  p {\n    a {\n      word-wrap: break-word;\n    }\n  }\n\n  blockquote {\n    font-size: 15px;\n    background: ", ";\n\n    p:last-child {\n      margin-bottom: 0;\n    }\n  }\n"], ["\n  /* this was nested under \".activity-note.activity-bubble\" */\n  ul {\n    list-style: disc;\n  }\n\n  h1,\n  h2,\n  h3,\n  h4,\n  p,\n  ul:not(.nav),\n  ol,\n  pre,\n  hr,\n  blockquote {\n    margin-bottom: ", ";\n  }\n\n  ul:not(.nav),\n  ol {\n    padding-left: 20px;\n  }\n\n  p {\n    a {\n      word-wrap: break-word;\n    }\n  }\n\n  blockquote {\n    font-size: 15px;\n    background: ", ";\n\n    p:last-child {\n      margin-bottom: 0;\n    }\n  }\n"])), space(2), function (p) { return p.theme.gray200; });
var ActivityItemWithEditing = styled(StyledActivityItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  &:hover {\n    ", " {\n      display: inline-block;\n    }\n  }\n"], ["\n  &:hover {\n    ", " {\n      display: inline-block;\n    }\n  }\n"])), EditorTools);
export default Note;
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map