import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import SentryTypes from 'app/sentryTypes';
import UserAvatar from 'app/components/avatar/userAvatar';
import Tooltip from 'app/components/tooltip';
var defaultProps = {
    avatarSize: 28,
    maxVisibleAvatars: 5,
    typeMembers: 'users',
    tooltipOptions: {},
};
var AvatarList = /** @class */ (function (_super) {
    __extends(AvatarList, _super);
    function AvatarList() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AvatarList.prototype.render = function () {
        var _a = this.props, className = _a.className, users = _a.users, avatarSize = _a.avatarSize, maxVisibleAvatars = _a.maxVisibleAvatars, renderTooltip = _a.renderTooltip, typeMembers = _a.typeMembers, tooltipOptions = _a.tooltipOptions;
        var visibleUsers = users.slice(0, maxVisibleAvatars);
        var numCollapsedUsers = users.length - visibleUsers.length;
        if (!tooltipOptions.position) {
            tooltipOptions.position = 'top';
        }
        return (<AvatarListWrapper className={className}>
        {!!numCollapsedUsers && (<Tooltip title={numCollapsedUsers + " other " + typeMembers}>
            <CollapsedUsers size={avatarSize}>
              {numCollapsedUsers < 99 && <Plus>+</Plus>}
              {numCollapsedUsers}
            </CollapsedUsers>
          </Tooltip>)}
        {visibleUsers.map(function (user) { return (<StyledAvatar key={user.id + "-" + user.email} user={user} size={avatarSize} renderTooltip={renderTooltip} tooltipOptions={tooltipOptions} hasTooltip/>); })}
      </AvatarListWrapper>);
    };
    AvatarList.propTypes = {
        users: PropTypes.arrayOf(SentryTypes.User).isRequired,
        avatarSize: PropTypes.number,
        maxVisibleAvatars: PropTypes.number,
        renderTooltip: PropTypes.func,
        tooltipOptions: PropTypes.object,
        typeMembers: PropTypes.string,
    };
    AvatarList.defaultProps = defaultProps;
    return AvatarList;
}(React.Component));
export default AvatarList;
// used in releases list page to do some alignment
export var AvatarListWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row-reverse;\n"], ["\n  display: flex;\n  flex-direction: row-reverse;\n"])));
var Circle = function (p) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: 50%;\n  border: 2px solid ", ";\n  margin-left: -8px;\n  cursor: default;\n\n  &:hover {\n    z-index: 1;\n  }\n"], ["\n  border-radius: 50%;\n  border: 2px solid ", ";\n  margin-left: -8px;\n  cursor: default;\n\n  &:hover {\n    z-index: 1;\n  }\n"])), p.theme.background); };
var StyledAvatar = styled(UserAvatar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  overflow: hidden;\n  ", ";\n"], ["\n  overflow: hidden;\n  ", ";\n"])), Circle);
var CollapsedUsers = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  text-align: center;\n  font-weight: 600;\n  background-color: ", ";\n  color: ", ";\n  font-size: ", "px;\n  width: ", "px;\n  height: ", "px;\n  ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  text-align: center;\n  font-weight: 600;\n  background-color: ", ";\n  color: ", ";\n  font-size: ", "px;\n  width: ", "px;\n  height: ", "px;\n  ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; }, function (p) { return Math.floor(p.size / 2.3); }, function (p) { return p.size; }, function (p) { return p.size; }, Circle);
var Plus = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 10px;\n  margin-left: 1px;\n  margin-right: -1px;\n"], ["\n  font-size: 10px;\n  margin-left: 1px;\n  margin-right: -1px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=avatarList.jsx.map