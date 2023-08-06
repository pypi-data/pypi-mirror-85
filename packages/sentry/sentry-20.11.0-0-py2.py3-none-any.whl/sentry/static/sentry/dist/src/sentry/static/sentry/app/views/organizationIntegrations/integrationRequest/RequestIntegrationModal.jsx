import { __assign, __extends } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import { t } from 'app/locale';
import TextareaField from 'app/views/settings/components/forms/textareaField';
import TextBlock from 'app/views/settings/components/text/textBlock';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
/**
 * This modal serves as a non-owner's confirmation step before sending
 * organization owners an email requesting a new organization integration. It
 * lets the user attach an optional message to be included in the email.
 */
var RequestIntegrationModal = /** @class */ (function (_super) {
    __extends(RequestIntegrationModal, _super);
    function RequestIntegrationModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = __assign(__assign({}, _this.getDefaultState()), { isSending: false, message: '' });
        _this.sendRequest = function () {
            var _a = _this.props, organization = _a.organization, slug = _a.slug, type = _a.type;
            var message = _this.state.message;
            trackIntegrationEvent({
                eventKey: 'integrations.request_install',
                eventName: 'Integrations: Request Install',
                integration_type: type,
                integration: slug,
            }, organization);
            var endpoint = "/organizations/" + organization.slug + "/integration-requests/";
            _this.api.request(endpoint, {
                method: 'POST',
                data: {
                    providerSlug: slug,
                    providerType: type,
                    message: message,
                },
                success: _this.handleSubmitSuccess,
                error: _this.handleSubmitError,
            });
        };
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, closeModal = _a.closeModal, onSuccess = _a.onSuccess;
            addSuccessMessage(t('Request successfully sent.'));
            _this.setState({ isSending: false });
            onSuccess();
            closeModal();
        };
        _this.handleSubmitError = function () {
            addErrorMessage('Error sending the request');
            _this.setState({ isSending: false });
        };
        return _this;
    }
    RequestIntegrationModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, name = _a.name;
        var buttonText = this.state.isSending ? t('Sending Request') : t('Send Request');
        return (<React.Fragment>
        <Header>
          <h4>{t('Request %s Installation', name)}</h4>
        </Header>
        <Body>
          <TextBlock>
            {t('Looks like your organization owner, manager, or admin needs to install %s. Want to send them a request?', name)}
          </TextBlock>
          <TextBlock>
            {t('(Optional) You’ve got good reasons for installing the %s Integration. Share them with your organization owner.', name)}
          </TextBlock>
          <TextareaField inline={false} flexibleControlStateSize stacked name="message" type="string" onChange={function (value) { return _this.setState({ message: value }); }} placeholder={t('Optional message…')}/>
          <TextBlock>
            {t('When you click “Send Request”, we’ll email your request to your organization’s owners. So just keep that in mind.')}
          </TextBlock>
        </Body>
        <Footer>
          <Button onClick={this.sendRequest}>{buttonText}</Button>
        </Footer>
      </React.Fragment>);
    };
    return RequestIntegrationModal;
}(AsyncComponent));
export default RequestIntegrationModal;
//# sourceMappingURL=RequestIntegrationModal.jsx.map