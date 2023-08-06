import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { userDisplayName } from 'app/utils/formatters';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import SentryTypes from 'app/sentryTypes';
import { isRenderFunc } from 'app/utils/isRenderFunc';
var defaultProps = {
    // Default gravatar to false in order to support transparent avatars
    // Avatar falls through to letter avatars if a remote image fails to load,
    // however gravatar sends back a transparent image when it does not find a gravatar,
    // so there's little we have to control whether we need to fallback to letter avatar
    gravatar: false,
};
function isActor(maybe) {
    return typeof maybe.email === 'undefined';
}
var UserAvatar = /** @class */ (function (_super) {
    __extends(UserAvatar, _super);
    function UserAvatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getType = function (user, gravatar) {
            if (isActor(user)) {
                return 'letter_avatar';
            }
            if (user.avatar) {
                return user.avatar.avatarType;
            }
            if (user.options && user.options.avatarType) {
                return user.options.avatarType;
            }
            return user.email && gravatar ? 'gravatar' : 'letter_avatar';
        };
        return _this;
    }
    UserAvatar.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, user = _d.user, gravatar = _d.gravatar, renderTooltip = _d.renderTooltip, props = __rest(_d, ["user", "gravatar", "renderTooltip"]);
        if (!user) {
            return null;
        }
        var type = this.getType(user, gravatar);
        var tooltip = null;
        if (isRenderFunc(renderTooltip)) {
            tooltip = renderTooltip(user);
        }
        else if (props.tooltip) {
            tooltip = props.tooltip;
        }
        else {
            tooltip = userDisplayName(user);
        }
        var avatarData = isActor(user)
            ? {
                uploadId: '',
                gravatarId: '',
                letterId: user.name,
                title: user.name,
            }
            : {
                uploadId: (_b = (_a = user.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid) !== null && _b !== void 0 ? _b : '',
                gravatarId: (_c = user.email) === null || _c === void 0 ? void 0 : _c.toLowerCase(),
                letterId: user.email || user.username || user.id || user.ip_address,
                title: user.name || user.email || user.username || '',
            };
        return (<BaseAvatar round {...props} type={type} uploadPath="avatar" uploadId={avatarData.uploadId} gravatarId={avatarData.gravatarId} letterId={avatarData.letterId} title={avatarData.title} tooltip={tooltip}/>);
    };
    UserAvatar.propTypes = __assign({ user: SentryTypes.User, gravatar: PropTypes.bool, renderTooltip: PropTypes.func }, BaseAvatar.propTypes);
    UserAvatar.defaultProps = defaultProps;
    return UserAvatar;
}(React.Component));
export default UserAvatar;
//# sourceMappingURL=userAvatar.jsx.map