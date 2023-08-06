import { t, tct } from 'app/locale';
import { defined } from 'app/utils';
export function formatStoreCrashReports(value, organizationValue) {
    if (value === null && defined(organizationValue)) {
        return tct('Inherit organization settings ([organizationValue])', {
            organizationValue: formatStoreCrashReports(organizationValue),
        });
    }
    if (value === -1) {
        return t('Unlimited');
    }
    if (value === 0) {
        return t('Disabled');
    }
    return tct('[value] per issue', { value: value });
}
export var SettingScope;
(function (SettingScope) {
    SettingScope[SettingScope["Organization"] = 0] = "Organization";
    SettingScope[SettingScope["Project"] = 1] = "Project";
})(SettingScope || (SettingScope = {}));
export function getStoreCrashReportsValues(settingScope) {
    var values = [
        0,
        1,
        5,
        10,
        20,
        -1,
    ];
    if (settingScope === SettingScope.Project) {
        values.unshift(null); // inherit option
    }
    return values;
}
//# sourceMappingURL=crashReports.jsx.map