import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import { trackAdhocEvent } from 'app/utils/analytics';
import EmailField from 'app/views/settings/components/forms/emailField';
import Form from 'app/views/settings/components/forms/form';
import { IconMegaphone } from 'app/icons';
import NarrowLayout from 'app/components/narrowLayout';
import space from 'app/styles/space';
var OrganizationJoinRequest = /** @class */ (function (_super) {
    __extends(OrganizationJoinRequest, _super);
    function OrganizationJoinRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            submitSuccess: null,
        };
        _this.handleSubmitSuccess = function () {
            _this.setState({ submitSuccess: true });
        };
        _this.handleCancel = function (e) {
            e.preventDefault();
            var orgId = _this.props.params.orgId;
            window.location.assign("/auth/login/" + orgId + "/");
        };
        return _this;
    }
    OrganizationJoinRequest.prototype.componentDidMount = function () {
        var orgId = this.props.params.orgId;
        trackAdhocEvent({
            eventKey: 'join_request.viewed',
            org_slug: orgId,
        });
    };
    OrganizationJoinRequest.prototype.handleSubmitError = function () {
        addErrorMessage(t('Request to join failed'));
    };
    OrganizationJoinRequest.prototype.render = function () {
        var orgId = this.props.params.orgId;
        var submitSuccess = this.state.submitSuccess;
        if (submitSuccess) {
            return (<NarrowLayout maxWidth="550px">
          <SuccessModal>
            <StyledIconMegaphone size="5em"/>
            <StyledHeader>{t('Request Sent')}</StyledHeader>
            <StyledText>{t('Your request to join has been sent.')}</StyledText>
            <ReceiveEmailMessage>
              {tct('You will receive an email when your request is approved.', { orgId: orgId })}
            </ReceiveEmailMessage>
          </SuccessModal>
        </NarrowLayout>);
        }
        return (<NarrowLayout maxWidth="650px">
        <StyledIconMegaphone size="5em"/>
        <StyledHeader>{t('Request to Join')}</StyledHeader>
        <StyledText>
          {tct('Ask the admins if you can join the [orgId] organization.', {
            orgId: orgId,
        })}
        </StyledText>
        <Form requireChanges apiEndpoint={"/organizations/" + orgId + "/join-request/"} apiMethod="POST" submitLabel={t('Request to Join')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={this.handleCancel}>
          <StyledEmailField name="email" inline={false} label={t('Email Address')} placeholder="name@example.com"/>
        </Form>
      </NarrowLayout>);
    };
    return OrganizationJoinRequest;
}(React.Component));
var SuccessModal = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  justify-items: center;\n  text-align: center;\n  padding-top: 10px;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  justify-items: center;\n  text-align: center;\n  padding-top: 10px;\n  padding-bottom: ", ";\n"])), space(4));
var StyledIconMegaphone = styled(IconMegaphone)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space(3));
var StyledHeader = styled('h3')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var StyledText = styled('p')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var ReceiveEmailMessage = styled(StyledText)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  max-width: 250px;\n"], ["\n  max-width: 250px;\n"])));
var StyledEmailField = styled(EmailField)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding-top: ", ";\n  padding-left: 0;\n"], ["\n  padding-top: ", ";\n  padding-left: 0;\n"])), space(2));
export default OrganizationJoinRequest;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=organizationJoinRequest.jsx.map