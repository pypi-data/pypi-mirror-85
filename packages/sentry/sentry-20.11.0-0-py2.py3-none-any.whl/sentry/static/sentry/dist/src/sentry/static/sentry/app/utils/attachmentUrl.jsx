import { __extends } from "tslib";
import React from 'react';
import withOrganization from 'app/utils/withOrganization';
import Role from 'app/components/acl/role';
var AttachmentUrl = /** @class */ (function (_super) {
    __extends(AttachmentUrl, _super);
    function AttachmentUrl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AttachmentUrl.prototype.getDownloadUrl = function () {
        var _a = this.props, attachment = _a.attachment, organization = _a.organization, eventId = _a.eventId, projectId = _a.projectId;
        return "/api/0/projects/" + organization.slug + "/" + projectId + "/events/" + eventId + "/attachments/" + attachment.id + "/";
    };
    AttachmentUrl.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, organization = _a.organization;
        return (<Role role={organization.attachmentsRole}>
        {function (_a) {
            var hasRole = _a.hasRole;
            return children(hasRole ? _this.getDownloadUrl() : null);
        }}
      </Role>);
    };
    return AttachmentUrl;
}(React.PureComponent));
export default withOrganization(AttachmentUrl);
//# sourceMappingURL=attachmentUrl.jsx.map