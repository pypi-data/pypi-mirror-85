import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import Access from 'app/components/acl/access';
import BooleanField from 'app/views/settings/components/forms/booleanField';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import DateTime from 'app/components/dateTime';
import ExternalLink from 'app/components/links/externalLink';
import Field from 'app/views/settings/components/forms/field';
import Form from 'app/views/settings/components/forms/form';
import { IconFlag } from 'app/icons';
import KeyRateLimitsForm from 'app/views/settings/project/projectKeys/details/keyRateLimitsForm';
import ProjectKeyCredentials from 'app/views/settings/project/projectKeys/projectKeyCredentials';
import SelectField from 'app/views/settings/components/forms/selectField';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import TextField from 'app/views/settings/components/forms/textField';
import getDynamicText from 'app/utils/getDynamicText';
var KeySettings = /** @class */ (function (_super) {
    __extends(KeySettings, _super);
    function KeySettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
        };
        _this.handleRemove = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, onRemove, params, keyId, orgId, projectId, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (this.state.loading) {
                            return [2 /*return*/];
                        }
                        addLoadingMessage(t('Revoking key\u2026'));
                        _a = this.props, api = _a.api, onRemove = _a.onRemove, params = _a.params;
                        keyId = params.keyId, orgId = params.orgId, projectId = params.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        onRemove();
                        addSuccessMessage(t('Revoked key'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({
                            error: true,
                            loading: false,
                        });
                        addErrorMessage(t('Unable to revoke key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    KeySettings.prototype.render = function () {
        var _this = this;
        var _a = this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
        var data = this.props.data;
        var apiEndpoint = "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/";
        var loaderLink = getDynamicText({
            value: data.dsn.cdn,
            fixed: '__JS_SDK_LOADER_URL__',
        });
        return (<Access access={['project:write']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<React.Fragment>
            <Form saveOnBlur allowUndo apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <Panel>
                <PanelHeader>{t('Details')}</PanelHeader>

                <PanelBody>
                  <TextField name="name" label={t('Name')} disabled={!hasAccess} required={false} maxLength={64}/>
                  <BooleanField name="isActive" label={t('Enabled')} required={false} disabled={!hasAccess} help="Accept events from this key? This may be used to temporarily suspend a key."/>
                  <Field label={t('Created')}>
                    <div className="controls">
                      <DateTime date={data.dateCreated}/>
                    </div>
                  </Field>
                </PanelBody>
              </Panel>
            </Form>

            <KeyRateLimitsForm params={_this.props.params} data={data} disabled={!hasAccess}/>

            <Form saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
              <Panel>
                <PanelHeader>{t('JavaScript Loader')}</PanelHeader>
                <PanelBody>
                  <Field help={tct('Copy this script into your website to setup your JavaScript SDK without any additional configuration. [link]', {
                link: (<ExternalLink href="https://docs.sentry.io/platforms/javascript/#what-does-the-loader-provide">
                            What does the script provide?
                          </ExternalLink>),
            })} inline={false} flexibleControlStateSize>
                    <TextCopyInput>
                      {"<script src='" + loaderLink + "' crossorigin=\"anonymous\"></script>"}
                    </TextCopyInput>
                  </Field>
                  <SelectField deprecatedSelectControl name="browserSdkVersion" choices={data.browserSdk ? data.browserSdk.choices : []} placeholder={t('4.x')} allowClear={false} enabled={!hasAccess} help={t('Select the version of the SDK that should be loaded. Note that it can take a few minutes until this change is live.')}/>
                </PanelBody>
              </Panel>
            </Form>

            <Panel>
              <PanelHeader>{t('Credentials')}</PanelHeader>
              <PanelBody>
                <PanelAlert type="info" icon={<IconFlag size="md"/>}>
                  {t('Your credentials are coupled to a public and secret key. Different clients will require different credentials, so make sure you check the documentation before plugging things in.')}
                </PanelAlert>

                <ProjectKeyCredentials projectId={"" + data.projectId} data={data} showPublicKey showSecretKey showProjectId/>
              </PanelBody>
            </Panel>

            <Access access={['project:admin']}>
              <Panel>
                <PanelHeader>{t('Revoke Key')}</PanelHeader>
                <PanelBody>
                  <Field label={t('Revoke Key')} help={t('Revoking this key will immediately remove and suspend the credentials. This action is irreversible.')}>
                    <div>
                      <Confirm priority="danger" message={t('Are you sure you want to revoke this key? This will immediately remove and suspend the credentials.')} onConfirm={_this.handleRemove} confirmText={t('Revoke Key')}>
                        <Button priority="danger">{t('Revoke Key')}</Button>
                      </Confirm>
                    </div>
                  </Field>
                </PanelBody>
              </Panel>
            </Access>
          </React.Fragment>);
        }}
      </Access>);
    };
    return KeySettings;
}(React.Component));
export default KeySettings;
//# sourceMappingURL=keySettings.jsx.map