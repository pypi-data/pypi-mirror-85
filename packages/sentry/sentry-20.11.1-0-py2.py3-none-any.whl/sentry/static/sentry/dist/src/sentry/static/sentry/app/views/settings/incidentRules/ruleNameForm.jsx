import { __extends } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import TextField from 'app/views/settings/components/forms/textField';
var RuleNameForm = /** @class */ (function (_super) {
    __extends(RuleNameForm, _super);
    function RuleNameForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RuleNameForm.prototype.render = function () {
        var disabled = this.props.disabled;
        return (<Panel>
        <PanelHeader>{t('Give your rule a name')}</PanelHeader>
        <PanelBody>
          <TextField disabled={disabled} name="name" label={t('Rule Name')} help={t('Give your rule a name so it is easy to manage later')} placeholder={t('Something really bad happened')} required/>
        </PanelBody>
      </Panel>);
    };
    return RuleNameForm;
}(React.PureComponent));
export default RuleNameForm;
//# sourceMappingURL=ruleNameForm.jsx.map