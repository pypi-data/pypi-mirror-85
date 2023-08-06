import React from 'react';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { Panel, PanelBody } from 'app/components/panels';
var EmptyState = function (_a) {
    var withIcon = _a.withIcon, children = _a.children;
    return (<Panel>
    <PanelBody>
      <EmptyStateWarning small withIcon={withIcon}>
        {children}
      </EmptyStateWarning>
    </PanelBody>
  </Panel>);
};
export default EmptyState;
//# sourceMappingURL=emptyState.jsx.map