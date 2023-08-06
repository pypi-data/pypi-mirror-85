import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import FieldControlState from 'app/views/settings/components/forms/field/fieldControlState';
import QuestionTooltip from 'app/components/questionTooltip';
import space from 'app/styles/space';
var defaultProps = {
    flexibleControlStateSize: false,
};
var FieldControl = /** @class */ (function (_super) {
    __extends(FieldControl, _super);
    function FieldControl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FieldControl.prototype.render = function () {
        var _a = this.props, inline = _a.inline, alignRight = _a.alignRight, disabled = _a.disabled, disabledReason = _a.disabledReason, flexibleControlStateSize = _a.flexibleControlStateSize, errorState = _a.errorState, controlState = _a.controlState, children = _a.children, hideControlState = _a.hideControlState;
        return (<FieldControlErrorWrapper inline={inline}>
        <FieldControlWrapper>
          <FieldControlStyled alignRight={alignRight}>{children}</FieldControlStyled>

          {disabled && disabledReason && (<DisabledIndicator className="disabled-indicator">
              <StyledQuestionTooltip title={disabledReason} size="sm" position="top"/>
            </DisabledIndicator>)}

          {!hideControlState && (<FieldControlState flexibleControlStateSize={!!flexibleControlStateSize}>
              {controlState}
            </FieldControlState>)}
        </FieldControlWrapper>

        {!hideControlState && errorState}
      </FieldControlErrorWrapper>);
    };
    FieldControl.propTypes = {
        inline: PropTypes.bool,
        alignRight: PropTypes.bool,
        disabled: PropTypes.bool,
        disabledReason: PropTypes.node,
        flexibleControlStateSize: PropTypes.bool,
        controlState: PropTypes.node,
        errorState: PropTypes.node,
    };
    FieldControl.defaultProps = defaultProps;
    return FieldControl;
}(React.Component));
export default FieldControl;
// This wraps Control + ControlError message
// * can NOT be a flex box here because of `position: absolute` on "control error message"
// * can NOT have overflow hidden because "control error message" overflows
var FieldControlErrorWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.inline ? 'width: 50%; padding-left: 10px;' : ''); });
var FieldControlStyled = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  position: relative;\n  ", ";\n"], ["\n  color: ", ";\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  position: relative;\n  ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return (p.alignRight ? 'align-items: flex-end;' : ''); });
var FieldControlWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  flex-shrink: 0;\n"])));
var StyledQuestionTooltip = styled(QuestionTooltip)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: block;\n  margin: 0 auto;\n"], ["\n  display: block;\n  margin: 0 auto;\n"])));
var DisabledIndicator = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=fieldControl.jsx.map