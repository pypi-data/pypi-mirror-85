import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import { addSuccessMessage } from 'app/actionCreators/indicator';
/**
 * This component is a hack for Split.
 * It will display the installation ID after installation so users can copy it and paste it in Split's website.
 * We also have a link for users to click so they can go to Split's website.
 */
var SplitInstallationIdModal = /** @class */ (function (_super) {
    __extends(SplitInstallationIdModal, _super);
    function SplitInstallationIdModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onCopy = function () { return __awaiter(_this, void 0, void 0, function () { return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: 
                //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
                return [4 /*yield*/, navigator.clipboard.writeText(this.props.installationId)];
                case 1: 
                //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
                return [2 /*return*/, _a.sent()];
            }
        }); }); };
        _this.handleContinue = function () {
            var delay = 2000;
            _this.onCopy();
            addSuccessMessage('Copied to clipboard');
            setTimeout(function () {
                window.open('https://app.split.io/org/admin/integrations');
            }, delay);
        };
        return _this;
    }
    SplitInstallationIdModal.prototype.render = function () {
        var _a = this.props, installationId = _a.installationId, closeModal = _a.closeModal;
        //no need to translate this temporary component
        return (<div>
        <ItemHolder>
          Copy this Installation ID and click to continue. You will use it to finish setup
          on Split.io.
        </ItemHolder>
        <ItemHolder>
          <TextCopyInput onCopy={this.onCopy}>{installationId}</TextCopyInput>
        </ItemHolder>
        <ButtonHolder>
          <Button size="small" onClick={closeModal}>
            Close
          </Button>
          <Button size="small" priority="primary" onClick={this.handleContinue}>
            Copy and Open Link
          </Button>
        </ButtonHolder>
      </div>);
    };
    SplitInstallationIdModal.propTypes = {
        installationId: PropTypes.string.isRequired,
        closeModal: PropTypes.func.isRequired,
    };
    return SplitInstallationIdModal;
}(React.Component));
export default SplitInstallationIdModal;
var ItemHolder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 10px;\n"], ["\n  margin: 10px;\n"])));
var ButtonHolder = styled(ItemHolder)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n  & button {\n    margin: 5px;\n  }\n"], ["\n  text-align: right;\n  & button {\n    margin: 5px;\n  }\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=SplitInstallationIdModal.jsx.map