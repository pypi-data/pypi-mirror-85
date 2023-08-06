import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import UserAvatar from 'app/components/avatar/userAvatar';
import Link from 'app/components/links/link';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import SentryTypes from 'app/sentryTypes';
function getMemberUser(member) {
    if (member.user) {
        return member.user;
    }
    // Adapt the member into a AvatarUser
    return {
        id: '',
        name: member.name,
        email: member.email,
        username: '',
        ip_address: '',
    };
}
var MemberBadge = function (_a) {
    var _b = _a.avatarSize, avatarSize = _b === void 0 ? 24 : _b, _c = _a.useLink, useLink = _c === void 0 ? true : _c, _d = _a.hideEmail, hideEmail = _d === void 0 ? false : _d, displayName = _a.displayName, displayEmail = _a.displayEmail, member = _a.member, orgId = _a.orgId, className = _a.className;
    var user = getMemberUser(member);
    var title = displayName ||
        user.name ||
        user.email ||
        user.username ||
        user.ipAddress ||
        // Because this can be used to render EventUser models, or User *interface*
        // objects from serialized Event models. we try both ipAddress and ip_address.
        user.ip_address;
    return (<StyledUserBadge className={className}>
      <StyledAvatar user={user} size={avatarSize}/>
      <StyledNameAndEmail>
        <StyledName useLink={useLink && !!orgId} hideEmail={hideEmail} to={(member && orgId && "/settings/" + orgId + "/members/" + member.id + "/") || ''}>
          {title}
        </StyledName>
        {!hideEmail && <StyledEmail>{displayEmail || user.email}</StyledEmail>}
      </StyledNameAndEmail>
    </StyledUserBadge>);
};
MemberBadge.propTypes = {
    displayName: PropTypes.node,
    displayEmail: PropTypes.node,
    avatarSize: PropTypes.number,
    /**
     * This is a Sentry member (not the user object that is a child of the member object)
     */
    member: SentryTypes.Member,
    orgId: PropTypes.string,
    useLink: PropTypes.bool,
    hideEmail: PropTypes.bool,
};
var StyledUserBadge = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledNameAndEmail = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"], ["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"])));
var StyledEmail = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"], ["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"])), space(0.25), function (p) { return p.theme.gray300; }, overflowEllipsis);
var StyledName = styled(function (_a) {
    var useLink = _a.useLink, to = _a.to, props = __rest(_a, ["useLink", "to"]);
    var forwardProps = omit(props, 'hideEmail');
    return useLink ? <Link to={to} {...forwardProps}/> : <span {...forwardProps}/>;
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"], ["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"])), function (p) { return (p.hideEmail ? 'inherit' : 'bold'); }, overflowEllipsis);
var StyledAvatar = styled(UserAvatar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"], ["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"])), space(3), space(3), space(1));
export default MemberBadge;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=memberBadge.jsx.map