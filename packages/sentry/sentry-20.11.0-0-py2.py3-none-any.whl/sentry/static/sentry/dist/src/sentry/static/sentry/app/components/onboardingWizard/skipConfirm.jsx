import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import space from 'app/styles/space';
import { fadeIn } from 'app/styles/animations';
import ButtonBar from 'app/components/buttonBar';
import HookOrDefault from 'app/components/hookOrDefault';
var SkipConfirm = /** @class */ (function (_super) {
    __extends(SkipConfirm, _super);
    function SkipConfirm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showConfirmation: false,
        };
        _this.toggleConfirm = function (e) {
            e.stopPropagation();
            _this.setState(function (state) { return ({ showConfirmation: !state.showConfirmation }); });
        };
        _this.handleSkip = function (e) {
            e.stopPropagation();
            _this.props.onSkip();
        };
        return _this;
    }
    SkipConfirm.prototype.render = function () {
        var children = this.props.children;
        return (<React.Fragment>
        {children({ skip: this.toggleConfirm })}
        <Confirmation visible={this.state.showConfirmation} onSkip={this.handleSkip} onDismiss={this.toggleConfirm}/>
      </React.Fragment>);
    };
    return SkipConfirm;
}(React.Component));
export default SkipConfirm;
var SkipHelp = HookOrDefault({
    hookName: 'onboarding-wizard:skip-help',
    defaultComponent: function () { return (<Button priority="primary" size="xsmall" to="https://forum.sentry.io/" external>
      {t('Community Forum')}
    </Button>); },
});
var Confirmation = styled(function (_a) {
    var onDismiss = _a.onDismiss, onSkip = _a.onSkip, _ = _a.visible, props = __rest(_a, ["onDismiss", "onSkip", "visible"]);
    return (<div onClick={onDismiss} {...props}>
    <p>{t("Not sure what to do? We're here for you!")}</p>
    <ButtonBar gap={1}>
      <SkipHelp />
      <Button size="xsmall" onClick={onSkip}>
        {t('Just skip')}
      </Button>
    </ButtonBar>
  </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n  padding: 0 ", ";\n  border-radius: ", ";\n  align-items: center;\n  flex-direction: column;\n  justify-content: center;\n  background: rgba(255, 255, 255, 0.9);\n  animation: ", " 200ms normal forwards;\n  font-size: ", ";\n\n  p {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n  padding: 0 ", ";\n  border-radius: ", ";\n  align-items: center;\n  flex-direction: column;\n  justify-content: center;\n  background: rgba(255, 255, 255, 0.9);\n  animation: ", " 200ms normal forwards;\n  font-size: ", ";\n\n  p {\n    margin-bottom: ", ";\n  }\n"])), function (p) { return (p.visible ? 'flex' : 'none'); }, space(3), function (p) { return p.theme.borderRadius; }, fadeIn, function (p) { return p.theme.fontSizeMedium; }, space(1));
var templateObject_1;
//# sourceMappingURL=skipConfirm.jsx.map