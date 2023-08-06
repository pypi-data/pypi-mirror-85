import React from 'react';
import { t } from 'app/locale';
import { IconSiren } from 'app/icons';
import Button from 'app/components/button';
import Access from 'app/components/acl/access';
import { navigateTo } from 'app/actionCreators/navigation';
var CreateRuleButton = function (_a) {
    var router = _a.router, organization = _a.organization, buttonProps = _a.buttonProps, iconProps = _a.iconProps;
    return (<Access organization={organization} access={['project:write']}>
    {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Button disabled={!hasAccess} title={!hasAccess
            ? t('Users with admin permission or higher can create alert rules.')
            : undefined} onClick={function (e) {
            e.preventDefault();
            navigateTo("/organizations/" + organization.slug + "/alerts/:projectId/new/?referrer=alert_stream", router);
        }} priority="primary" href="#" icon={<IconSiren {...iconProps}/>} {...buttonProps}>
        {t('Create Alert Rule')}
      </Button>);
    }}
  </Access>);
};
export default CreateRuleButton;
//# sourceMappingURL=createRuleButton.jsx.map