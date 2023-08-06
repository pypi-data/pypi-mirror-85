import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconInfo } from 'app/icons';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
function ReleaseArchivedNotice(_a) {
    var onRestore = _a.onRestore, multi = _a.multi;
    return (<Alert icon={<IconInfo size="md"/>} type="warning">
      {multi
        ? t('These releases have been archived.')
        : t('This release has been archived.')}

      {!multi && onRestore && (<React.Fragment>
          {' '}
          <UnarchiveButton size="zero" priority="link" onClick={onRestore}>
            {t('Restore this release')}
          </UnarchiveButton>
        </React.Fragment>)}
    </Alert>);
}
var UnarchiveButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: inherit;\n  text-decoration: underline;\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: inherit;\n  text-decoration: underline;\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; });
export default ReleaseArchivedNotice;
var templateObject_1;
//# sourceMappingURL=releaseArchivedNotice.jsx.map