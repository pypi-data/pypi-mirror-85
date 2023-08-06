import { __awaiter, __generator } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import FieldHelp from 'app/views/settings/components/forms/field/fieldHelp';
import Textarea from 'app/views/settings/components/forms/controls/textarea';
import Field from 'app/views/settings/components/forms/field';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
var Form = function (_a) {
    var values = _a.values, onChange = _a.onChange, errors = _a.errors, onValidate = _a.onValidate, isFormValid = _a.isFormValid, disables = _a.disables, onValidateKey = _a.onValidateKey, onSave = _a.onSave;
    var handleChange = function (field) { return function (event) {
        onChange(field, event.target.value);
    }; };
    var handleSubmit = function () {
        if (isFormValid) {
            onSave();
        }
    };
    // code below copied from src/sentry/static/sentry/app/views/organizationIntegrations/SplitInstallationIdModal.tsx
    // TODO: fix the common method selectText
    var onCopy = function (value) { return function () { return __awaiter(void 0, void 0, void 0, function () { return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: 
            //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [4 /*yield*/, navigator.clipboard.writeText(value)];
            case 1: 
            //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [2 /*return*/, _a.sent()];
        }
    }); }); }; };
    return (<form onSubmit={handleSubmit} id="relay-form">
      <Field flexibleControlStateSize label={t('Display Name')} error={errors.name} inline={false} stacked required>
        <Input type="text" name="name" placeholder={t('Display Name')} onChange={handleChange('name')} value={values.name} onBlur={onValidate('name')} disabled={disables.name}/>
      </Field>

      {disables.publicKey ? (<Field flexibleControlStateSize label={t('Public Key')} inline={false} stacked>
          <TextCopyInput onCopy={onCopy(values.publicKey)}>
            {values.publicKey}
          </TextCopyInput>
        </Field>) : (<Field label={t('Public Key')} error={errors.publicKey} flexibleControlStateSize inline={false} stacked required>
          <Input type="text" name="publicKey" placeholder={t('Public Key')} onChange={handleChange('publicKey')} value={values.publicKey} onBlur={onValidateKey}/>
          <FieldHelp>
            {t('Only enter the Public Key value from your credentials file. Never share the Secret key with Sentry or any third party')}
          </FieldHelp>
        </Field>)}
      <Field flexibleControlStateSize label={t('Description')} inline={false} stacked>
        <Textarea name="description" placeholder={t('Description')} onChange={handleChange('description')} value={values.description} disabled={disables.description}/>
      </Field>
    </form>);
};
export default Form;
//# sourceMappingURL=form.jsx.map