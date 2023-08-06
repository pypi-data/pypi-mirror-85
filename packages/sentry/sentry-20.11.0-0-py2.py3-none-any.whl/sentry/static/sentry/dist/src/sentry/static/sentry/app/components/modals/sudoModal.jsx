import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { withRouter } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import withApi from 'app/utils/withApi';
import Button from 'app/components/button';
import ConfigStore from 'app/stores/configStore';
import Form from 'app/views/settings/components/forms/form';
import InputField from 'app/views/settings/components/forms/inputField';
import { IconFlag } from 'app/icons';
import TextBlock from 'app/views/settings/components/text/textBlock';
import U2fContainer from 'app/components/u2f/u2fContainer';
import space from 'app/styles/space';
var SudoModal = /** @class */ (function (_super) {
    __extends(SudoModal, _super);
    function SudoModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            busy: false,
        };
        _this.handleSuccess = function () {
            var _a = _this.props, closeModal = _a.closeModal, superuser = _a.superuser, location = _a.location, router = _a.router, retryRequest = _a.retryRequest;
            if (!retryRequest) {
                closeModal();
                return;
            }
            if (superuser) {
                router.replace({ pathname: location.pathname, state: { forceUpdate: new Date() } });
                return;
            }
            _this.setState({ busy: true }, function () {
                retryRequest().then(function () {
                    _this.setState({ busy: false }, closeModal);
                });
            });
        };
        _this.handleError = function () {
            _this.setState({ busy: false, error: true });
        };
        _this.handleU2fTap = function (data) { return __awaiter(_this, void 0, void 0, function () {
            var api, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ busy: true });
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/', { method: 'PUT', data: data })];
                    case 2:
                        _a.sent();
                        this.handleSuccess();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.setState({ busy: false });
                        // u2fInterface relies on this
                        throw err_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    SudoModal.prototype.renderBodyContent = function () {
        var superuser = this.props.superuser;
        var error = this.state.error;
        var user = ConfigStore.get('user');
        if (!user.hasPasswordAuth) {
            return (<React.Fragment>
          <TextBlock>{t('You will need to reauthenticate to continue.')}</TextBlock>
          <Button priority="primary" href={"/auth/login/?next=" + encodeURIComponent(location.pathname)}>
            {t('Continue')}
          </Button>
        </React.Fragment>);
        }
        return (<React.Fragment>
        <StyledTextBlock>
          {superuser
            ? t('You are attempting to access a resource that requires superuser access, please re-authenticate as a superuser.')
            : t('Help us keep your account safe by confirming your identity.')}
        </StyledTextBlock>

        {error && (<StyledAlert type="error" icon={<IconFlag size="md"/>}>
            {t('Incorrect password')}
          </StyledAlert>)}

        <Form apiMethod="PUT" apiEndpoint="/auth/" submitLabel={t('Confirm Password')} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} hideFooter={!user.hasPasswordAuth} hideErrors resetOnError>
          <StyledInputField type="password" inline={false} label={t('Password')} name="password" autoFocus flexibleControlStateSize/>
          <U2fContainer displayMode="sudo" onTap={this.handleU2fTap}/>
        </Form>
      </React.Fragment>);
    };
    SudoModal.prototype.render = function () {
        var _a = this.props, closeModal = _a.closeModal, Header = _a.Header, Body = _a.Body;
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          {t('Confirm Password to Continue')}
        </Header>
        <Body>{this.renderBodyContent()}</Body>
      </React.Fragment>);
    };
    return SudoModal;
}(React.Component));
export default withRouter(withApi(SudoModal));
export { SudoModal };
var StyledTextBlock = styled(TextBlock)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var StyledInputField = styled(InputField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: 0;\n"], ["\n  padding-left: 0;\n"])));
var StyledAlert = styled(Alert)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sudoModal.jsx.map