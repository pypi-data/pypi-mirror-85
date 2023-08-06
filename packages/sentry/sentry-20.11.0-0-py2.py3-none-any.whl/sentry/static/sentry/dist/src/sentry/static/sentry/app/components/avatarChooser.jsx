import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
import { t } from 'app/locale';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import withApi from 'app/utils/withApi';
import Well from 'app/components/well';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import Avatar from 'app/components/avatar';
import AvatarCropper from 'app/components/avatarCropper';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
var AvatarChooser = /** @class */ (function (_super) {
    __extends(AvatarChooser, _super);
    function AvatarChooser() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            model: _this.props.model,
            savedDataUrl: null,
            dataUrl: null,
            hasError: false,
        };
        _this.handleSaveSettings = function (ev) {
            var _a = _this.props, endpoint = _a.endpoint, api = _a.api;
            var _b = _this.state, model = _b.model, dataUrl = _b.dataUrl;
            ev.preventDefault();
            var data = {};
            var avatarType = model && model.avatar ? model.avatar.avatarType : undefined;
            var avatarPhoto = dataUrl ? dataUrl.split(',')[1] : undefined;
            data = {
                avatar_photo: avatarPhoto,
                avatar_type: avatarType,
            };
            api.request(endpoint, {
                method: 'PUT',
                data: data,
                success: function (resp) {
                    _this.setState({ savedDataUrl: _this.state.dataUrl });
                    _this.handleSuccess(resp);
                },
                error: _this.handleError.bind(_this, 'There was an error saving your preferences.'),
            });
        };
        _this.handleChange = function (id) {
            var _a, _b;
            return _this.updateState(__assign(__assign({}, _this.state.model), { avatar: { avatarUuid: (_b = (_a = _this.state.model.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid) !== null && _b !== void 0 ? _b : '', avatarType: id } }));
        };
        return _this;
    }
    AvatarChooser.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // Update local state if defined in props
        if (typeof nextProps.model !== 'undefined') {
            this.setState({ model: nextProps.model });
        }
    };
    AvatarChooser.prototype.updateState = function (model) {
        this.setState({ model: model });
    };
    AvatarChooser.prototype.handleError = function (msg) {
        addErrorMessage(msg);
    };
    AvatarChooser.prototype.handleSuccess = function (model) {
        var onSave = this.props.onSave;
        this.setState({ model: model });
        onSave(model);
        addSuccessMessage(t('Successfully saved avatar preferences'));
    };
    AvatarChooser.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, allowGravatar = _c.allowGravatar, allowUpload = _c.allowUpload, allowLetter = _c.allowLetter, savedDataUrl = _c.savedDataUrl, type = _c.type, isUser = _c.isUser, disabled = _c.disabled;
        var _d = this.state, hasError = _d.hasError, model = _d.model;
        if (hasError) {
            return <LoadingError />;
        }
        if (!model) {
            return <LoadingIndicator />;
        }
        var avatarType = (_b = (_a = model.avatar) === null || _a === void 0 ? void 0 : _a.avatarType) !== null && _b !== void 0 ? _b : 'letter_avatar';
        var isLetter = avatarType === 'letter_avatar';
        var isTeam = type === 'team';
        var isOrganization = type === 'organization';
        var choices = [];
        if (allowLetter) {
            choices.push(['letter_avatar', t('Use initials')]);
        }
        if (allowUpload) {
            choices.push(['upload', t('Upload an image')]);
        }
        if (allowGravatar) {
            choices.push(['gravatar', t('Use Gravatar')]);
        }
        return (<Panel>
        <PanelHeader>{t('Avatar')}</PanelHeader>
        <PanelBody>
          <AvatarForm>
            <AvatarGroup inline={isLetter}>
              <RadioGroup style={{ flex: 1 }} choices={choices} value={avatarType} label={t('Avatar Type')} onChange={this.handleChange} disabled={disabled}/>
              {isLetter && (<Avatar gravatar={false} style={{ width: 90, height: 90 }} user={isUser ? model : undefined} organization={isOrganization ? model : undefined} team={isTeam ? model : undefined}/>)}
            </AvatarGroup>

            <AvatarUploadSection>
              {allowGravatar && avatarType === 'gravatar' && (<Well>
                  {t('Gravatars are managed through ')}
                  <ExternalLink href="http://gravatar.com">Gravatar.com</ExternalLink>
                </Well>)}

              {model.avatar && avatarType === 'upload' && (<AvatarCropper {...this.props} type={type} model={model} savedDataUrl={savedDataUrl} updateDataUrlState={function (dataState) { return _this.setState(dataState); }}/>)}
              <AvatarSubmit className="form-actions">
                <Button type="button" priority="primary" onClick={this.handleSaveSettings} disabled={disabled}>
                  {t('Save Avatar')}
                </Button>
              </AvatarSubmit>
            </AvatarUploadSection>
          </AvatarForm>
        </PanelBody>
      </Panel>);
    };
    AvatarChooser.defaultProps = {
        allowGravatar: true,
        allowLetter: true,
        allowUpload: true,
        type: 'user',
        onSave: function () { },
    };
    return AvatarChooser;
}(React.Component));
var AvatarGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: ", ";\n"], ["\n  display: flex;\n  flex-direction: ", ";\n"])), function (p) { return (p.inline ? 'row' : 'column'); });
var AvatarForm = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  line-height: 1.5em;\n  padding: 1em 1.25em;\n"], ["\n  line-height: 1.5em;\n  padding: 1em 1.25em;\n"])));
var AvatarSubmit = styled('fieldset')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 1em;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 1em;\n"])));
var AvatarUploadSection = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-top: 1em;\n"], ["\n  margin-top: 1em;\n"])));
export default withApi(AvatarChooser);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=avatarChooser.jsx.map