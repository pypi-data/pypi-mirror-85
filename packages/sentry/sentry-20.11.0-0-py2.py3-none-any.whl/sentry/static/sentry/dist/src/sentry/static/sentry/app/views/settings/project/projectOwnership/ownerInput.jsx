import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import TextareaAutosize from 'react-autosize-textarea';
import { Client } from 'app/api';
import memberListStore from 'app/stores/memberListStore';
import ProjectsStore from 'app/stores/projectsStore';
import Button from 'app/components/button';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import { inputStyles } from 'app/styles/input';
import theme from 'app/utils/theme';
import RuleBuilder from './ruleBuilder';
var defaultProps = {
    urls: [],
    paths: [],
    disabled: false,
};
var OwnerInput = /** @class */ (function (_super) {
    __extends(OwnerInput, _super);
    function OwnerInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasChanges: false,
            text: '',
            error: null,
        };
        _this.handleUpdateOwnership = function () {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var text = _this.state.text;
            _this.setState({ error: null });
            var api = new Client();
            var request = api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/ownership/", {
                method: 'PUT',
                data: { raw: text || '' },
            });
            request
                .then(function () {
                addSuccessMessage(t('Updated issue ownership rules'));
                _this.setState({
                    hasChanges: false,
                    text: text,
                });
            })
                .catch(function (error) {
                _this.setState({ error: error.responseJSON });
                if (error.status === 403) {
                    addErrorMessage(t("You don't have permission to modify issue ownership rules for this project"));
                }
                else if (error.status === 400 &&
                    error.responseJSON.raw &&
                    error.responseJSON.raw[0].startsWith('Invalid rule owners:')) {
                    addErrorMessage(t('Unable to save issue ownership rule changes: ' + error.responseJSON.raw[0]));
                }
                else {
                    addErrorMessage(t('Unable to save issue ownership rule changes'));
                }
            });
            return request;
        };
        _this.handleChange = function (e) {
            _this.setState({
                hasChanges: true,
                text: e.target.value,
            });
        };
        _this.handleAddRule = function (rule) {
            _this.setState(function (_a) {
                var text = _a.text;
                return ({
                    text: text + '\n' + rule,
                });
            }, _this.handleUpdateOwnership);
        };
        return _this;
    }
    OwnerInput.prototype.parseError = function (error) {
        var _a, _b, _c;
        var text = (_a = error === null || error === void 0 ? void 0 : error.raw) === null || _a === void 0 ? void 0 : _a[0];
        if (!text) {
            return null;
        }
        if (text.startsWith('Invalid rule owners:')) {
            return <InvalidOwners>{text}</InvalidOwners>;
        }
        else {
            return (<SyntaxOverlay line={parseInt((_c = (_b = text.match(/line (\d*),/)) === null || _b === void 0 ? void 0 : _b[1]) !== null && _c !== void 0 ? _c : '', 10) - 1}/>);
        }
    };
    OwnerInput.prototype.mentionableUsers = function () {
        return memberListStore.getAll().map(function (member) { return ({
            id: member.id,
            display: member.email,
            email: member.email,
        }); });
    };
    OwnerInput.prototype.mentionableTeams = function () {
        var project = this.props.project;
        var projectWithTeams = ProjectsStore.getBySlug(project.slug);
        if (!projectWithTeams) {
            return [];
        }
        return projectWithTeams.teams.map(function (team) { return ({
            id: team.id,
            display: "#" + team.slug,
            email: team.id,
        }); });
    };
    OwnerInput.prototype.render = function () {
        var _this = this;
        var _a = this.props, project = _a.project, organization = _a.organization, disabled = _a.disabled, urls = _a.urls, paths = _a.paths, initialText = _a.initialText;
        var _b = this.state, hasChanges = _b.hasChanges, text = _b.text, error = _b.error;
        return (<React.Fragment>
        <RuleBuilder urls={urls} paths={paths} organization={organization} project={project} onAddRule={this.handleAddRule.bind(this)} disabled={disabled}/>
        <div style={{ position: 'relative' }} onKeyDown={function (e) {
            if (e.metaKey && e.key === 'Enter') {
                _this.handleUpdateOwnership();
            }
        }}>
          <StyledTextArea placeholder={'#example usage\n' +
            'path:src/example/pipeline/* person@sentry.io #infra\n' +
            'url:http://example.com/settings/* #product\n' +
            'tags.sku_class:enterprise #enterprise'} onChange={this.handleChange} disabled={disabled} value={text || initialText} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off" theme={theme}/>
          <ActionBar>
            <div>{this.parseError(error)}</div>
            <SaveButton>
              <Button size="small" priority="primary" onClick={this.handleUpdateOwnership} disabled={disabled || !hasChanges}>
                {t('Save Changes')}
              </Button>
            </SaveButton>
          </ActionBar>
        </div>
      </React.Fragment>);
    };
    OwnerInput.defaultProps = defaultProps;
    return OwnerInput;
}(React.Component));
var TEXTAREA_PADDING = 4;
var TEXTAREA_LINE_HEIGHT = 24;
var ActionBar = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var SyntaxOverlay = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  width: 100%;\n  height: ", "px;\n  background-color: red;\n  opacity: 0.1;\n  pointer-events: none;\n  position: absolute;\n  top: ", "px;\n"], ["\n  ", ";\n  width: 100%;\n  height: ", "px;\n  background-color: red;\n  opacity: 0.1;\n  pointer-events: none;\n  position: absolute;\n  top: ", "px;\n"])), inputStyles, TEXTAREA_LINE_HEIGHT, function (_a) {
    var line = _a.line;
    return TEXTAREA_PADDING + line * 24;
});
var SaveButton = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: end;\n  padding-top: 10px;\n"], ["\n  text-align: end;\n  padding-top: 10px;\n"])));
var StyledTextArea = styled(TextareaAutosize)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n  min-height: 140px;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  padding-top: ", "px;\n  line-height: ", "px;\n"], ["\n  ", ";\n  min-height: 140px;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  padding-top: ", "px;\n  line-height: ", "px;\n"])), inputStyles, function (p) { return p.theme.text.familyMono; }, TEXTAREA_PADDING, TEXTAREA_LINE_HEIGHT);
var InvalidOwners = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: bold;\n  margin-top: 12px;\n"], ["\n  color: ", ";\n  font-weight: bold;\n  margin-top: 12px;\n"])), function (p) { return p.theme.error; });
export default OwnerInput;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=ownerInput.jsx.map