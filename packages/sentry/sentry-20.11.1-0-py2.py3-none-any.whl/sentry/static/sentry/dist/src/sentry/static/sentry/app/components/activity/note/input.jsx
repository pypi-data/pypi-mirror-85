import { __extends, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import { MentionsInput, Mention } from 'react-mentions';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ConfigStore from 'app/stores/configStore';
import NavTabs from 'app/components/navTabs';
import { IconMarkdown } from 'app/icons';
import marked from 'app/utils/marked';
import space from 'app/styles/space';
import textStyles from 'app/styles/text';
import Mentionables from './mentionables';
import mentionStyle from './mentionStyle';
var defaultProps = {
    placeholder: t('Add a comment.\nTag users with @, or teams with #'),
    minHeight: 140,
    busy: false,
};
var NoteInput = /** @class */ (function (_super) {
    __extends(NoteInput, _super);
    function NoteInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            preview: false,
            value: _this.props.text || '',
            memberMentions: [],
            teamMentions: [],
        };
        _this.handleToggleEdit = function () {
            _this.setState({ preview: false });
        };
        _this.handleTogglePreview = function () {
            _this.setState({ preview: true });
        };
        _this.handleSubmit = function (e) {
            e.preventDefault();
            _this.submitForm();
        };
        _this.handleChange = function (e) {
            _this.setState({ value: e.target.value });
            if (_this.props.onChange) {
                _this.props.onChange(e, { updating: !!_this.props.modelId });
            }
        };
        _this.handleKeyDown = function (e) {
            // Auto submit the form on [meta] + Enter
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                _this.submitForm();
            }
        };
        _this.handleCancel = function (e) {
            e.preventDefault();
            _this.finish();
        };
        _this.handleAddMember = function (id, display) {
            _this.setState(function (_a) {
                var memberMentions = _a.memberMentions;
                return ({
                    memberMentions: __spread(memberMentions, [["" + id, display]]),
                });
            });
        };
        _this.handleAddTeam = function (id, display) {
            _this.setState(function (_a) {
                var teamMentions = _a.teamMentions;
                return ({
                    teamMentions: __spread(teamMentions, [["" + id, display]]),
                });
            });
        };
        return _this;
    }
    NoteInput.prototype.cleanMarkdown = function (text) {
        return text
            .replace(/\[sentry\.strip:member\]/g, '@')
            .replace(/\[sentry\.strip:team\]/g, '');
    };
    NoteInput.prototype.submitForm = function () {
        if (!!this.props.modelId) {
            this.update();
            return;
        }
        this.create();
    };
    NoteInput.prototype.create = function () {
        var onCreate = this.props.onCreate;
        if (onCreate) {
            onCreate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    };
    NoteInput.prototype.update = function () {
        var onUpdate = this.props.onUpdate;
        if (onUpdate) {
            onUpdate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    };
    NoteInput.prototype.finish = function () {
        this.props.onEditFinish && this.props.onEditFinish();
    };
    NoteInput.prototype.finalizeMentions = function () {
        var _this = this;
        var _a = this.state, memberMentions = _a.memberMentions, teamMentions = _a.teamMentions;
        // each mention looks like [id, display]
        return __spread(memberMentions, teamMentions).filter(function (mention) { return _this.state.value.indexOf(mention[1]) !== -1; })
            .map(function (mention) { return mention[0]; });
    };
    NoteInput.prototype.render = function () {
        var _a = this.state, preview = _a.preview, value = _a.value;
        var _b = this.props, modelId = _b.modelId, busy = _b.busy, placeholder = _b.placeholder, minHeight = _b.minHeight, errorJSON = _b.errorJSON, memberList = _b.memberList, teams = _b.teams;
        var existingItem = !!modelId;
        var btnText = existingItem ? t('Save Comment') : t('Post Comment');
        var errorMessage = (errorJSON &&
            (typeof errorJSON.detail === 'string'
                ? errorJSON.detail
                : (errorJSON.detail && errorJSON.detail.message) ||
                    t('Unable to post comment'))) ||
            null;
        return (<NoteInputForm data-test-id="note-input-form" noValidate onSubmit={this.handleSubmit}>
        <NoteInputNavTabs>
          <NoteInputNavTab className={!preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleToggleEdit}>
              {existingItem ? t('Edit') : t('Write')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <NoteInputNavTab className={preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleTogglePreview}>
              {t('Preview')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <MarkdownTab>
            <IconMarkdown />
            <MarkdownSupported>{t('Markdown supported')}</MarkdownSupported>
          </MarkdownTab>
        </NoteInputNavTabs>

        <NoteInputBody>
          {preview ? (<NotePreview minHeight={minHeight} dangerouslySetInnerHTML={{ __html: marked(this.cleanMarkdown(value)) }}/>) : (<MentionsInput style={mentionStyle({ minHeight: minHeight })} placeholder={placeholder} onChange={this.handleChange} onKeyDown={this.handleKeyDown} value={value} required autoFocus>
              <Mention trigger="@" data={memberList} onAdd={this.handleAddMember} displayTransform={function (_id, display) { return "@" + display; }} markup="**[sentry.strip:member]__display__**" appendSpaceOnAdd/>
              <Mention trigger="#" data={teams} onAdd={this.handleAddTeam} markup="**[sentry.strip:team]__display__**" appendSpaceOnAdd/>
            </MentionsInput>)}
        </NoteInputBody>

        <Footer>
          <div>{errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}</div>
          <div>
            {existingItem && (<FooterButton priority="danger" type="button" onClick={this.handleCancel}>
                {t('Cancel')}
              </FooterButton>)}
            <FooterButton error={errorMessage} type="submit" disabled={busy}>
              {btnText}
            </FooterButton>
          </div>
        </Footer>
      </NoteInputForm>);
    };
    return NoteInput;
}(React.Component));
var NoteInputContainer = /** @class */ (function (_super) {
    __extends(NoteInputContainer, _super);
    function NoteInputContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderInput = function (_a) {
            var members = _a.members, teams = _a.teams;
            var _b = _this.props, _ = _b.projectSlugs, props = __rest(_b, ["projectSlugs"]);
            return <NoteInput memberList={members} teams={teams} {...props}/>;
        };
        return _this;
    }
    NoteInputContainer.prototype.render = function () {
        var projectSlugs = this.props.projectSlugs;
        var me = ConfigStore.get('user');
        return (<Mentionables me={me} projectSlugs={projectSlugs}>
        {this.renderInput}
      </Mentionables>);
    };
    NoteInputContainer.defaultProps = defaultProps;
    return NoteInputContainer;
}(React.Component));
export default NoteInputContainer;
// This styles both the note preview and the note editor input
var getNotePreviewCss = function (p) {
    var _a = mentionStyle(p)['&multiLine'].input, minHeight = _a.minHeight, padding = _a.padding, overflow = _a.overflow, border = _a.border;
    return "\n  max-height: 1000px;\n  max-width: 100%;\n  " + ((minHeight && "min-height: " + minHeight + "px") || '') + ";\n  padding: " + padding + ";\n  overflow: " + overflow + ";\n  border: " + border + ";\n";
};
var getNoteInputErrorStyles = function (p) {
    if (!p.error) {
        return '';
    }
    return "\n  color: " + p.theme.error + ";\n  margin: -1px;\n  border: 1px solid " + p.theme.error + ";\n  border-radius: " + p.theme.borderRadius + ";\n\n    &:before {\n      display: block;\n      content: '';\n      width: 0;\n      height: 0;\n      border-top: 7px solid transparent;\n      border-bottom: 7px solid transparent;\n      border-right: 7px solid " + p.theme.red300 + ";\n      position: absolute;\n      left: -7px;\n      top: 12px;\n    }\n\n    &:after {\n      display: block;\n      content: '';\n      width: 0;\n      height: 0;\n      border-top: 6px solid transparent;\n      border-bottom: 6px solid transparent;\n      border-right: 6px solid #fff;\n      position: absolute;\n      left: -5px;\n      top: 12px;\n    }\n  ";
};
var NoteInputForm = styled('form')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 15px;\n  line-height: 22px;\n  transition: padding 0.2s ease-in-out;\n\n  ", "\n"], ["\n  font-size: 15px;\n  line-height: 22px;\n  transition: padding 0.2s ease-in-out;\n\n  ", "\n"])), getNoteInputErrorStyles);
var NoteInputBody = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), textStyles);
var Footer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  border-top: 1px solid ", ";\n  justify-content: space-between;\n  transition: opacity 0.2s ease-in-out;\n  padding-left: ", ";\n"], ["\n  display: flex;\n  border-top: 1px solid ", ";\n  justify-content: space-between;\n  transition: opacity 0.2s ease-in-out;\n  padding-left: ", ";\n"])), function (p) { return p.theme.border; }, space(1.5));
var FooterButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 13px;\n  margin: -1px -1px -1px;\n  border-radius: 0 0 ", ";\n\n  ", "\n"], ["\n  font-size: 13px;\n  margin: -1px -1px -1px;\n  border-radius: 0 0 ", ";\n\n  ",
    "\n"])), function (p) { return p.theme.borderRadius; }, function (p) {
    return p.error &&
        "\n  &, &:active, &:focus, &:hover {\n  border-bottom-color: " + p.theme.error + ";\n  border-right-color: " + p.theme.error + ";\n  }\n  ";
});
var ErrorMessage = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  color: ", ";\n  font-size: 0.9em;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  color: ", ";\n  font-size: 0.9em;\n"])), function (p) { return p.theme.error; });
var NoteInputNavTabs = styled(NavTabs)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  margin-bottom: 0;\n"], ["\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  margin-bottom: 0;\n"])), space(1), space(2), function (p) { return p.theme.border; });
var NoteInputNavTab = styled('li')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: 13px;\n"], ["\n  margin-right: 13px;\n"])));
var NoteInputNavTabLink = styled('a')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  .nav-tabs > li > & {\n    font-size: 15px;\n    padding-bottom: 5px;\n  }\n"], ["\n  .nav-tabs > li > & {\n    font-size: 15px;\n    padding-bottom: 5px;\n  }\n"])));
var MarkdownTab = styled(NoteInputNavTab)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  .nav-tabs > & {\n    display: flex;\n    align-items: center;\n    margin-right: 0;\n    color: ", ";\n\n    float: right;\n  }\n"], ["\n  .nav-tabs > & {\n    display: flex;\n    align-items: center;\n    margin-right: 0;\n    color: ", ";\n\n    float: right;\n  }\n"])), function (p) { return p.theme.subText; });
var MarkdownSupported = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin-left: ", ";\n  font-size: 14px;\n"], ["\n  margin-left: ", ";\n  font-size: 14px;\n"])), space(0.5));
var NotePreview = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  ", ";\n  padding-bottom: ", ";\n"], ["\n  ", ";\n  padding-bottom: ", ";\n"])), getNotePreviewCss, space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=input.jsx.map