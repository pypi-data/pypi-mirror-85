import { __extends } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import AvatarChooser from 'app/components/avatarChooser';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import accountDetailsFields from 'app/data/forms/accountDetails';
import accountPreferencesFields from 'app/data/forms/accountPreferences';
import { updateUser } from 'app/actionCreators/account';
import { t } from 'app/locale';
var ENDPOINT = '/users/me/';
var AccountDetails = /** @class */ (function (_super) {
    __extends(AccountDetails, _super);
    function AccountDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (user) {
            // the updateUser method updates our Config Store
            // No components listen to the ConfigStore, they just access it directly
            updateUser(user);
            // We need to update the state, because AvatarChooser is using it,
            // otherwise it will flick
            _this.setState({
                user: user,
            });
        };
        return _this;
    }
    AccountDetails.prototype.getEndpoints = function () {
        // local state is NOT updated when the form saves
        return [['user', ENDPOINT]];
    };
    AccountDetails.prototype.renderBody = function () {
        var _this = this;
        var user = this.state.user;
        var location = this.props.location;
        var formCommonProps = {
            apiEndpoint: ENDPOINT,
            apiMethod: 'PUT',
            allowUndo: true,
            saveOnBlur: true,
        };
        return (<div>
        <SettingsPageHeader title={t('Account Details')}/>
        <Form initialData={user} {...formCommonProps} onSubmitSuccess={this.handleSubmitSuccess}>
          <JsonForm location={location} forms={accountDetailsFields} additionalFieldProps={{ user: user }}/>
        </Form>
        <Form initialData={user.options} {...formCommonProps} allowUndo>
          <JsonForm location={location} forms={accountPreferencesFields}/>
        </Form>
        <AvatarChooser endpoint="/users/me/avatar/" model={user} onSave={function (resp) {
            _this.handleSubmitSuccess(resp);
        }} isUser/>
      </div>);
    };
    return AccountDetails;
}(AsyncView));
export default AccountDetails;
//# sourceMappingURL=accountDetails.jsx.map