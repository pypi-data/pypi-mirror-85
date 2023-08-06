import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { fadeOut, pulse } from 'app/styles/animations';
import { IconCheckmark, IconWarning } from 'app/icons';
import Spinner from 'app/views/settings/components/forms/spinner';
/**
 * ControlState (i.e. loading/error icons) for form fields
 */
var ControlState = /** @class */ (function (_super) {
    __extends(ControlState, _super);
    function ControlState() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ControlState.prototype.render = function () {
        var _a = this.props, isSaving = _a.isSaving, isSaved = _a.isSaved, error = _a.error;
        return (<React.Fragment>
        {isSaving ? (<ControlStateWrapper>
            <FormSpinner />
          </ControlStateWrapper>) : isSaved ? (<ControlStateWrapper>
            <FieldIsSaved>
              <IconCheckmark size="18px"/>
            </FieldIsSaved>
          </ControlStateWrapper>) : null}

        {error ? (<ControlStateWrapper>
            <FieldError>
              <IconWarning size="18px"/>
            </FieldError>
          </ControlStateWrapper>) : null}
      </React.Fragment>);
    };
    return ControlState;
}(React.Component));
var ControlStateWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0 8px;\n"], ["\n  padding: 0 8px;\n"])));
var FieldIsSaved = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  animation: ", " 0.3s ease 2s 1 forwards;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  color: ", ";\n  animation: ", " 0.3s ease 2s 1 forwards;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.green300; }, fadeOut);
var FormSpinner = styled(Spinner)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: 0;\n"], ["\n  margin-left: 0;\n"])));
var FieldError = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  animation: ", " 1s ease infinite;\n"], ["\n  color: ", ";\n  animation: ", " 1s ease infinite;\n"])), function (p) { return p.theme.red300; }, function () { return pulse(1.15); });
export default ControlState;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=controlState.jsx.map