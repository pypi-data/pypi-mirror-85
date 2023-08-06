import { __assign } from "tslib";
import React from 'react';
import { tct } from 'app/locale';
import { IconInfo } from 'app/icons';
import { crashReportTypes } from 'app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsFilter';
import Alert from '../alert';
import Link from '../links/link';
var EventAttachmentsCrashReportsNotice = function (_a) {
    var orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, location = _a.location, groupId = _a.groupId;
    var settingsUrl = "/settings/" + orgSlug + "/projects/" + projectSlug + "/security-and-privacy/";
    var attachmentsUrl = {
        pathname: "/organizations/" + orgSlug + "/issues/" + groupId + "/attachments/",
        query: __assign(__assign({}, location.query), { types: crashReportTypes }),
    };
    return (<Alert type="info" icon={<IconInfo size="md"/>}>
      {tct('Your limit of stored crash reports has been reached for this issue. [attachmentsLink: View crashes] or [settingsLink: configure limit].', {
        attachmentsLink: <Link to={attachmentsUrl} data-test-id="attachmentsLink"/>,
        settingsLink: <Link to={settingsUrl} data-test-id="settingsLink"/>,
    })}
    </Alert>);
};
export default EventAttachmentsCrashReportsNotice;
//# sourceMappingURL=eventAttachmentsCrashReportsNotice.jsx.map