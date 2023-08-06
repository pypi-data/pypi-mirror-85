import React from 'react';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var EmptyState = function () { return (<Panel>
    <EmptyMessage>{t('No Keys Registered.')}</EmptyMessage>
  </Panel>); };
export default EmptyState;
//# sourceMappingURL=emptyState.jsx.map