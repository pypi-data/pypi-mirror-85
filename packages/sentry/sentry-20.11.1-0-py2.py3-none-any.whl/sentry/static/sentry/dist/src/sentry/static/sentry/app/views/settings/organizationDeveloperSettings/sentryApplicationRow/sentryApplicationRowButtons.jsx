import React from 'react';
import Access from 'app/components/acl/access';
import { t } from 'app/locale';
import ActionButtons from './actionButtons';
var SentryApplicationRowButtons = function (_a) {
    var organization = _a.organization, app = _a.app, onClickRemove = _a.onClickRemove, onClickPublish = _a.onClickPublish;
    var isInternal = app.status === 'internal';
    return (<Access access={['org:admin']}>
      {function (_a) {
        var hasAccess = _a.hasAccess;
        var disablePublishReason = '';
        var disableDeleteReason = '';
        // Publish & Delete buttons will always be disabled if the app is published
        if (app.status === 'published') {
            disablePublishReason = t('Published integrations cannot be re-published.');
            disableDeleteReason = t('Published integrations cannot be removed.');
        }
        else if (!hasAccess) {
            disablePublishReason = t('Organization owner permissions are required for this action.');
            disableDeleteReason = t('Organization owner permissions are required for this action.');
        }
        return (<ActionButtons org={organization} app={app} showPublish={!isInternal} showDelete onPublish={onClickPublish} onDelete={onClickRemove} disablePublishReason={disablePublishReason} disableDeleteReason={disableDeleteReason}/>);
    }}
    </Access>);
};
export default SentryApplicationRowButtons;
//# sourceMappingURL=sentryApplicationRowButtons.jsx.map