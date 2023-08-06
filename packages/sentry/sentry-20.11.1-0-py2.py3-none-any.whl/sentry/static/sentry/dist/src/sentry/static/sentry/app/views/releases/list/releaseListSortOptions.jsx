import React from 'react';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
var ReleaseListSortOptions = function (_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    var options = [
        {
            key: 'date',
            label: t('Date Created'),
        },
        {
            key: 'sessions',
            label: t('Total Sessions'),
        },
        {
            key: 'users_24h',
            label: t('Active Users'),
        },
        {
            key: 'crash_free_users',
            label: t('Crash Free Users'),
        },
        {
            key: 'crash_free_sessions',
            label: t('Crash Free Sessions'),
        },
    ];
    return (<ReleaseListDropdown label={t('Sort by')} options={options} selected={selected} onSelect={onSelect}/>);
};
export default ReleaseListSortOptions;
//# sourceMappingURL=releaseListSortOptions.jsx.map