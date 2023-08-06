import { __extends, __rest } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import { sanitizeQuerySelector } from 'app/utils/sanitizeQuerySelector';
var FormPanel = /** @class */ (function (_super) {
    __extends(FormPanel, _super);
    function FormPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FormPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, title = _a.title, fields = _a.fields, access = _a.access, disabled = _a.disabled, additionalFieldProps = _a.additionalFieldProps, renderFooter = _a.renderFooter, renderHeader = _a.renderHeader, otherProps = __rest(_a, ["title", "fields", "access", "disabled", "additionalFieldProps", "renderFooter", "renderHeader"]);
        return (<Panel id={typeof title === 'string' ? sanitizeQuerySelector(title) : undefined}>
        {title && <PanelHeader>{title}</PanelHeader>}
        <PanelBody>
          {typeof renderHeader === 'function' && renderHeader({ title: title, fields: fields })}

          {fields.map(function (field) {
            if (typeof field === 'function') {
                return field();
            }
            var _ = field.defaultValue, fieldWithoutDefaultValue = __rest(field, ["defaultValue"]);
            // Allow the form panel disabled prop to override the fields
            // disabled prop, with fallback to the fields disabled state.
            if (disabled === true) {
                fieldWithoutDefaultValue.disabled = true;
                fieldWithoutDefaultValue.disabledReason = undefined;
            }
            return (<FieldFromConfig access={access} disabled={disabled} key={field.name} {...otherProps} {...additionalFieldProps} field={fieldWithoutDefaultValue} highlighted={_this.props.highlighted === "#" + field.name}/>);
        })}
          {typeof renderFooter === 'function' && renderFooter({ title: title, fields: fields })}
        </PanelBody>
      </Panel>);
    };
    return FormPanel;
}(React.Component));
export default FormPanel;
//# sourceMappingURL=formPanel.jsx.map