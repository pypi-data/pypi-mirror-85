import { __extends } from "tslib";
import { browserHistory } from 'react-router';
import DocumentTitle from 'react-document-title';
import React from 'react';
import { API_ACCESS_SCOPES, DEFAULT_API_ACCESS_SCOPES } from 'app/constants';
import { t, tct } from 'app/locale';
import ApiForm from 'app/views/settings/components/forms/apiForm';
import FormField from 'app/views/settings/components/forms/formField';
import MultipleCheckbox from 'app/views/settings/components/forms/controls/multipleCheckbox';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var SORTED_DEFAULT_API_ACCESS_SCOPES = DEFAULT_API_ACCESS_SCOPES.sort();
var API_CHOICES = API_ACCESS_SCOPES.map(function (s) { return [s, s]; });
var API_INDEX_ROUTE = '/settings/account/api/auth-tokens/';
var ApiNewToken = /** @class */ (function (_super) {
    __extends(ApiNewToken, _super);
    function ApiNewToken() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onCancel = function () {
            browserHistory.push(API_INDEX_ROUTE);
        };
        _this.onSubmitSuccess = function () {
            browserHistory.push(API_INDEX_ROUTE);
        };
        return _this;
    }
    ApiNewToken.prototype.render = function () {
        return (<DocumentTitle title="Create API Token - Sentry">
        <div>
          <SettingsPageHeader title={t('Create New Token')}/>
          <TextBlock>
            {t("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API.")}
          </TextBlock>
          <TextBlock>
            {tct('For more information on how to use the web API, see our [link:documentation].', {
            link: <a href="https://docs.sentry.io/api/"/>,
        })}
          </TextBlock>
          <Panel>
            <PanelHeader>{t('Create New Token')}</PanelHeader>
            <ApiForm apiMethod="POST" apiEndpoint="/api-tokens/" initialData={{ scopes: SORTED_DEFAULT_API_ACCESS_SCOPES }} onSubmitSuccess={this.onSubmitSuccess} onCancel={this.onCancel} footerStyle={{
            marginTop: 0,
            paddingRight: 20,
        }} submitLabel={t('Create Token')}>
              <PanelBody>
                <FormField name="scopes" label={t('Scopes')} inline={false} required>
                  {function (_a) {
            var value = _a.value, onChange = _a.onChange;
            return (<MultipleCheckbox onChange={onChange} value={value} choices={API_CHOICES}/>);
        }}
                </FormField>
              </PanelBody>
            </ApiForm>
          </Panel>
        </div>
      </DocumentTitle>);
    };
    return ApiNewToken;
}(React.Component));
export default ApiNewToken;
//# sourceMappingURL=apiNewToken.jsx.map