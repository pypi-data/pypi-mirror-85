import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread, __values } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { Observer } from 'mobx-react';
import omit from 'lodash/omit';
import scrollToElement from 'scroll-to-element';
import styled from '@emotion/styled';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import { Panel, PanelItem, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import FormModel from 'app/views/settings/components/forms/model';
import FormField from 'app/views/settings/components/forms/formField';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import { IconAdd, IconDelete } from 'app/icons';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionsObserver from 'app/views/settings/organizationDeveloperSettings/permissionsObserver';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import { publicIntegrationForms, internalIntegrationForms, } from 'app/data/forms/sentryApplication';
import getDynamicText from 'app/utils/getDynamicText';
import routeTitleGen from 'app/utils/routeTitle';
import DateTime from 'app/components/dateTime';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { addSentryAppToken, removeSentryAppToken, } from 'app/actionCreators/sentryAppTokens';
import Tooltip from 'app/components/tooltip';
import { SENTRY_APP_PERMISSIONS } from 'app/constants';
/**
 * Finds the resource in SENTRY_APP_PERMISSIONS that contains a given scope
 * We should always find a match unless there is a bug
 * @param {Scope} scope
 * @return {Resource | undefined}
 */
var getResourceFromScope = function (scope) {
    var e_1, _a;
    try {
        for (var SENTRY_APP_PERMISSIONS_1 = __values(SENTRY_APP_PERMISSIONS), SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next(); !SENTRY_APP_PERMISSIONS_1_1.done; SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next()) {
            var permObj = SENTRY_APP_PERMISSIONS_1_1.value;
            var allChoices = Object.values(permObj.choices);
            var allScopes = allChoices.reduce(function (_allScopes, choice) { var _a; return _allScopes.concat((_a = choice === null || choice === void 0 ? void 0 : choice.scopes) !== null && _a !== void 0 ? _a : []); }, []);
            if (allScopes.includes(scope)) {
                return permObj.resource;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (SENTRY_APP_PERMISSIONS_1_1 && !SENTRY_APP_PERMISSIONS_1_1.done && (_a = SENTRY_APP_PERMISSIONS_1.return)) _a.call(SENTRY_APP_PERMISSIONS_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return undefined;
};
var SentryAppFormModel = /** @class */ (function (_super) {
    __extends(SentryAppFormModel, _super);
    function SentryAppFormModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Filter out Permission input field values.
     *
     * Permissions (API Scopes) are presented as a list of SelectFields.
     * Instead of them being submitted individually, we want them rolled
     * up into a single list of scopes (this is done in `PermissionSelection`).
     *
     * Because they are all individual inputs, we end up with attributes
     * in the JSON we send to the API that we don't want.
     *
     * This function filters those attributes out of the data that is
     * ultimately sent to the API.
     */
    SentryAppFormModel.prototype.getData = function () {
        return Object.entries(this.fields.toJSON()).reduce(function (data, _a) {
            var _b = __read(_a, 2), k = _b[0], v = _b[1];
            if (!k.endsWith('--permission')) {
                data[k] = v;
            }
            return data;
        }, {});
    };
    /**
     * We need to map the API response errors to the actual form fields.
     * We do this by pulling out scopes and mapping each scope error to the correct input.
     * @param {Object} responseJSON
     */
    SentryAppFormModel.prototype.mapFormErrors = function (responseJSON) {
        if (!responseJSON) {
            return responseJSON;
        }
        var formErrors = omit(responseJSON, ['scopes']);
        if (responseJSON.scopes) {
            responseJSON.scopes.forEach(function (message) {
                //find the scope from the error message of a specific format
                var matches = message.match(/Requested permission of (\w+:\w+)/);
                if (matches) {
                    var scope = matches[1];
                    var resource = getResourceFromScope(scope);
                    //should always match but technically resource can be undefined
                    if (resource) {
                        formErrors[resource + "--permission"] = [message];
                    }
                }
            });
        }
        return formErrors;
    };
    return SentryAppFormModel;
}(FormModel));
var SentryApplicationDetails = /** @class */ (function (_super) {
    __extends(SentryApplicationDetails, _super);
    function SentryApplicationDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.form = new SentryAppFormModel();
        _this.handleSubmitSuccess = function (data) {
            var app = _this.state.app;
            var orgId = _this.props.params.orgId;
            var baseUrl = "/settings/" + orgId + "/developer-settings/";
            var url = app ? baseUrl : "" + baseUrl + data.slug + "/";
            if (app) {
                addSuccessMessage(t('%s successfully saved.', data.name));
            }
            else {
                addSuccessMessage(t('%s successfully created.', data.name));
            }
            browserHistory.push(url);
        };
        _this.handleSubmitError = function (err) {
            var _a;
            var errorMessage = t('Unknown Error');
            if (err.status >= 400 && err.status < 500) {
                errorMessage = (_a = err === null || err === void 0 ? void 0 : err.responseJSON.detail) !== null && _a !== void 0 ? _a : errorMessage;
            }
            addErrorMessage(errorMessage);
            if (_this.form.formErrors) {
                var firstErrorFieldId = Object.keys(_this.form.formErrors)[0];
                if (firstErrorFieldId) {
                    scrollToElement("#" + firstErrorFieldId, {
                        align: 'middle',
                        offset: 0,
                    });
                }
            }
        };
        _this.onAddToken = function (evt) { return __awaiter(_this, void 0, void 0, function () {
            var _a, app, tokens, api, token, newTokens;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        evt.preventDefault();
                        _a = this.state, app = _a.app, tokens = _a.tokens;
                        if (!app) {
                            return [2 /*return*/];
                        }
                        api = this.api;
                        return [4 /*yield*/, addSentryAppToken(api, app)];
                    case 1:
                        token = _b.sent();
                        newTokens = tokens.concat(token);
                        this.setState({ tokens: newTokens });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.onRemoveToken = function (token, evt) { return __awaiter(_this, void 0, void 0, function () {
            var _a, app, tokens, api, newTokens;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        evt.preventDefault();
                        _a = this.state, app = _a.app, tokens = _a.tokens;
                        if (!app) {
                            return [2 /*return*/];
                        }
                        api = this.api;
                        newTokens = tokens.filter(function (tok) { return tok.token !== token.token; });
                        return [4 /*yield*/, removeSentryAppToken(api, app, token.token)];
                    case 1:
                        _b.sent();
                        this.setState({ tokens: newTokens });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.renderTokens = function () {
            var tokens = _this.state.tokens;
            if (tokens.length > 0) {
                return tokens.map(function (token) { return (<StyledPanelItem key={token.token}>
          <TokenItem>
            <Tooltip disabled={_this.showAuthInfo} position="right" containerDisplayMode="inline" title={t('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
              <TextCopyInput>
                {getDynamicText({ value: token.token, fixed: 'xxxxxx' })}
              </TextCopyInput>
            </Tooltip>
          </TokenItem>
          <CreatedDate>
            <CreatedTitle>Created:</CreatedTitle>
            <DateTime date={getDynamicText({
                    value: token.dateCreated,
                    fixed: new Date(1508208080000),
                })}/>
          </CreatedDate>
          <Button onClick={_this.onRemoveToken.bind(_this, token)} size="small" icon={<IconDelete />} data-test-id="token-delete" type="button">
            {t('Revoke')}
          </Button>
        </StyledPanelItem>); });
            }
            else {
                return <EmptyMessage description={t('No tokens created yet.')}/>;
            }
        };
        _this.onFieldChange = function (name, value) {
            if (name === 'webhookUrl' && !value && _this.isInternal) {
                //if no webhook, then set isAlertable to false
                _this.form.setValue('isAlertable', false);
            }
        };
        return _this;
    }
    SentryApplicationDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { app: null, tokens: [] });
    };
    SentryApplicationDetails.prototype.getEndpoints = function () {
        var appSlug = this.props.params.appSlug;
        if (appSlug) {
            return [
                ['app', "/sentry-apps/" + appSlug + "/"],
                ['tokens', "/sentry-apps/" + appSlug + "/api-tokens/"],
            ];
        }
        return [];
    };
    SentryApplicationDetails.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitleGen(t('Sentry Integration Details'), orgId, false);
    };
    // Events may come from the API as "issue.created" when we just want "issue" here.
    SentryApplicationDetails.prototype.normalize = function (events) {
        if (events.length === 0) {
            return events;
        }
        return events.map(function (e) { return e.split('.').shift(); });
    };
    Object.defineProperty(SentryApplicationDetails.prototype, "isInternal", {
        get: function () {
            var app = this.state.app;
            if (app) {
                // if we are editing an existing app, check the status of the app
                return app.status === 'internal';
            }
            return this.props.route.path === 'new-internal/';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryApplicationDetails.prototype, "showAuthInfo", {
        get: function () {
            var app = this.state.app;
            return !(app && app.clientSecret && app.clientSecret[0] === '*');
        },
        enumerable: false,
        configurable: true
    });
    SentryApplicationDetails.prototype.renderBody = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var app = this.state.app;
        var scopes = (app && __spread(app.scopes)) || [];
        var events = (app && this.normalize(app.events)) || [];
        var method = app ? 'PUT' : 'POST';
        var endpoint = app ? "/sentry-apps/" + app.slug + "/" : '/sentry-apps/';
        var forms = this.isInternal ? internalIntegrationForms : publicIntegrationForms;
        var verifyInstall;
        if (this.isInternal) {
            //force verifyInstall to false for all internal apps
            verifyInstall = false;
        }
        else {
            //use the existing value for verifyInstall if the app exists, otherwise default to true
            verifyInstall = app ? app.verifyInstall : true;
        }
        return (<div>
        <SettingsPageHeader title={this.getTitle()}/>
        <Form apiMethod={method} apiEndpoint={endpoint} allowUndo initialData={__assign(__assign({ organization: orgId, isAlertable: false, isInternal: this.isInternal, schema: {}, scopes: [] }, app), { verifyInstall: verifyInstall })} model={this.form} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onFieldChange={this.onFieldChange}>
          <Observer>
            {function () {
            var webhookDisabled = _this.isInternal && !_this.form.getValue('webhookUrl');
            return (<React.Fragment>
                  <JsonForm location={_this.props.location} additionalFieldProps={{ webhookDisabled: webhookDisabled }} forms={forms}/>

                  <PermissionsObserver webhookDisabled={webhookDisabled} appPublished={app ? app.status === 'published' : false} scopes={scopes} events={events}/>
                </React.Fragment>);
        }}
          </Observer>

          {app && app.status === 'internal' && (<Panel>
              <PanelHeader hasButtons>
                {t('Tokens')}
                <Button size="xsmall" icon={<IconAdd size="xs" isCircled/>} onClick={function (evt) { return _this.onAddToken(evt); }} data-test-id="token-add" type="button">
                  {t('New Token')}
                </Button>
              </PanelHeader>
              <PanelBody>{this.renderTokens()}</PanelBody>
            </Panel>)}

          {app && (<Panel>
              <PanelHeader>{t('Credentials')}</PanelHeader>
              <PanelBody>
                {app.status !== 'internal' && (<FormField name="clientId" label="Client ID">
                    {function (_a) {
            var value = _a.value;
            return (<TextCopyInput>
                        {getDynamicText({ value: value, fixed: 'CI_CLIENT_ID' })}
                      </TextCopyInput>);
        }}
                  </FormField>)}
                <FormField name="clientSecret" label="Client Secret">
                  {function (_a) {
            var value = _a.value;
            return value ? (<Tooltip disabled={_this.showAuthInfo} position="right" containerDisplayMode="inline" title={t('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
                        <TextCopyInput>
                          {getDynamicText({ value: value, fixed: 'CI_CLIENT_SECRET' })}
                        </TextCopyInput>
                      </Tooltip>) : (<em>hidden</em>);
        }}
                </FormField>
              </PanelBody>
            </Panel>)}
        </Form>
      </div>);
    };
    return SentryApplicationDetails;
}(AsyncView));
export default SentryApplicationDetails;
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var TokenItem = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 70%;\n"], ["\n  width: 70%;\n"])));
var CreatedTitle = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: 2px;\n"], ["\n  color: ", ";\n  margin-bottom: 2px;\n"])), function (p) { return p.theme.gray300; });
var CreatedDate = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  font-size: 14px;\n  margin: 0 10px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  font-size: 14px;\n  margin: 0 10px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryApplicationDetails.jsx.map