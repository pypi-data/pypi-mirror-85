import React from 'react';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { IconWarning } from 'app/icons';
import Rules from './rules';
var Content = function (_a) {
    var rules = _a.rules, disabled = _a.disabled, onDeleteRule = _a.onDeleteRule, onEditRule = _a.onEditRule;
    if (rules.length === 0) {
        return (<EmptyMessage icon={<IconWarning size="xl"/>} description={t('You have no data scrubbing rules')}/>);
    }
    return (<Rules rules={rules} onDeleteRule={onDeleteRule} onEditRule={onEditRule} disabled={disabled}/>);
};
export default Content;
//# sourceMappingURL=content.jsx.map