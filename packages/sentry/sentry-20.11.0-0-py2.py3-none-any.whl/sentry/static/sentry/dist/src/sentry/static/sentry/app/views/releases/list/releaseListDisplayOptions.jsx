import React from 'react';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
var options = [
    {
        key: 'active',
        label: t('Active'),
    },
    {
        key: 'archived',
        label: t('Archived'),
    },
];
function ReleaseListDisplayOptions(_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    return (<ReleaseListDropdown label={t('Display')} options={options} selected={selected} onSelect={onSelect}/>);
}
export default ReleaseListDisplayOptions;
//# sourceMappingURL=releaseListDisplayOptions.jsx.map