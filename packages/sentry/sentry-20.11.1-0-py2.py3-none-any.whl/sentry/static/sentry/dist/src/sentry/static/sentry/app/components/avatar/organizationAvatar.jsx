import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { explodeSlug } from 'app/utils';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import SentryTypes from 'app/sentryTypes';
var OrganizationAvatar = /** @class */ (function (_super) {
    __extends(OrganizationAvatar, _super);
    function OrganizationAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationAvatar.prototype.render = function () {
        var _a = this.props, organization = _a.organization, props = __rest(_a, ["organization"]);
        if (!organization) {
            return null;
        }
        var slug = (organization && organization.slug) || '';
        var title = explodeSlug(slug);
        return (<BaseAvatar {...props} type={(organization.avatar && organization.avatar.avatarType) || 'letter_avatar'} uploadPath="organization-avatar" uploadId={organization.avatar && organization.avatar.avatarUuid} letterId={slug} tooltip={slug} title={title}/>);
    };
    OrganizationAvatar.propTypes = __assign({ organization: SentryTypes.Organization.isRequired }, BaseAvatar.propTypes);
    return OrganizationAvatar;
}(React.Component));
export default OrganizationAvatar;
//# sourceMappingURL=organizationAvatar.jsx.map