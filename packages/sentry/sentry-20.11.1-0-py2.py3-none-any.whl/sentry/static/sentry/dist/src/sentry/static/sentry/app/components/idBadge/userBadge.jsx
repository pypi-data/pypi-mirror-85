import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import UserAvatar from 'app/components/avatar/userAvatar';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import SentryTypes from 'app/sentryTypes';
var UserBadge = function (_a) {
    var _b = _a.avatarSize, avatarSize = _b === void 0 ? 24 : _b, _c = _a.hideEmail, hideEmail = _c === void 0 ? false : _c, displayName = _a.displayName, displayEmail = _a.displayEmail, user = _a.user, className = _a.className;
    var title = displayName ||
        (user &&
            (user.name ||
                user.email ||
                user.username ||
                user.ipAddress ||
                // Because this can be used to render EventUser models, or User *interface*
                // objects from serialized Event models. we try both ipAddress and ip_address.
                user.ip_address ||
                user.id));
    return (<StyledUserBadge className={className}>
      <StyledAvatar user={user} size={avatarSize}/>
      <StyledNameAndEmail>
        <StyledName hideEmail={!!hideEmail}>{title}</StyledName>
        {!hideEmail && <StyledEmail>{displayEmail || (user && user.email)}</StyledEmail>}
      </StyledNameAndEmail>
    </StyledUserBadge>);
};
UserBadge.propTypes = {
    displayName: PropTypes.node,
    displayEmail: PropTypes.node,
    avatarSize: PropTypes.number,
    /**
     * Sometimes we may not have the member object (i.e. the current user, `ConfigStore.get('user')`,
     * is an user, not a member)
     */
    user: SentryTypes.User,
    hideEmail: PropTypes.bool,
};
var StyledUserBadge = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledNameAndEmail = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"], ["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"])));
var StyledEmail = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"], ["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"])), space(0.25), function (p) { return p.theme.gray300; }, overflowEllipsis);
var StyledName = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"], ["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"])), function (p) { return (p.hideEmail ? 'inherit' : 'bold'); }, overflowEllipsis);
var StyledAvatar = styled(UserAvatar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"], ["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"])), space(3), space(3), space(1));
export default UserBadge;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=userBadge.jsx.map