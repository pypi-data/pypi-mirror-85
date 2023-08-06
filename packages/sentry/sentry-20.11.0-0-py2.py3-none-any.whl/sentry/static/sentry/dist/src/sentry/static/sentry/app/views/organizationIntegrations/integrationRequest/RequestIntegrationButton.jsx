import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Button from 'app/components/button';
import { t } from 'app/locale';
import space from 'app/styles/space';
import RequestIntegrationModal from './RequestIntegrationModal';
var RequestIntegrationButton = /** @class */ (function (_super) {
    __extends(RequestIntegrationButton, _super);
    function RequestIntegrationButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
            isSent: false,
        };
        return _this;
    }
    RequestIntegrationButton.prototype.openRequestModal = function () {
        var _this = this;
        this.setState({ isOpen: true });
        openModal(function (renderProps) { return (<RequestIntegrationModal {..._this.props} {...renderProps} onSuccess={function () { return _this.setState({ isSent: true }); }}/>); }, {
            onClose: function () { return _this.setState({ isOpen: false }); },
        });
    };
    RequestIntegrationButton.prototype.render = function () {
        var _this = this;
        var _a = this.state, isOpen = _a.isOpen, isSent = _a.isSent;
        var buttonText;
        if (isOpen) {
            buttonText = t('Requesting Installation');
        }
        else if (isSent) {
            buttonText = t('Installation Requested');
        }
        else {
            buttonText = t('Request Installation');
        }
        return (<StyledRequestIntegrationButton data-test-id="request-integration-button" disabled={isOpen || isSent} onClick={function () { return _this.openRequestModal(); }} priority="primary" size="small">
        {buttonText}
      </StyledRequestIntegrationButton>);
    };
    return RequestIntegrationButton;
}(React.Component));
export default RequestIntegrationButton;
var StyledRequestIntegrationButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=RequestIntegrationButton.jsx.map