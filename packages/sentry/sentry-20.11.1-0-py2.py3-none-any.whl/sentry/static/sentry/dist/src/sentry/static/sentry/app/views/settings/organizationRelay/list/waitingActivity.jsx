import React from 'react';
import { t, tct } from 'app/locale';
import { Panel } from 'app/components/panels';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import CommandLine from 'app/components/commandLine';
import { IconRefresh } from 'app/icons';
var WaitingActivity = function (_a) {
    var onRefresh = _a.onRefresh;
    return (<Panel>
    <EmptyMessage title={t('Waiting on Activity!')} description={tct('Run relay in your terminal with [commandLine]', {
        commandLine: <CommandLine>{'relay run'}</CommandLine>,
    })} action={<Button icon={<IconRefresh />} onClick={onRefresh}>
          {t('Refresh')}
        </Button>}/>
  </Panel>);
};
export default WaitingActivity;
//# sourceMappingURL=waitingActivity.jsx.map