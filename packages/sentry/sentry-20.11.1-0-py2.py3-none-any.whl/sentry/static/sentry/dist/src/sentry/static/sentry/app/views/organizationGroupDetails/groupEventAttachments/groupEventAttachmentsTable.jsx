import React from 'react';
import { t } from 'app/locale';
import GroupEventAttachmentsTableRow from 'app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsTableRow';
var GroupEventAttachmentsTable = function (_a) {
    var attachments = _a.attachments, orgId = _a.orgId, projectId = _a.projectId, groupId = _a.groupId, onDelete = _a.onDelete, deletedAttachments = _a.deletedAttachments;
    var tableRowNames = [t('Name'), t('Type'), t('Size'), t('Actions')];
    return (<table className="table events-table">
      <thead>
        <tr>
          {tableRowNames.map(function (name) { return (<th key={name}>{name}</th>); })}
        </tr>
      </thead>
      <tbody>
        {attachments.map(function (attachment) { return (<GroupEventAttachmentsTableRow key={attachment.id} attachment={attachment} orgId={orgId} projectId={projectId} groupId={groupId} onDelete={onDelete} isDeleted={deletedAttachments.some(function (id) { return attachment.id === id; })}/>); })}
      </tbody>
    </table>);
};
export default GroupEventAttachmentsTable;
//# sourceMappingURL=groupEventAttachmentsTable.jsx.map