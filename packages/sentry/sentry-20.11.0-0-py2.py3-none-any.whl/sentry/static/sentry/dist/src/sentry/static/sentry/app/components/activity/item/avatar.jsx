import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import UserAvatar from 'app/components/avatar/userAvatar';
import { IconSentry } from 'app/icons';
import Placeholder from 'app/components/placeholder';
import SentryTypes from 'app/sentryTypes';
function ActivityAvatar(_a) {
    var className = _a.className, type = _a.type, user = _a.user, _b = _a.size, size = _b === void 0 ? 38 : _b;
    if (user) {
        return <UserAvatar user={user} size={size} className={className}/>;
    }
    if (type === 'system') {
        // Return Sentry avatar
        return (<SystemAvatar className={className} size={size}>
        <StyledIconSentry size="md"/>
      </SystemAvatar>);
    }
    return (<Placeholder className={className} width={size + "px"} height={size + "px"} shape="circle"/>);
}
ActivityAvatar.propTypes = {
    user: SentryTypes.User,
    type: PropTypes.oneOf(['system', 'user']),
    size: PropTypes.number,
};
export default ActivityAvatar;
var SystemAvatar = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  border-radius: 50%;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  border-radius: 50%;\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; });
var StyledIconSentry = styled(IconSentry)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-bottom: 3px;\n"], ["\n  padding-bottom: 3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=avatar.jsx.map