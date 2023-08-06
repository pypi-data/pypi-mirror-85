import { __extends } from "tslib";
import { Observer } from 'mobx-react';
import React from 'react';
import ControlState from 'app/views/settings/components/forms/field/controlState';
import FormState from 'app/components/forms/state';
/**
 * ControlState (i.e. loading/error icons) for connected form components
 */
var FormFieldControlState = /** @class */ (function (_super) {
    __extends(FormFieldControlState, _super);
    function FormFieldControlState() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FormFieldControlState.prototype.render = function () {
        var _a = this.props, model = _a.model, name = _a.name;
        return (<Observer>
        {function () {
            var isSaving = model.getFieldState(name, FormState.SAVING);
            var isSaved = model.getFieldState(name, FormState.READY);
            var error = model.getError(name);
            return <ControlState isSaving={isSaving} isSaved={isSaved} error={error}/>;
        }}
      </Observer>);
    };
    return FormFieldControlState;
}(React.Component));
export default FormFieldControlState;
//# sourceMappingURL=controlState.jsx.map